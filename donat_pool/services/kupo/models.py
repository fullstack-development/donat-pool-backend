from .serialization import get_thread_token, ValueException

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
    def __init__(self, creator, title, goal, raisedAmt, deadline, threadTokenCurrency, threadTokenName, isCompleted):
        self.creator = creator
        self.title = title
        self.goal = goal
        self.raisedAmt = raisedAmt
        self.deadline = deadline
        self.threadTokenCurrency = threadTokenCurrency
        self.threadTokenName = threadTokenName
        self.isCompleted = isCompleted
