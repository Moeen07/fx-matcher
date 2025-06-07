import os
import csv
from datetime import datetime, timedelta
from typing import List
from models.transaction import Transaction
from utils.date_utils import parse_date
from services import xero_client
from config import CSV_DIR, MOCK_MODE

def load_csv_transactions() -> List[Transaction]:
    transactions = []

    def load_file(file_path: str):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)[3:]  # Skip metadata rows

            headers = rows[0]
            data_rows = rows[1:]

            for row in data_rows:
                if not row or not row[0].strip():
                    continue  # Skip blank rows

                # Skip rows where date is not a valid date (like totals)
                try:
                    txn_date = parse_date(row[0])
                except ValueError:
                    continue  # Skip this row if not a real date

                amount = 0.0
                try:
                    amount = float(row[5].replace(",", "")) if row[5] else 0.0
                except ValueError:
                    continue  # Skip rows with invalid amount

                txn = Transaction(
                    transaction_id="",
                    date=txn_date,
                    amount=amount,
                    currency=row[4],
                    type=row[1].upper(),
                    reference=row[3] or "",
                    account_name=row[2] or ""
                )
                transactions.append(txn)

    aud_file = os.path.join(CSV_DIR, "Airwallex AUD - Demo Data Jan to May 2025 - Airwallex AUD Transactions.csv")
    load_file(aud_file)

    usd_file = os.path.join(CSV_DIR, "Demo Data Jan May 2025 - USD AIRWALLEX.csv")
    load_file(usd_file)

    return transactions


def load_xero_transactions() -> List[Transaction]:
    """
    In real mode, fetch transactions from Xero API.
    """
    return xero_client.get_transactions()

def match_transfers(transactions: List[Transaction]) -> List[tuple]:
    """
    Matches transfers based on:
    - Opposite type (SPEND vs. RECEIVE)
    - ±1 day proximity
    - Same amount
    - Different currencies
    """
    matches = []
    used_indices = set()

    for i, txn1 in enumerate(transactions):
        if i in used_indices or txn1.type not in ["SPEND", "RECEIVE"]:
            continue

        for j, txn2 in enumerate(transactions):
            if i == j or j in used_indices:
                continue

            # Check opposite directions
            if txn1.type == txn2.type:
                continue

            # ±1 day
            if abs((txn1.date - txn2.date).days) > 1:
                continue

            # Same amount, different currency
            if txn1.amount == txn2.amount and txn1.currency != txn2.currency:
                matches.append((txn1, txn2))
                used_indices.update([i, j])
                break

    return matches

def save_matches_to_csv(matches: List[tuple]):
    with open("matched_transfers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Txn1 Date", "Txn1 Amount", "Txn1 Currency", "Txn2 Date", "Txn2 Amount", "Txn2 Currency", "Reference"])
        for txn1, txn2 in matches:
            writer.writerow([
                txn1.date.strftime("%Y-%m-%d"),
                txn1.amount,
                txn1.currency,
                txn2.date.strftime("%Y-%m-%d"),
                txn2.amount,
                txn2.currency,
                txn1.reference or txn2.reference
            ])

def post_matches_to_xero(matches: List[tuple]):
    for txn1, txn2 in matches:
        if txn1.type == "SPEND":
            from_acc, to_acc = txn1.account_name, txn2.account_name
        else:
            from_acc, to_acc = txn2.account_name, txn1.account_name

        xero_client.create_bank_transfer(
            amount=txn1.amount,
            from_account_name=from_acc,
            to_account_name=to_acc,
            date=txn1.date.strftime("%Y-%m-%d")
        )
