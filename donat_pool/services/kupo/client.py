import requests
from .models import Value, Utxo
from django.conf import settings
from donat_pool.ext.list import map_by_list
import logging

class KupoClient:

    def utxos_at(self, script_address):
        utxos_at_url = settings.KUPO_SERVICE + "matches/" + script_address + "?unspent"

        try:
            response_data = self.get_from_kupo(utxos_at_url)
            utxos = map_by_list(self.parse_utxo, response_data)
            return utxos
        
        except KupoApiError:
            raise

    def get_datum_by_hash(self, datum_hash):
        get_datum_url = settings.KUPO_SERVICE + "datums/" + datum_hash

        try:
            response_data = self.get_from_kupo(get_datum_url)
            return response_data.get("datum", None)
        except KupoApiError:
            raise 

    def get_from_kupo(self, url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                raise KupoErrorResponse(response)
            
        except requests.exceptions.RequestException as e:
            raise KupoErrorResponse(e)

    def parse_utxo(self, utxo_data):
        try:
            value = Value(utxo_data["value"]["coins"], utxo_data["value"]["assets"])
            utxo = Utxo(value, utxo_data["datum_hash"], utxo_data["datum_type"])
            return utxo
        except KeyError as e:
            raise UtxoParsingError(e, utxo)
        
class KupoApiError(Exception):
    def __init__(self, exception_info):
      self.exception_info = exception_info

    def __str__(self):
      return repr(self.exception_info)
    
class KupoRequestError(KupoApiError):
    def __init__(self, resp):
      super().__init__("Kupo respond with error: " + str(resp))

class KupoErrorResponse(KupoApiError):
    def __init__(self, e):
      super().__init__("Error during Kupo request: " + str(e))

class UtxoParsingError(KupoApiError):
    def __init__(self, e, utxo):
      super().__init__("Error in UTXO parsing: " + str(e) + " UTXO: " + str(utxo))


    