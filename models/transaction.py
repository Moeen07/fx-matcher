from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    transaction_id: str
    date: datetime
    amount: float
    currency: str
    type: str  # SPEND or RECEIVE...Should make an Enum later!
    reference: str
    account_name: str
