"""
Quick ML prediction test.
"""

from app.services.transaction_generator import (
    generate_normal_transaction,
    generate_fraud_transaction,
)

from app.services.ml.predict import predict_fraud


def main():

    # ----------------------------------------------
    # Test Normal Transaction
    # ----------------------------------------------

    normal_transaction = generate_normal_transaction()

    normal_result = predict_fraud(
        normal_transaction
    )

    print()
    print("=" * 60)
    print("NORMAL TRANSACTION")
    print("=" * 60)

    print(
        f"Amount: ${normal_transaction['amount']}"
    )

    print(
        f"Country: {normal_transaction['country']}"
    )

    print(
        f"Merchant: {normal_transaction['merchant_category']}"
    )

    print(
        f"ML Probability: "
        f"{normal_result['fraud_probability_percent']}%"
    )

    print(
        f"ML Prediction: "
        f"{normal_result['ml_prediction']}"
    )

    # ----------------------------------------------
    # Test Fraud Transaction
    # ----------------------------------------------

    fraud_transaction = generate_fraud_transaction()

    fraud_result = predict_fraud(
        fraud_transaction
    )

    print()
    print("=" * 60)
    print("FRAUD TRANSACTION")
    print("=" * 60)

    print(
        f"Amount: ${fraud_transaction['amount']}"
    )

    print(
        f"Country: {fraud_transaction['country']}"
    )

    print(
        f"Merchant: {fraud_transaction['merchant_category']}"
    )

    print(
        f"ML Probability: "
        f"{fraud_result['fraud_probability_percent']}%"
    )

    print(
        f"ML Prediction: "
        f"{fraud_result['ml_prediction']}"
    )


if __name__ == "__main__":
    main()