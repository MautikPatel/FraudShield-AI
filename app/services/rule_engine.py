"""
Rule Engine

Evaluates fraud detection rules and calculates
a transaction risk score.
"""


from configs.rules import (
    HIGH_AMOUNT_THRESHOLD,
    VERY_HIGH_AMOUNT_THRESHOLD,
    HIGH_RISK_COUNTRIES,
    HIGH_RISK_MERCHANTS,
    NIGHT_START,
    NIGHT_END,
    REVIEW_THRESHOLD,
    BLOCK_THRESHOLD,
    MAX_RISK_SCORE,
)


class RuleEngine:
    """Fraud Detection Rule Engine."""

    def evaluate(self, transaction: dict):
        """
        Evaluate a transaction.

        Returns:
            risk_score
            fraud_status
            reasons
        """

        risk_score = 0
        reasons = []

        # Rule 1
        score, reason = self._high_amount_rule(transaction)
        risk_score += score
        if reason:
            reasons.append(reason)

        # Rule 2
        score, reason = self._high_risk_country_rule(transaction)
        risk_score += score
        if reason:
            reasons.append(reason)

        # Rule 3
        score, reason = self._high_risk_merchant_rule(transaction)
        risk_score += score
        if reason:
            reasons.append(reason)

        # Rule 4
        score, reason = self._night_transaction_rule(transaction)
        risk_score += score
        if reason:
            reasons.append(reason)

        risk_score = min(risk_score, MAX_RISK_SCORE)

        if risk_score >= BLOCK_THRESHOLD:
            fraud_status = "BLOCKED"
        elif risk_score >= REVIEW_THRESHOLD:
            fraud_status = "REVIEW"
        else:
            fraud_status = "APPROVED"

        return {
            "risk_score": risk_score,
            "fraud_status": fraud_status,
            "reasons": reasons,
        }

    def _high_amount_rule(self, transaction):

        amount = float(transaction["amount"])

        if amount >= VERY_HIGH_AMOUNT_THRESHOLD:
            return 50, "Very High Amount"

        if amount >= HIGH_AMOUNT_THRESHOLD:
            return 20, "High Amount"

        return 0, None

    def _high_risk_country_rule(self, transaction):

        if transaction["country"] in HIGH_RISK_COUNTRIES:
            return 40, "High Risk Country"

        return 0, None

    def _high_risk_merchant_rule(self, transaction):

        if transaction["merchant_category"] in HIGH_RISK_MERCHANTS:
            return 20, "High Risk Merchant"

        return 0, None

    def _night_transaction_rule(self, transaction):

        hour = transaction["transaction_time"].hour

        if hour >= NIGHT_START or hour < NIGHT_END:
            return 10, "Night Transaction"

        return 0, None