from builtins import bytes
from pycardano.transaction import MultiAsset, ScriptHash, AssetName
from django.conf import settings
from pycardano import PlutusData
from dataclasses import dataclass
from pycardano.address import Address

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


class Asset:
    def __init__(self, currencySymbol, tokenName):
        self.currencySymbol = currencySymbol
        self.tokenName = tokenName

def get_thread_token(assets_dict):
    multi_asset = make_multi_asset(assets_dict)
    if not ver_token_in_assets(multi_asset): 
        raise VerTokenNotFound(assets_dict)
    cs = get_thread_token_currency(multi_asset)
    return Asset(cs, settings.THREAD_TOKEN_TN)

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
        raise ThreadTokenNotFound(assets)
    try:
        next(iterable)
        raise MultipleThreadTokensFound(assets)
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

def deserialize_datum(datum_cbor):
    return FundraisingDatum.from_cbor(datum_cbor)

def deserialize_address(addr):
    addr_cbor = addr.to_cbor_hex()
    address = Address.from_primitive(addr_cbor)
    return str(address)

class ValueException(Exception):
    def __init__(self, exception_info):
      self.exception_info = exception_info

    def __str__(self):
      return repr(self.exception_info)

class VerTokenNotFound(ValueException):
    def __init__(self, assets):
      super().__init__("Verification token is not found: " + str(assets))

class ThreadTokenNotFound(ValueException):
    def __init__(self, assets):
      super().__init__("Thread token is not found: " + str(assets))

class MultipleThreadTokensFound(ValueException):
    def __init__(self, assets):
      super().__init__("Multiple thread tokens with similar names are found: " + str(assets))
