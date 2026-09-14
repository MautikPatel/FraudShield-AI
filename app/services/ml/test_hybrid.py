"""
Quick test for the Hybrid Rule + ML risk engine.
"""

from app.services.transaction_generator import (
    generate_normal_transaction,
    generate_fraud_transaction,
)

from app.services.ml.hybrid_risk import (
    calculate_hybrid_risk,
)


def print_result(
    transaction,
    result,
    title,
):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    print(
        f"Amount: ${transaction['amount']}"
    )

    print(
        f"Country: {transaction['country']}"
    )

    print(
        f"Merchant: "
        f"{transaction['merchant_category']}"
    )

    print()

    print(
        f"Rule Risk Score: "
        f"{result['rule_risk_score']}"
    )

    print(
        f"ML Fraud Probability: "
        f"{result['ml_fraud_probability'] * 100:.2f}%"
    )

    print(
        f"ML Risk Score: "
        f"{result['ml_risk_score']}"
    )

    print(
        f"Hybrid Risk Score: "
        f"{result['hybrid_risk_score']}"
    )

    print(
        f"Final Decision: "
        f"{result['final_decision']}"
    )

    print(
        f"Rule Reasons: "
        f"{result['rule_reasons']}"
    )


def main():

    # ----------------------------------------------
    # Normal Transaction
    # ----------------------------------------------

    normal_transaction = (
        generate_normal_transaction()
    )

    normal_result = calculate_hybrid_risk(
        normal_transaction
    )

    print_result(
        normal_transaction,
        normal_result,
        "NORMAL TRANSACTION",
    )

    # ----------------------------------------------
    # Fraud Transaction
    # ----------------------------------------------

    fraud_transaction = (
        generate_fraud_transaction()
    )

    fraud_result = calculate_hybrid_risk(
        fraud_transaction
    )

    print_result(
        fraud_transaction,
        fraud_result,
        "FRAUD TRANSACTION",
    )


if __name__ == "__main__":
    main()