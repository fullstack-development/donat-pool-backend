from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework.decorators import action
from rest_framework import status
from .models import FundraisingInfo
from django.conf import settings
from .client import KupoClient, KupoRequestError
from .serialization import deserialize_datum, deserialize_address
from rest_framework import serializers
from donat_pool.ext.time import current_time_ms
from donat_pool.ext.list import clean_list, map_by_list

class FundraisingInfoView(APIView):
    def __init__(self, **kwargs):
        View.__init__(kwargs)
        self.kupo_client = KupoClient()

    def get(self, request, action):
        if action == "all-projects":
            return self.all_projects(request)

    @action(methods=['get'], detail=False)
    def all_projects(self, request):
        try:
            utxos = self.kupo_client.utxos_at(settings.FUNDRAISING_SCRIPT_ADDRESS)
        except KupoRequestError as e:
            return Response(
                {"error": f"Request to Kupo failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        fundraisings = map_by_list(self.utxo_to_fundraising_info, utxos)
        cleaned_fundraisings = clean_list(fundraisings)
        return Response(cleaned_fundraisings, status=200)
    
    def utxo_to_fundraising_info(self, utxo):
        value = utxo.value
        thread_token = value.get_utxo_thread_token()
        raised_amt = value.coins - settings.FUNDRAISING_SYSTEM_ADA_AMOUNT
        if thread_token == None:
            return
        
        datum_encoded = self.kupo_client.get_datum_by_hash(utxo.datum_hash)
        datum_fields = deserialize_datum(datum_encoded)

        creator = None
        title = datum_fields.frTitle.decode('utf-8')
        goal = datum_fields.frAmount
        deadline = datum_fields.frDeadline
        thread_token_currency = thread_token.currencySymbol
        thread_token_name = thread_token.tokenName.decode('ascii')

        now = current_time_ms()
        isCompleted = raised_amt >= goal or now >= deadline
        
        frInfo = FundraisingInfo(creator, title, goal, raised_amt, deadline, thread_token_currency, thread_token_name, isCompleted)
        fr_serialized =  FundraisingSerializer(frInfo)
        return fr_serialized.data
        
class FundraisingSerializer(serializers.Serializer):
    creator = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    goal = serializers.IntegerField()
    raisedAmt = serializers.IntegerField()
    deadline = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    threadTokenCurrency = serializers.CharField(max_length=255)
    threadTokenName = serializers.CharField(max_length=255)
    isCompleted = serializers.BooleanField()
