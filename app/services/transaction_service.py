"""
Transaction Service

Handles database operations for transactions
and transaction analytics.
"""

from sqlalchemy import case, func

from app.database.session import SessionLocal
from app.models.transaction import Transaction


def save_transaction(transaction_data: dict):
    """
    Save a transaction to PostgreSQL.
    """

    db = SessionLocal()

    try:
        transaction = Transaction(
            **transaction_data
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    finally:
        db.close()


def save_transactions(
    transaction_list: list,
):
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


def get_transactions(
    limit: int = 100,
):
    """
    Return the latest transactions.
    """

    db = SessionLocal()

    try:
        return (
            db.query(Transaction)
            .order_by(
                Transaction.id.desc()
            )
            .limit(limit)
            .all()
        )

    finally:
        db.close()


def get_transaction_by_id(
    transaction_id: str,
):
    """
    Return a single transaction by
    transaction ID.
    """

    db = SessionLocal()

    try:
        return (
            db.query(Transaction)
            .filter(
                Transaction.transaction_id
                == transaction_id
            )
            .first()
        )

    finally:
        db.close()


def get_transaction_stats():
    """
    Return summary statistics for transactions.
    """

    db = SessionLocal()

    try:
        total_transactions = (
            db.query(Transaction).count()
        )

        blocked_transactions = (
            db.query(Transaction)
            .filter(
                Transaction.fraud_status
                == "BLOCKED"
            )
            .count()
        )

        review_transactions = (
            db.query(Transaction)
            .filter(
                Transaction.fraud_status
                == "REVIEW"
            )
            .count()
        )

        approved_transactions = (
            db.query(Transaction)
            .filter(
                Transaction.fraud_status
                == "APPROVED"
            )
            .count()
        )

        total_amount = (
            db.query(
                func.sum(Transaction.amount)
            ).scalar()
            or 0
        )

        average_risk_score = (
            db.query(
                func.avg(Transaction.risk_score)
            ).scalar()
            or 0
        )

        blocked_rate = (
            (
                blocked_transactions
                / total_transactions
            ) * 100
            if total_transactions > 0
            else 0
        )

        return {
            "total_transactions": total_transactions,
            "blocked_transactions": blocked_transactions,
            "review_transactions": review_transactions,
            "approved_transactions": approved_transactions,
            "blocked_rate": round(
                blocked_rate,
                2,
            ),
            "total_transaction_amount": float(
                total_amount
            ),
            "average_risk_score": round(
                float(average_risk_score),
                2,
            ),
        }

    finally:
        db.close()


def get_risk_distribution():
    """
    Return transaction distribution
    by fraud status.
    """

    db = SessionLocal()

    try:
        results = (
            db.query(
                Transaction.fraud_status,
                func.count(
                    Transaction.id
                ).label(
                    "transaction_count"
                ),
            )
            .group_by(
                Transaction.fraud_status
            )
            .all()
        )

        distribution = {
            "APPROVED": 0,
            "REVIEW": 0,
            "BLOCKED": 0,
        }

        for status, count in results:
            if status in distribution:
                distribution[status] = count

        return distribution

    finally:
        db.close()


def get_risky_countries(
    limit: int = 10,
):
    """
    Return countries ranked by
    average risk score.
    """

    db = SessionLocal()

    try:
        blocked_count = func.sum(
            case(
                (
                    Transaction.fraud_status
                    == "BLOCKED",
                    1,
                ),
                else_=0,
            )
        ).label("blocked_count")

        results = (
            db.query(
                Transaction.country,
                func.count(
                    Transaction.id
                ).label(
                    "transaction_count"
                ),
                blocked_count,
                func.avg(
                    Transaction.risk_score
                ).label(
                    "average_risk"
                ),
            )
            .group_by(
                Transaction.country
            )
            .order_by(
                func.avg(
                    Transaction.risk_score
                ).desc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "country": country,
                "transaction_count": (
                    transaction_count
                ),
                "blocked_count": int(
                    blocked_count or 0
                ),
                "average_risk": round(
                    float(
                        average_risk or 0
                    ),
                    2,
                ),
            }
            for (
                country,
                transaction_count,
                blocked_count,
                average_risk,
            ) in results
        ]

    finally:
        db.close()


def get_risky_merchant_categories(
    limit: int = 10,
):
    """
    Return merchant categories ranked by
    average risk score.
    """

    db = SessionLocal()

    try:
        blocked_count = func.sum(
            case(
                (
                    Transaction.fraud_status
                    == "BLOCKED",
                    1,
                ),
                else_=0,
            )
        ).label("blocked_count")

        results = (
            db.query(
                Transaction.merchant_category,
                func.count(
                    Transaction.id
                ).label(
                    "transaction_count"
                ),
                blocked_count,
                func.avg(
                    Transaction.risk_score
                ).label(
                    "average_risk"
                ),
            )
            .group_by(
                Transaction.merchant_category
            )
            .order_by(
                func.avg(
                    Transaction.risk_score
                ).desc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "merchant_category": (
                    merchant_category
                ),
                "transaction_count": (
                    transaction_count
                ),
                "blocked_count": int(
                    blocked_count or 0
                ),
                "average_risk": round(
                    float(
                        average_risk or 0
                    ),
                    2,
                ),
            }
            for (
                merchant_category,
                transaction_count,
                blocked_count,
                average_risk,
            ) in results
        ]

    finally:
        db.close()


def get_high_risk_transactions(
    threshold: float = 40,
    limit: int = 20,
):
    """
    Return recent transactions above
    the specified risk threshold.
    """

    db = SessionLocal()

    try:
        return (
            db.query(Transaction)
            .filter(
                Transaction.risk_score
                >= threshold
            )
            .order_by(
                Transaction.risk_score.desc(),
                Transaction.id.desc(),
            )
            .limit(limit)
            .all()
        )

    finally:
        db.close()