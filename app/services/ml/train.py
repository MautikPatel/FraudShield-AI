"""
Fraud Model Training

Trains and evaluates baseline machine-learning models
for FraudShield AI.
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


# --------------------------------------------------
# File Paths
# --------------------------------------------------

DATASET_PATH = Path(
    "datasets/processed/fraud_features.csv"
)

MODEL_PATH = Path(
    "artifacts/fraud_model.joblib"
)


# --------------------------------------------------
# Training Configuration
# --------------------------------------------------

TEST_SIZE = 0.20
RANDOM_STATE = 42


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

def load_dataset():
    """
    Load the processed ML dataset.
    """

    print("Loading processed dataset...")

    df = pd.read_csv(DATASET_PATH)

    print(f"Dataset shape: {df.shape}")

    return df


# --------------------------------------------------
# Evaluate Model
# --------------------------------------------------

def evaluate_model(
    model,
    model_name,
    X_test,
    y_test,
):
    """
    Evaluate a trained model using fraud-focused metrics.
    """

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print()
    print("=" * 60)
    print(model_name)
    print("=" * 60)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print()
    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    print()
    print("Classification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Not Fraud",
                "Fraud",
            ],
            zero_division=0,
        )
    )

    return {
        "model": model,
        "model_name": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
    }


# --------------------------------------------------
# Train Models
# --------------------------------------------------

def train_models():
    """
    Train and compare Logistic Regression
    and Random Forest models.
    """

    df = load_dataset()

    # ----------------------------------------------
    # Separate Features and Target
    # ----------------------------------------------

    X = df.drop(
        columns=["fraud_label"]
    )

    y = df["fraud_label"]

    print()
    print(f"Features: {X.shape[1]}")
    print(f"Samples : {X.shape[0]}")

    # ----------------------------------------------
    # Train / Test Split
    # ----------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print()
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples : {len(X_test)}")

    # ----------------------------------------------
    # Model 1: Logistic Regression
    # ----------------------------------------------

    print()
    print("Training Logistic Regression...")

    logistic_model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
    )

    logistic_model.fit(
        X_train,
        y_train,
    )

    logistic_results = evaluate_model(
        logistic_model,
        "Logistic Regression",
        X_test,
        y_test,
    )

    # ----------------------------------------------
    # Model 2: Random Forest
    # ----------------------------------------------

    print()
    print("Training Random Forest...")

    random_forest_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
    )

    random_forest_model.fit(
        X_train,
        y_train,
    )

    random_forest_results = evaluate_model(
        random_forest_model,
        "Random Forest",
        X_test,
        y_test,
    )

    # ----------------------------------------------
    # Select Best Model
    # ----------------------------------------------

    results = [
        logistic_results,
        random_forest_results,
    ]

    best_result = max(
        results,
        key=lambda result: result["f1"],
    )

    best_model = best_result["model"]

    print()
    print("=" * 60)
    print("MODEL SELECTION")
    print("=" * 60)

    print(
        f"Selected model: {best_result['model_name']}"
    )

    print(
        f"F1 Score: {best_result['f1']:.4f}"
    )

    print(
        f"ROC-AUC: {best_result['roc_auc']:.4f}"
    )

    # ----------------------------------------------
    # Save Model
    # ----------------------------------------------

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_package = {
        "model": best_model,
        "features": list(X.columns),
        "model_name": best_result["model_name"],
    }

    joblib.dump(
        model_package,
        MODEL_PATH,
    )

    print()
    print("Model saved successfully.")
    print(f"Model path: {MODEL_PATH}")


# --------------------------------------------------
# Script Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    train_models()