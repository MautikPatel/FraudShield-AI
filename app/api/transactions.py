"""
Transaction API

Endpoints for transaction operations.
"""

from fastapi import APIRouter

from app.services.transaction_generator import (
    generate_transaction,
    generate_transactions,
)

from app.services.transaction_service import (
    save_transaction,
    save_transactions,
    get_transactions,
)

from app.services.rule_engine import RuleEngine


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

rule_engine = RuleEngine()

@router.post("/generate")
def generate_one_transaction():
    """
    Generate one transaction and save it to PostgreSQL.
    """

    transaction = generate_transaction()

    result = rule_engine.evaluate(transaction)

    transaction["risk_score"] = result["risk_score"]
    transaction["fraud_status"] = result["fraud_status"]

    saved = save_transaction(transaction)

    return {
        "message": "Transaction created successfully",
        "id": saved.id,
        "transaction_id": saved.transaction_id,
        "merchant": saved.merchant_name,
        "amount": float(saved.amount),
        "risk_score": float(saved.risk_score),
        "status": saved.fraud_status,
    }


@router.post("/generate/{count}")
def generate_multiple_transactions(count: int):
    """
    Generate multiple transactions and save them to PostgreSQL.
    """

    if count <= 0:
        return {
            "message": "Count must be greater than zero."
        }

    transactions = generate_transactions(count)

    for transaction in transactions:
        result = rule_engine.evaluate(transaction)

        transaction["risk_score"] = result["risk_score"]
        transaction["fraud_status"] = result["fraud_status"]

    total = save_transactions(transactions)

    return {
        "message": f"{total} transactions generated successfully.",
        "generated": total,
    }

@router.get("/")
def get_all_transactions(limit: int = 100):
    """
    Return the latest transactions.
    """

    transactions = get_transactions(limit)

    return [
        {
            "id": transaction.id,
            "transaction_id": transaction.transaction_id,
            "customer_id": transaction.customer_id,
            "merchant_id": transaction.merchant_id,
            "merchant_name": transaction.merchant_name,
            "merchant_category": transaction.merchant_category,
            "amount": float(transaction.amount),
            "currency": transaction.currency,
            "payment_method": transaction.payment_method,
            "country": transaction.country,
            "city": transaction.city,
            "risk_score": float(transaction.risk_score),
            "fraud_status": transaction.fraud_status,
            "transaction_time": transaction.transaction_time,
        }
        for transaction in transactions
    ]