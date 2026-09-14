"""
Transaction API

Endpoints for transaction operations.
"""

from fastapi import APIRouter

from app.services.transaction_generator import (
    generate_transaction,
    generate_transactions,
    generate_fraud_transaction,
)

from app.services.transaction_service import (
    save_transaction,
    save_transactions,
    get_transactions,
    get_transaction_by_id,
    get_transaction_stats,
)

from app.services.ml.hybrid_risk import (
    calculate_hybrid_risk,
)


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("/generate")
def generate_one_transaction():
    """
    Generate one transaction, evaluate it using
    the hybrid Rule + ML risk engine, and save it.
    """

    transaction = generate_transaction()

    result = calculate_hybrid_risk(
        transaction
    )

    transaction["risk_score"] = result[
        "final_risk_score"
    ]

    transaction["fraud_status"] = result[
        "final_decision"
    ]

    saved = save_transaction(
        transaction
    )

    return {
        "message": "Transaction created successfully",
        "id": saved.id,
        "transaction_id": saved.transaction_id,
        "merchant": saved.merchant_name,
        "amount": float(saved.amount),
        "country": saved.country,

        "rule_risk_score": result[
            "rule_risk_score"
        ],

        "ml_fraud_probability": result[
            "ml_fraud_probability"
        ],

        "ml_risk_score": result[
            "ml_risk_score"
        ],

        "weighted_hybrid_score": result[
            "weighted_hybrid_score"
        ],

        "final_risk_score": result[
            "final_risk_score"
        ],

        "final_decision": result[
            "final_decision"
        ],

        "rule_reasons": result[
            "rule_reasons"
        ],

        "ml_prediction": result[
            "ml_prediction"
        ],

        "model_name": result[
            "model_name"
        ],
    }


@router.post("/generate/fraud")
def generate_one_fraud_transaction():
    """
    Generate a high-risk fraud transaction, evaluate it
    using the hybrid Rule + ML risk engine, and save it.
    """

    transaction = generate_fraud_transaction()

    result = calculate_hybrid_risk(
        transaction
    )

    transaction["risk_score"] = result[
        "final_risk_score"
    ]

    transaction["fraud_status"] = result[
        "final_decision"
    ]

    saved = save_transaction(
        transaction
    )

    return {
        "message": "Fraud transaction created successfully",
        "id": saved.id,
        "transaction_id": saved.transaction_id,
        "merchant": saved.merchant_name,
        "amount": float(saved.amount),
        "country": saved.country,

        "rule_risk_score": result[
            "rule_risk_score"
        ],

        "ml_fraud_probability": result[
            "ml_fraud_probability"
        ],

        "ml_risk_score": result[
            "ml_risk_score"
        ],

        "weighted_hybrid_score": result[
            "weighted_hybrid_score"
        ],

        "final_risk_score": result[
            "final_risk_score"
        ],

        "final_decision": result[
            "final_decision"
        ],

        "rule_reasons": result[
            "rule_reasons"
        ],

        "ml_prediction": result[
            "ml_prediction"
        ],

        "model_name": result[
            "model_name"
        ],
    }


@router.post("/generate/{count}")
def generate_multiple_transactions(
    count: int
):
    """
    Generate multiple transactions, evaluate each using
    the hybrid Rule + ML risk engine, and save them.
    """

    if count <= 0:
        return {
            "message": "Count must be greater than zero."
        }

    transactions = generate_transactions(
        count
    )

    for transaction in transactions:

        result = calculate_hybrid_risk(
            transaction
        )

        transaction["risk_score"] = result[
            "final_risk_score"
        ]

        transaction["fraud_status"] = result[
            "final_decision"
        ]

    total = save_transactions(
        transactions
    )

    return {
        "message": (
            f"{total} transactions generated successfully."
        ),
        "generated": total,
    }


@router.get("/")
def get_all_transactions(
    limit: int = 100
):
    """
    Return the latest transactions.
    """

    transactions = get_transactions(
        limit
    )

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
            "risk_score": float(
                transaction.risk_score
            ),
            "fraud_status": transaction.fraud_status,
            "transaction_time": transaction.transaction_time,
        }
        for transaction in transactions
    ]


@router.get("/stats")
def get_transaction_statistics():
    """
    Return transaction and fraud statistics.
    """

    return get_transaction_stats()


@router.get("/{transaction_id}")
def get_single_transaction(
    transaction_id: str
):
    """
    Return a single transaction by transaction ID.
    """

    transaction = get_transaction_by_id(
        transaction_id
    )

    if transaction is None:
        return {
            "message": "Transaction not found.",
            "transaction_id": transaction_id,
        }

    return {
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
        "risk_score": float(
            transaction.risk_score
        ),
        "fraud_status": transaction.fraud_status,
        "transaction_time": transaction.transaction_time,
    }