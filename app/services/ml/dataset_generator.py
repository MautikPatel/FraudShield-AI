"""
ML Dataset Generator

Creates a controlled synthetic dataset for FraudShield AI
model training and evaluation.
"""

import csv
import random
from pathlib import Path

from app.services.transaction_generator import (
    generate_normal_transaction,
    generate_suspicious_transaction,
    generate_fraud_transaction,
)


# --------------------------------------------------
# Dataset Configuration
# --------------------------------------------------

DATASET_PATH = Path("datasets/raw/fraud_transactions.csv")

NORMAL_COUNT = 8000
SUSPICIOUS_COUNT = 1000
FRAUD_COUNT = 1000


# --------------------------------------------------
# Convert Transaction to ML Dataset Row
# --------------------------------------------------

def transaction_to_row(
    transaction: dict,
    scenario: str,
    fraud_label: int,
):
    """
    Convert a generated transaction into an ML dataset row.
    """

    transaction_time = transaction["transaction_time"]
    hour = transaction_time.hour

    return {
        "amount": float(transaction["amount"]),
        "merchant_category": transaction["merchant_category"],
        "payment_method": transaction["payment_method"],
        "country": transaction["country"],
        "city": transaction["city"],
        "transaction_hour": hour,
        "is_night_transaction": int(
            hour >= 23 or hour < 5
        ),
        "scenario": scenario,
        "fraud_label": fraud_label,
    }


# --------------------------------------------------
# Generate Dataset
# --------------------------------------------------

def generate_dataset():
    """
    Generate a controlled synthetic fraud dataset.
    """

    rows = []

    # ----------------------------------------------
    # Normal Transactions
    # ----------------------------------------------

    print("Generating normal transactions...")

    for _ in range(NORMAL_COUNT):

        transaction = generate_normal_transaction()

        rows.append(
            transaction_to_row(
                transaction,
                scenario="NORMAL",
                fraud_label=0,
            )
        )

    # ----------------------------------------------
    # Suspicious Transactions
    # ----------------------------------------------

    print("Generating suspicious transactions...")

    for _ in range(SUSPICIOUS_COUNT):

        transaction = generate_suspicious_transaction()

        rows.append(
            transaction_to_row(
                transaction,
                scenario="SUSPICIOUS",
                fraud_label=0,
            )
        )

    # ----------------------------------------------
    # Fraud Transactions
    # ----------------------------------------------

    print("Generating fraud transactions...")

    for _ in range(FRAUD_COUNT):

        transaction = generate_fraud_transaction()

        rows.append(
            transaction_to_row(
                transaction,
                scenario="FRAUD",
                fraud_label=1,
            )
        )

    # ----------------------------------------------
    # Shuffle Dataset
    # ----------------------------------------------

    random.shuffle(rows)

    # ----------------------------------------------
    # Create Output Directory
    # ----------------------------------------------

    DATASET_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ----------------------------------------------
    # Dataset Columns
    # ----------------------------------------------

    fieldnames = [
        "amount",
        "merchant_category",
        "payment_method",
        "country",
        "city",
        "transaction_hour",
        "is_night_transaction",
        "scenario",
        "fraud_label",
    ]

    # ----------------------------------------------
    # Write CSV
    # ----------------------------------------------

    with DATASET_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    # ----------------------------------------------
    # Summary
    # ----------------------------------------------

    print()
    print("Dataset generated successfully.")
    print(f"File: {DATASET_PATH}")
    print(f"Total rows: {len(rows)}")
    print(f"Normal: {NORMAL_COUNT}")
    print(f"Suspicious: {SUSPICIOUS_COUNT}")
    print(f"Fraud: {FRAUD_COUNT}")


# --------------------------------------------------
# Script Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    generate_dataset()