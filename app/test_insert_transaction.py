"""
Test inserting one transaction into PostgreSQL.
"""

from app.services.transaction_generator import generate_transaction
from app.services.transaction_service import save_transaction


def main():
    transaction = generate_transaction()

    saved = save_transaction(transaction)

    print("\nTransaction saved successfully!\n")
    print(f"ID              : {saved.id}")
    print(f"Transaction ID  : {saved.transaction_id}")
    print(f"Merchant        : {saved.merchant_name}")
    print(f"Amount          : {saved.amount}")
    print(f"Status          : {saved.fraud_status}")


if __name__ == "__main__":
    main()