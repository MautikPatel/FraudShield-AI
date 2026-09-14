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
        f"Rule Decision: "
        f"{result['rule_decision']}"
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
        f"Weighted Hybrid Score: "
        f"{result['weighted_hybrid_score']}"
    )

    print(
        f"Final Risk Score: "
        f"{result['final_risk_score']}"
    )

    print(
        f"Final Decision: "
        f"{result['final_decision']}"
    )

    print(
        f"Rule Reasons: "
        f"{result['rule_reasons']}"
    )

    print(
        f"ML Prediction: "
        f"{result['ml_prediction']}"
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