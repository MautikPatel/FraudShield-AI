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


def save_transactions(transaction_list: list):
    """
    Save multiple transactions to PostgreSQL.
    """

    db = SessionLocal()

    try:
        transactions = [
            Transaction(**transaction)
            for transaction in transaction_list
        ]

        db.add_all(transactions)
        db.commit()

        return len(transactions)

    finally:
        db.close()


def get_transactions(limit: int = 100):
    """
    Return the latest transactions.
    """

    db = SessionLocal()

    try:
        return (
            db.query(Transaction)
            .order_by(Transaction.id.desc())
            .limit(limit)
            .all()
        )

    finally:
        db.close()


def get_transaction_by_id(transaction_id: str):
    """
    Return a single transaction by transaction ID.
    """

    db = SessionLocal()

    try:
        return (
            db.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )

    finally:
        db.close()