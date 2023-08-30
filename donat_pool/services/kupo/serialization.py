from builtins import bytes
from pycardano.transaction import MultiAsset, ScriptHash, AssetName
from django.conf import settings
from pycardano import PlutusData, RawPlutusData
from datetime import datetime
from dataclasses import dataclass, field
from pycardano.address import Address
from pycardano.serialization import ArrayCBORSerializable
from typing import Iterable, List, Optional, Tuple
from pycardano.hash import TransactionId
from pycardano.key import Key

class Asset:
    def __init__(self, currencySymbol, tokenName):
        self.currencySymbol = currencySymbol
        self.tokenName = tokenName

def get_thread_token(assets_dict):
    cs = get_thread_currency_from_assets(assets_dict)
    return Asset(cs, settings.THREAD_TOKEN_TN)

def get_thread_currency_from_assets(assets_dict):
    multi_asset = make_multi_asset(assets_dict)
    if not ver_token_in_assets(multi_asset): 
        raise VerTokenNotFound
    return get_thread_token_currency(multi_asset)

def make_multi_asset(assets_dict):
    multi_asset = MultiAsset()
    for asset_key, amount_value in assets_dict.items():
        hex_cs, hex_tn = split_hex_asset(asset_key)
        asset = MultiAsset.from_primitive({bytes.fromhex(hex_cs): {bytes.fromhex(hex_tn): amount_value}})
        multi_asset = multi_asset.__add__(asset)
    return multi_asset

def ver_token_in_assets(multi_asset):
    ver_tokens = multi_asset.count(is_ver_token)
    if ver_tokens == 1:
        return True
    else: 
        return False
    
def get_thread_token_currency(multi_asset):
    assets = multi_asset.filter(have_thread_token_name)
    iterable = iter(assets)
    try:
        thread_token = next(iterable)
    except StopIteration:
        raise ThreadTokenNotFound
    try:
        next(iterable)
        raise MultipleThreadTokensFound
    except StopIteration:
        return thread_token.payload.hex()

def is_ver_token(policy_id, asset_name, amount):
    ver_policy_id = ScriptHash(bytes.fromhex(settings.VER_TOKEN_CS))
    ver_token_name = AssetName(settings.VER_TOKEN_TN)
    return policy_id == ver_policy_id and asset_name == ver_token_name and amount == 1

def have_thread_token_name(policy_id, asset_name, amount):
    thread_token_name=AssetName(settings.THREAD_TOKEN_TN)
    return asset_name == thread_token_name and amount == 1

def split_hex_asset(hex_str):
    try:
        return hex_str.split(".")
    except ValueError:
        raise

def deserialize_datum(datum):
    return FundraisingDatum.from_cbor(datum)

class ValueException(Exception):
    pass

class CantSplitHexAsset(ValueException):
    pass

class VerTokenNotFound(ValueException):
    pass

class ThreadTokenNotFound(ValueException):
    pass

class MultipleThreadTokensFound(ValueException):
    pass

@dataclass
class FundraisingDatum(PlutusData):
    CONSTR_ID = 0

    creatorPkh: bytes
    tokenOrigin: PlutusData
    frTitle: bytes
    frAmount: int
    frDeadline: int
    frFee: int
    managerAddress: PlutusData 

if __name__ == "__main__":
    datum_cbor = "d8799f581c7c7863fc6938a9007ce5b98847bdb88f4ee1f739dd022173d22931b1d8799fd8799f582029d4526ac0fc57efaa49bc4de384ecbb4bcada22d9b5ab9585867754fb265e04ff01ff5819446f6e61746520746f206665656420737472617920636174731a08f0d1801b0000018a2a48646f0ad8799fd8799f581c49d49d1715768d0b9fb498e60a7515e390c744330b91f4a1f6329afaffd8799fd8799fd8799f581c19ce8af5ab31ca45d7ab8edbd405f409be29499250ea1c4722920f60ffffffffff"
    d = FundraisingDatum.from_cbor(datum_cbor)
    print(d)
    

    # dict = {"2ad1727329f49229089c470bcabc158a2344e149499614dba10cbfac.566572696669636174696f6e546f6b656e": 1, "d803d5d21d6439c9b8834947c8ef65b9c685f2be23fc34ce1dba174a.46756e6472616973696e67546872656164546f6b656e": 1}
    # thread_token_cs = get_thread_currency_from_assets(dict)
    # print(thread_token_cs)

# TODO: deserialize using dataclass
# FundraisingDatum.from_cbor(d)

# @dataclass
# class TransactionInputDatum(PlutusData):
#     transaction_id: str
#     index: int


