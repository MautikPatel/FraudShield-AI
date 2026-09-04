"""
Fraud Detection Rules Configuration
"""

# -------------------------
# Amount Rules
# -------------------------

HIGH_AMOUNT_THRESHOLD = 3000

VERY_HIGH_AMOUNT_THRESHOLD = 6000


# -------------------------
# Country Rules
# -------------------------

HIGH_RISK_COUNTRIES = [
    "Russia",
    "North Korea",
    "Iran",
]


# -------------------------
# Merchant Rules
# -------------------------

HIGH_RISK_MERCHANTS = [
    "Electronics",
    "Luxury",
]


# -------------------------
# Time Rules
# -------------------------

NIGHT_START = 23
NIGHT_END = 5


# -------------------------
# Risk Thresholds
# -------------------------

REVIEW_THRESHOLD = 40

BLOCK_THRESHOLD = 80

MAX_RISK_SCORE = 100