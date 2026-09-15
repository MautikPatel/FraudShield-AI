"""
Fraud Decision Explainability

Creates a human-readable explanation of the
hybrid fraud decision.
"""


def generate_decision_explanation(
    hybrid_result: dict,
):
    """
    Generate a human-readable explanation from
    the hybrid risk engine result.

    This explains the decision logic and signals.
    It does not claim model-level feature explainability.
    """

    final_decision = hybrid_result[
        "final_decision"
    ]

    final_risk_score = hybrid_result[
        "final_risk_score"
    ]

    rule_reasons = hybrid_result[
        "rule_reasons"
    ]

    ml_probability = hybrid_result[
        "ml_fraud_probability"
    ]

    ml_prediction = hybrid_result[
        "ml_prediction"
    ]

    rule_decision = hybrid_result[
        "rule_decision"
    ]

    weighted_score = hybrid_result[
        "weighted_hybrid_score"
    ]

    # ----------------------------------------------
    # Summary
    # ----------------------------------------------

    if final_decision == "BLOCKED":

        summary = (
            "Transaction blocked due to high fraud risk."
        )

    elif final_decision == "REVIEW":

        summary = (
            "Transaction requires manual review "
            "due to elevated fraud risk."
        )

    else:

        summary = (
            "Transaction approved with low fraud risk."
        )

    # ----------------------------------------------
    # Decision Basis
    # ----------------------------------------------

    if rule_decision == "BLOCKED":

        decision_basis = (
            "Deterministic block rule triggered."
        )

    elif weighted_score >= 80:

        decision_basis = (
            "Hybrid risk score exceeded the "
            "block threshold."
        )

    elif weighted_score >= 40:

        decision_basis = (
            "Hybrid risk score exceeded the "
            "review threshold."
        )

    else:

        decision_basis = (
            "Hybrid risk score remained below "
            "the review threshold."
        )

    # ----------------------------------------------
    # ML Signal
    # ----------------------------------------------

    ml_signal = (
        f"{ml_probability * 100:.2f}% fraud probability "
        f"({ml_prediction})"
    )

    # ----------------------------------------------
    # Return Explanation
    # ----------------------------------------------

    return {
        "summary": summary,
        "rule_signals": rule_reasons,
        "ml_signal": ml_signal,
        "decision_basis": decision_basis,
        "final_risk_score": final_risk_score,
        "final_decision": final_decision,
    }