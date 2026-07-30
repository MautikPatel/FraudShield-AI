"""
Transaction Service

Handles database operations for transactions.
"""

from app.database.session import SessionLocal
from app.models.transaction import Transaction


def save_transaction(transaction_data: dict):
    """
    Save a transaction to PostgreSQL.
    """

    db = SessionLocal()

    try:
        transaction = Transaction(**transaction_data)

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    finally:
        db.close()