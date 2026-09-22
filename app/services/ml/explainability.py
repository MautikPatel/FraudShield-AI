"""
Fraud Decision Explainability

Creates a human-readable explanation of the
hybrid fraud decision and generates natural-language
fraud insights from the available risk signals.

This does not claim model-level feature explainability.
"""


def generate_decision_explanation(
    hybrid_result: dict,
):
    """
    Generate a human-readable explanation from
    the hybrid risk engine result.

    The explanation is generated from existing
    rule-based and ML outputs. It does not use
    an external LLM.
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
    # Risk Level
    # ----------------------------------------------

    if final_risk_score >= 80:

        risk_level = "HIGH"

    elif final_risk_score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # ----------------------------------------------
    # Headline
    # ----------------------------------------------

    if final_decision == "BLOCKED":

        headline = "High Fraud Risk"

    elif final_decision == "REVIEW":

        headline = "Elevated Fraud Risk"

    else:

        headline = "Low Fraud Risk"

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

    ml_percentage = ml_probability * 100

    ml_signal = (
        f"{ml_percentage:.2f}% fraud probability "
        f"({ml_prediction})"
    )

    # ----------------------------------------------
    # Key Signals
    # ----------------------------------------------

    key_signals = list(rule_reasons)

    if ml_prediction == "FRAUD":

        key_signals.append(
            f"ML model indicates elevated fraud probability "
            f"({ml_percentage:.2f}%)"
        )

    # ----------------------------------------------
    # Natural-Language Insight
    # ----------------------------------------------

    if final_decision == "BLOCKED":

        if rule_reasons and ml_prediction == "FRAUD":

            natural_language_insight = (
                "This transaction was blocked because "
                "multiple fraud risk signals were detected. "
                f"Rule-based checks identified: "
                f"{', '.join(rule_reasons)}. "
                f"The ML model also assigned a "
                f"{ml_percentage:.2f}% fraud probability, "
                "reinforcing the overall risk assessment."
            )

        elif rule_reasons:

            natural_language_insight = (
                "This transaction was blocked because "
                "deterministic fraud rules identified "
                f"the following risk signals: "
                f"{', '.join(rule_reasons)}."
            )

        else:

            natural_language_insight = (
                "This transaction was blocked because "
                "the overall hybrid risk score reached "
                "the block threshold."
            )

    elif final_decision == "REVIEW":

        if rule_reasons and ml_prediction == "FRAUD":

            natural_language_insight = (
                "This transaction requires manual review "
                "because multiple risk signals were detected. "
                f"Rule-based checks identified: "
                f"{', '.join(rule_reasons)}. "
                f"The ML model assigned a "
                f"{ml_percentage:.2f}% fraud probability, "
                "indicating elevated risk."
            )

        elif rule_reasons:

            natural_language_insight = (
                "This transaction requires manual review "
                "because rule-based checks identified: "
                f"{', '.join(rule_reasons)}."
            )

        else:

            natural_language_insight = (
                "This transaction requires manual review "
                "because the hybrid risk score exceeded "
                "the review threshold."
            )

    else:

        if ml_prediction == "NOT_FRAUD":

            natural_language_insight = (
                "This transaction was approved because "
                "no significant rule-based risk signals "
                "were detected and the ML model assigned "
                f"a low fraud probability of "
                f"{ml_percentage:.2f}%."
            )

        elif rule_reasons:

            natural_language_insight = (
                "This transaction was approved because "
                "the overall hybrid risk score remained "
                "below the review threshold despite "
                "the presence of some risk signals."
            )

        else:

            natural_language_insight = (
                "This transaction was approved because "
                "the overall hybrid risk score remained "
                "below the review threshold."
            )

    # ----------------------------------------------
    # Recommended Action
    # ----------------------------------------------

    if final_decision == "BLOCKED":

        recommended_action = (
            "Block transaction and investigate if required."
        )

    elif final_decision == "REVIEW":

        recommended_action = (
            "Route transaction for manual fraud review."
        )

    else:

        recommended_action = (
            "Approve transaction."
        )

    # ----------------------------------------------
    # Return Explanation
    # ----------------------------------------------

    return {
        "headline": headline,
        "risk_level": risk_level,
        "summary": summary,
        "key_signals": key_signals,
        "rule_signals": rule_reasons,
        "ml_signal": ml_signal,
        "decision_basis": decision_basis,
        "natural_language_insight": (
            natural_language_insight
        ),
        "recommended_action": (
            recommended_action
        ),
        "final_risk_score": final_risk_score,
        "final_decision": final_decision,
    }