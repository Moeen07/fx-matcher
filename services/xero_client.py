import requests
from datetime import datetime
from typing import List
from models.transaction import Transaction
from config import (
    XERO_CLIENT_ID,
    XERO_CLIENT_SECRET,
    XERO_REFRESH_TOKEN,
    XERO_TENANT_ID,
    XERO_TOKEN_URL,
    XERO_API_BASE,
    FROM_ACCOUNT_ID,
    TO_ACCOUNT_ID
)
from utils.logger import get_logger

logger = get_logger()

def get_access_token() -> str:
    """
    Use the refresh token to get a new access token from Xero.
    """
    data = {
        "grant_type": "refresh_token",
        "refresh_token": XERO_REFRESH_TOKEN
    }
    auth = (XERO_CLIENT_ID, XERO_CLIENT_SECRET)

    response = requests.post(XERO_TOKEN_URL, data=data, auth=auth)
    response.raise_for_status()
    return response.json()["access_token"]

def get_transactions() -> List[Transaction]:
    """
    Fetch bank transactions from Xero API.
    """
    access_token = get_access_token()
    url = f"{XERO_API_BASE}/BankTransactions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "xero-tenant-id": XERO_TENANT_ID,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json().get("BankTransactions", [])

    transactions = []
    for txn in data:
        transactions.append(Transaction(
            transaction_id=txn.get("BankTransactionID"),
            date=datetime.strptime(txn.get("Date")[:10], "%Y-%m-%d"),
            amount=txn.get("Total", 0.0),
            currency=txn.get("CurrencyCode"),
            type=txn.get("Type", "").upper(),
            reference=txn.get("Reference", ""),
            account_name=txn.get("BankAccount", {}).get("Name", "")
        ))

    return transactions

def create_bank_transfer(amount: float, from_account_name: str, to_account_name: str, date: str):
    """
    Post a draft bank transfer to Xero API.
    """
    access_token = get_access_token()
    url = f"{XERO_API_BASE}/BankTransfers"

    payload = {
        "Amount": amount,
        "FromBankAccount": {"AccountID": FROM_ACCOUNT_ID},
        "ToBankAccount": {"AccountID": TO_ACCOUNT_ID},
        "Date": date
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "xero-tenant-id": XERO_TENANT_ID,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    logger.info(f"Transfer posted for amount {amount} on {date}")
