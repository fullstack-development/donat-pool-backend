from .serialization import get_thread_token, ValueException
from dataclasses import dataclass
from pycardano import PlutusData, TransactionInput, RawPlutusData
from datetime import datetime
from pycardano.address import Address
from pycardano.serialization import CBORSerializable
from typing import Dict, List, Union
from pycardano.serialization import IndefiniteList
from pycardano.hash import *

class Value:
    def __init__(self, coins, assets):
        self.coins = coins
        self.assets = assets

    def get_utxo_thread_token(self):
        try:
            return get_thread_token(self.assets)
        except ValueException as e:
            print(e)
            return None

class Utxo:
    def __init__(self, value: Value, datum_hash, datum_type):
        self.value = value
        self.datum_hash = datum_hash
        self.datum_type = datum_type

class FundraisingInfo:
    def __init__(self, title, goal, raisedAmt, deadline, threadTokenCurrency, threadTokenName, isCompleted):
        # self.creator = creator #
        self.title = title #
        self.goal = goal #
        self.raisedAmt = raisedAmt #
        self.deadline = deadline #
        self.threadTokenCurrency = threadTokenCurrency
        self.threadTokenName = threadTokenName
        self.isCompleted = isCompleted
