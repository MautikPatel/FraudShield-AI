"""
Fraud Model Prediction

Loads the trained FraudShield AI model and generates
a fraud probability for a transaction.
"""

from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# Model Path
# --------------------------------------------------

MODEL_PATH = Path(
    "artifacts/fraud_model.joblib"
)


# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------

def load_model():
    """
    Load the trained fraud model package.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_PATH}"
        )

    model_package = joblib.load(MODEL_PATH)

    return model_package


# --------------------------------------------------
# Prepare Transaction
# --------------------------------------------------

def prepare_transaction(transaction: dict, feature_columns: list):
    """
    Convert a transaction into the same feature structure
    used during model training.
    """

    transaction_time = transaction["transaction_time"]

    hour = transaction_time.hour

    row = {
        "amount": float(transaction["amount"]),
        "transaction_hour": hour,
        "is_night_transaction": int(
            hour >= 23 or hour < 5
        ),
    }

    # ----------------------------------------------
    # One-hot encoded categorical features
    # ----------------------------------------------

    categorical_values = {
        "merchant_category": transaction["merchant_category"],
        "payment_method": transaction["payment_method"],
        "country": transaction["country"],
        "city": transaction["city"],
    }

    for column, value in categorical_values.items():

        feature_name = f"{column}_{value}"

        if feature_name in feature_columns:
            row[feature_name] = 1

    # ----------------------------------------------
    # Add missing one-hot columns as zero
    # ----------------------------------------------

    for feature in feature_columns:

        if feature not in row:
            row[feature] = 0

    # ----------------------------------------------
    # Preserve exact training feature order
    # ----------------------------------------------

    return pd.DataFrame(
        [row],
        columns=feature_columns,
    )


# --------------------------------------------------
# Predict Fraud
# --------------------------------------------------

def predict_fraud(transaction: dict):
    """
    Generate fraud probability and prediction
    for a single transaction.
    """

    model_package = load_model()

    model = model_package["model"]
    feature_columns = model_package["features"]
    model_name = model_package["model_name"]

    features = prepare_transaction(
        transaction,
        feature_columns,
    )

    fraud_probability = model.predict_proba(
        features
    )[0][1]

    prediction = int(
        fraud_probability >= 0.5
    )

    return {
        "model_name": model_name,
        "fraud_probability": round(
            float(fraud_probability),
            4,
        ),
        "fraud_probability_percent": round(
            float(fraud_probability) * 100,
            2,
        ),
        "ml_prediction": (
            "FRAUD"
            if prediction == 1
            else "NOT_FRAUD"
        ),
    }