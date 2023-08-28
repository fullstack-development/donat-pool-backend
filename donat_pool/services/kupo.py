import requests
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status

import json 

THREAD_TOKEN_NAME="FundraisingThreadToken"
VER_TOKEN_CURRENCY=""
VER_TOKEN_NAME="VerificationToken"

class KupoApiView(APIView):

    def get(self, request, action):
        if action == "utxos-at":
            return self.utxos_at(request)

    @action(methods=['get'], detail=False)
    def utxos_at(self, request):
        utxos_at_url = "https://kupo.donat-pool.io/matches/addr_test1xzyyxy9s609346ckm5eyv2qn3s56zc8spajw654yxsrwwkuggvgtp57trt43dhfjgc5p8rpf59s0qrmya4f2gdqxuads6zfmy0?unspent"

        try:
            response = requests.get(utxos_at_url)

            if response.status_code == 200:
                response_data = response.json()
                self.parse_utxos_at(response_data)
                return Response({"msg": "OK"}, status=200)

            else:
                return Response({"error": "Failed to fetch data from the external API"}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Request to external API failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_utxos_at(self, utxosAtResponse):
        for utxo_data in utxosAtResponse:
            utxo = self.parse_utxo(utxo_data)
        

    def parse_utxo(self, utxo_data):
        try:
            value = Value(utxo_data["value"]["coins"], utxo_data["value"]["assets"])
            utxo = Utxo(value, utxo_data["datum_hash"], utxo_data["datum_type"])
            return utxo
        except KeyError as e:
            print(f"KeyError: {e}")
            return Response({"error": "Can't parse kupo utxos_at response"}, status=500)
        
class Value:
    def __init__(self, coins, assets):
        self.coins = coins
        self.assets = assets

class Utxo:
    def __init__(self, value: Value, datum_hash, datum_type):
        self.value = value
        self.datum_hash = datum_hash
        self.datum_type = datum_type

class FundraisingInfo:
    def __init__(self, creator, title, goal, raisedAmt, deadline, threadTokenCurrency, threadTokenName, isCompleted):
        self.creator = creator
        self.title = title
        self.goal = goal
        self.raisedAmt = raisedAmt
        self.deadline = deadline
        self.threadTokenCurrency = threadTokenCurrency
        self.threadTokenName = threadTokenName
        self.isCompleted = isCompleted

