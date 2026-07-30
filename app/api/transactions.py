"""
Transaction API

Endpoints for transaction operations.
"""

from fastapi import APIRouter

from app.services.transaction_generator import generate_transaction
from app.services.transaction_service import save_transaction

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("/generate")
def generate_one_transaction():
    """
    Generate one transaction and save it to PostgreSQL.
    """

    transaction = generate_transaction()

    saved = save_transaction(transaction)

    return {
        "message": "Transaction created successfully",
        "id": saved.id,
        "transaction_id": saved.transaction_id,
        "merchant": saved.merchant_name,
        "amount": float(saved.amount),
        "status": saved.fraud_status,
    }