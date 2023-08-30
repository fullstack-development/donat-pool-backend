import requests
from .models import Value, Utxo
from django.conf import settings

class KupoClient:

    def utxos_at(self, script_address):
        utxos_at_url = settings.KUPO_SERVICE + "matches/" + script_address + "?unspent"

        try:
            response_data = self.get_from_kupo(utxos_at_url)
            utxos = list(map(self.parse_utxo, response_data))
            return utxos
        except KupoRequestError:
            raise

    def get_datum_by_hash(self, datum_hash):
        get_datum_url = settings.KUPO_SERVICE + "datums/" + datum_hash

        try:
            response_data = self.get_from_kupo(get_datum_url)
            return response_data.get("datum", None)
        except KupoRequestError:
            raise 

    def get_from_kupo(self, url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                raise KupoRequestError # pass error data
            
        except requests.exceptions.RequestException as e:
            raise KupoRequestError # pass error data

    def parse_utxo(self, utxo_data):
        try:
            value = Value(utxo_data["value"]["coins"], utxo_data["value"]["assets"])
            utxo = Utxo(value, utxo_data["datum_hash"], utxo_data["datum_type"])
            return utxo
        except KeyError as e:
            print(f"KeyError: {e}")
            raise KupoRequestError # pass error data

class KupoRequestError(Exception):
    pass