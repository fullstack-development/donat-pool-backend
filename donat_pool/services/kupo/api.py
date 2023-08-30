from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework.decorators import action
from rest_framework import status
from .models import Value, Utxo, FundraisingInfo
from django.conf import settings
from .client import KupoClient, KupoRequestError
from pycardano import Datum
from .serialization import deserialize_datum
import json 
from rest_framework import serializers

class FundraisingInfoView(APIView):
    def __init__(self, **kwargs):
        View.__init__(kwargs)
        self.kupo_client = KupoClient()

    # TODO: check if we need get here
    def get(self, request, action):

        if action == "all-projects":
            return self.all_projects(request)

    @action(methods=['get'], detail=False)
    def all_projects(self, request):
        try:
            utxos = self.kupo_client.utxos_at(settings.FUNDRAISING_SCRIPT_ADDRESS)
        except KupoRequestError as e:
            return Response({"error": f"Request to external API failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        fundraisings = list(map(self.utxo_to_fundraising_info, utxos))
        return Response({"msg": "OK", "projects": fundraisings}, status=200) # TODO: response with frInfo list

    def utxo_to_fundraising_info(self, utxo):
        value = utxo.value
        thread_token = value.get_utxo_thread_token()
        raisedAmt = value.coins - settings.FUNDRAISING_SYSTEM_ADA_AMOUNT
        if thread_token == None:
            return
        
        datum_encoded = self.kupo_client.get_datum_by_hash(utxo.datum_hash)
        datum_fields = deserialize_datum(datum_encoded)
        title = datum_fields.frTitle.decode('utf-8')
        goal = datum_fields.frAmount
        deadline = datum_fields.frDeadline
        creator = datum_fields.creatorPkh  # TODO: how to decode ???
        threadTokenCurrency = thread_token.currencySymbol
        threadTokenName = thread_token.tokenName.decode('ascii')
        isCompleted = raisedAmt >= goal # TODO: or deadline is already reached

        frInfo = FundraisingInfo(title, goal, raisedAmt, deadline, threadTokenCurrency, threadTokenName, isCompleted)
        fr_serialized =  FundraisingSerializer(frInfo)
        return fr_serialized.data
        
class FundraisingSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    goal = serializers.IntegerField()
    raisedAmt = serializers.IntegerField()
    deadline = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    threadTokenCurrency = serializers.CharField(max_length=255)
    threadTokenName = serializers.CharField(max_length=255)
    isCompleted = serializers.BooleanField()
