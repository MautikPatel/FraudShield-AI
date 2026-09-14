"""
Hybrid Risk Aggregator

Combines deterministic Rule Engine risk scoring
with machine-learning fraud probability.
"""

from app.services.ml.predict import predict_fraud
from app.services.rule_engine import RuleEngine

from configs.rules import (
    REVIEW_THRESHOLD,
    BLOCK_THRESHOLD,
    MAX_RISK_SCORE,
)


# --------------------------------------------------
# Hybrid Configuration
# --------------------------------------------------

RULE_WEIGHT = 0.40
ML_WEIGHT = 0.60


# --------------------------------------------------
# Hybrid Risk Calculation
# --------------------------------------------------

def calculate_hybrid_risk(transaction: dict):
    """
    Calculate the final hybrid risk score by combining
    Rule Engine risk and ML fraud probability.
    """

    # ----------------------------------------------
    # Rule Engine
    # ----------------------------------------------

    rule_engine = RuleEngine()

    rule_result = rule_engine.evaluate(
        transaction
    )

    rule_risk_score = rule_result["risk_score"]

    # ----------------------------------------------
    # ML Model
    # ----------------------------------------------

    ml_result = predict_fraud(
        transaction
    )

    ml_fraud_probability = (
        ml_result["fraud_probability"]
    )

    ml_risk_score = (
        ml_fraud_probability * 100
    )

    # ----------------------------------------------
    # Hybrid Score
    # ----------------------------------------------

    hybrid_score = (
        rule_risk_score * RULE_WEIGHT
        +
        ml_risk_score * ML_WEIGHT
    )

    hybrid_score = min(
        hybrid_score,
        MAX_RISK_SCORE,
    )

    hybrid_score = round(
        hybrid_score,
        2,
    )

    # ----------------------------------------------
    # Final Decision
    # ----------------------------------------------

    if hybrid_score >= BLOCK_THRESHOLD:

        final_decision = "BLOCKED"

    elif hybrid_score >= REVIEW_THRESHOLD:

        final_decision = "REVIEW"

    else:

        final_decision = "APPROVED"

    # ----------------------------------------------
    # Return Result
    # ----------------------------------------------

    return {
        "rule_risk_score": rule_risk_score,
        "ml_fraud_probability": round(
            ml_fraud_probability,
            4,
        ),
        "ml_risk_score": round(
            ml_risk_score,
            2,
        ),
        "hybrid_risk_score": hybrid_score,
        "final_decision": final_decision,
        "rule_reasons": rule_result["reasons"],
        "ml_prediction": ml_result[
            "ml_prediction"
        ],
        "model_name": ml_result[
            "model_name"
        ],
    }