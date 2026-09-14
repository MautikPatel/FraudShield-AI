"""
ML Feature Engineering

Converts the raw fraud transaction dataset into
machine-learning-ready features.
"""

from pathlib import Path

import pandas as pd


# --------------------------------------------------
# File Paths
# --------------------------------------------------

RAW_DATASET_PATH = Path(
    "datasets/raw/fraud_transactions.csv"
)

PROCESSED_DATASET_PATH = Path(
    "datasets/processed/fraud_features.csv"
)


# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

def create_features():
    """
    Load the raw dataset, create ML features,
    and save the processed dataset.
    """

    print("Loading raw dataset...")

    df = pd.read_csv(RAW_DATASET_PATH)

    print(f"Raw dataset shape: {df.shape}")

    # --------------------------------------------------
    # Remove scenario from model features
    # --------------------------------------------------
    #
    # scenario is useful for dataset validation,
    # but it must NOT be used as a model feature.
    #
    # Otherwise the model could simply learn:
    # FRAUD = fraud_label 1
    #
    # This would create data leakage.
    # --------------------------------------------------

    df = df.drop(columns=["scenario"])

    # --------------------------------------------------
    # One-Hot Encode Categorical Features
    # --------------------------------------------------

    categorical_columns = [
        "merchant_category",
        "payment_method",
        "country",
        "city",
    ]

    df = pd.get_dummies(
        df,
        columns=categorical_columns,
        dtype=int,
    )

    # --------------------------------------------------
    # Ensure Output Directory Exists
    # --------------------------------------------------

    PROCESSED_DATASET_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------
    # Save Processed Dataset
    # --------------------------------------------------

    df.to_csv(
        PROCESSED_DATASET_PATH,
        index=False,
    )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print()
    print("Feature engineering completed successfully.")
    print(f"Processed dataset: {PROCESSED_DATASET_PATH}")
    print(f"Processed shape: {df.shape}")

    print()
    print("Feature columns:")

    for column in df.columns:
        print(f" - {column}")

    print()
    print("Fraud label distribution:")
    print(df["fraud_label"].value_counts())


# --------------------------------------------------
# Script Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    create_features()