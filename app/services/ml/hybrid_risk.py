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

    Deterministic BLOCK decisions are preserved as
    hard controls and cannot be overridden by ML.
    """

    # ----------------------------------------------
    # Rule Engine
    # ----------------------------------------------

    rule_engine = RuleEngine()

    rule_result = rule_engine.evaluate(
        transaction
    )

    rule_risk_score = rule_result["risk_score"]

    rule_decision = (
        "BLOCKED"
        if rule_risk_score >= BLOCK_THRESHOLD
        else (
            "REVIEW"
            if rule_risk_score >= REVIEW_THRESHOLD
            else "APPROVED"
        )
    )

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
    # Weighted Hybrid Score
    # ----------------------------------------------

    weighted_score = (
        rule_risk_score * RULE_WEIGHT
        +
        ml_risk_score * ML_WEIGHT
    )

    weighted_score = min(
        weighted_score,
        MAX_RISK_SCORE,
    )

    weighted_score = round(
        weighted_score,
        2,
    )

    # ----------------------------------------------
    # Final Decision
    # ----------------------------------------------
    #
    # A deterministic BLOCK rule is treated as a
    # hard control and cannot be overridden by ML.
    # ----------------------------------------------

    if rule_decision == "BLOCKED":

        final_decision = "BLOCKED"

    elif weighted_score >= BLOCK_THRESHOLD:

        final_decision = "BLOCKED"

    elif weighted_score >= REVIEW_THRESHOLD:

        final_decision = "REVIEW"

    else:

        final_decision = "APPROVED"

    # ----------------------------------------------
    # Final Risk Score
    # ----------------------------------------------

    if final_decision == "BLOCKED":
        final_risk_score = max(
            weighted_score,
            rule_risk_score,
        )
    else:
        final_risk_score = weighted_score

    final_risk_score = min(
        final_risk_score,
        MAX_RISK_SCORE,
    )

    final_risk_score = round(
        final_risk_score,
        2,
    )

    # ----------------------------------------------
    # Return Result
    # ----------------------------------------------

    return {
        "rule_risk_score": rule_risk_score,
        "rule_decision": rule_decision,
        "ml_fraud_probability": round(
            ml_fraud_probability,
            4,
        ),
        "ml_risk_score": round(
            ml_risk_score,
            2,
        ),
        "weighted_hybrid_score": weighted_score,
        "final_risk_score": final_risk_score,
        "final_decision": final_decision,
        "rule_reasons": rule_result["reasons"],
        "ml_prediction": ml_result[
            "ml_prediction"
        ],
        "model_name": ml_result[
            "model_name"
        ],
    }