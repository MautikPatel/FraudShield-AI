"""
Transaction Generator

Generates realistic payment transactions for testing
FraudShield AI.
"""

import random
import uuid
from decimal import Decimal
from datetime import datetime

MERCHANTS = [
    ("Amazon", "Retail"),
    ("Walmart", "Retail"),
    ("Costco", "Retail"),

    ("Apple", "Electronics"),
    ("Best Buy", "Electronics"),
    ("Samsung Store", "Electronics"),

    ("Uber", "Transportation"),
    ("Lyft", "Transportation"),

    ("Starbucks", "Food"),
    ("McDonald's", "Food"),
    ("Domino's", "Food"),

    ("Shell", "Fuel"),
    ("BP", "Fuel"),

    ("Hilton", "Travel"),
    ("Airbnb", "Travel"),
    ("Delta Airlines", "Travel"),

    ("Steam", "Gaming"),
    ("PlayStation Store", "Gaming"),

    ("CVS Pharmacy", "Pharmacy"),
    ("Walgreens", "Pharmacy"),

    ("Gucci", "Luxury"),
    ("Louis Vuitton", "Luxury"),
]

NORMAL_COUNTRIES = [
    ("USA", "New York"),
    ("USA", "Chicago"),
    ("Canada", "Toronto"),
    ("India", "Mumbai"),
    ("India", "Bangalore"),
    ("UK", "London"),
    ("Germany", "Berlin"),
    ("Singapore", "Singapore"),
]

HIGH_RISK_COUNTRIES = [
    ("Russia", "Moscow"),
    ("Iran", "Tehran"),
    ("North Korea", "Pyongyang"),
]


PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Wallet",
]

AMOUNT_RANGES = {
    "Retail": (20, 500),
    "Electronics": (300, 5000),
    "Transportation": (8, 120),
    "Food": (5, 80),
    "Fuel": (20, 150),
    "Travel": (150, 3000),
    "Gaming": (10, 200),
    "Pharmacy": (10, 250),
    "Luxury": (1000, 8000),
}


def generate_amount(category: str):
    """
    Generate a realistic amount based on merchant category.
    """

    minimum, maximum = AMOUNT_RANGES[category]

    return Decimal(
        str(round(random.uniform(minimum, maximum), 2))
    )

def generate_normal_transaction():
    """
    Generate a normal low-risk transaction.
    """

    merchant_name, merchant_category = random.choice(MERCHANTS)
    country, city = random.choice(NORMAL_COUNTRIES)

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "merchant_id": f"MER{random.randint(100,999)}",
        "merchant_name": merchant_name,
        "merchant_category": merchant_category,
        "amount": generate_amount(merchant_category),
        "currency": "USD",
        "payment_method": random.choice(PAYMENT_METHODS),
        "country": country,
        "city": city,
        "device_id": f"DEV{random.randint(100000,999999)}",
        "ip_address": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
        "risk_score": Decimal("0.00"),
        "fraud_status": "PENDING",
        "transaction_time": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }


def generate_suspicious_transaction():
    """
    Generate a medium-risk transaction.
    """

    suspicious_merchants = [
        ("Apple", "Electronics"),
        ("Best Buy", "Electronics"),
        ("Samsung Store", "Electronics"),
        ("Hilton", "Travel"),
        ("Airbnb", "Travel"),
        ("Gucci", "Luxury"),
    ]

    merchant_name, merchant_category = random.choice(suspicious_merchants)

    country, city = random.choice(NORMAL_COUNTRIES)

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "merchant_id": f"MER{random.randint(100,999)}",
        "merchant_name": merchant_name,
        "merchant_category": merchant_category,
        "amount": Decimal(str(round(random.uniform(1500, 4500), 2))),
        "currency": "USD",
        "payment_method": random.choice(PAYMENT_METHODS),
        "country": country,
        "city": city,
        "device_id": f"DEV{random.randint(100000,999999)}",
        "ip_address": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
        "risk_score": Decimal("0.00"),
        "fraud_status": "PENDING",
        "transaction_time": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

def generate_review_transaction():
    """
    Generate a borderline-risk transaction intended
    for manual review.

    The transaction is intentionally constructed with
    moderate-risk characteristics. The API validates the
    final hybrid score before saving it.
    """

    review_merchants = [
        ("Apple", "Electronics"),
        ("Best Buy", "Electronics"),
        ("Samsung Store", "Electronics"),
        ("Hilton", "Travel"),
        ("Airbnb", "Travel"),
        ("Gucci", "Luxury"),
    ]

    merchant_name, merchant_category = random.choice(
        review_merchants
    )

    country, city = random.choice(
        NORMAL_COUNTRIES
    )

    # Keep the amount in a moderate/high range.
    # The hybrid engine ultimately determines whether
    # the transaction qualifies for REVIEW.
    amount_ranges = {
        "Electronics": (3000, 4500),
        "Travel": (1500, 3000),
        "Luxury": (1500, 3500),
    }

    minimum, maximum = amount_ranges[
        merchant_category
    ]

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "merchant_id": f"MER{random.randint(100,999)}",
        "merchant_name": merchant_name,
        "merchant_category": merchant_category,
        "amount": Decimal(
            str(
                round(
                    random.uniform(
                        minimum,
                        maximum,
                    ),
                    2,
                )
            )
        ),
        "currency": "USD",
        "payment_method": random.choice(
            PAYMENT_METHODS
        ),
        "country": country,
        "city": city,
        "device_id": (
            f"DEV{random.randint(100000,999999)}"
        ),
        "ip_address": (
            f"192.168."
            f"{random.randint(1,255)}."
            f"{random.randint(1,255)}"
        ),
        "risk_score": Decimal("0.00"),
        "fraud_status": "PENDING",
        "transaction_time": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }


def generate_review_transactions(count: int):
    """
    Generate review-oriented transaction candidates.

    The API validates each candidate using the hybrid
    Rule + ML engine before saving it.
    """

    transactions = []

    for _ in range(count):
        transactions.append(
            generate_review_transaction()
        )

    return transactions

def generate_fraud_transaction():
    """
    Generate a high-risk fraudulent transaction.
    """

    fraud_merchants = [
        ("Apple", "Electronics"),
        ("Best Buy", "Electronics"),
        ("Gucci", "Luxury"),
        ("Louis Vuitton", "Luxury"),
    ]

    merchant_name, merchant_category = random.choice(fraud_merchants)

    country, city = random.choice(HIGH_RISK_COUNTRIES)

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "merchant_id": f"MER{random.randint(100,999)}",
        "merchant_name": merchant_name,
        "merchant_category": merchant_category,
        "amount": Decimal(str(round(random.uniform(3500, 9000), 2))),
        "currency": "USD",
        "payment_method": "Credit Card",
        "country": country,
        "city": city,
        "device_id": f"DEV{random.randint(100000,999999)}",
        "ip_address": f"10.10.{random.randint(1,255)}.{random.randint(1,255)}",
        "risk_score": Decimal("0.00"),
        "fraud_status": "PENDING",
        "transaction_time": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }


def generate_transaction():
    """
    Generate a realistic transaction distribution.

    94% Normal
    5% Suspicious
    1% Fraud
    """

    probability = random.random()

    if probability < 0.94:
        return generate_normal_transaction()

    elif probability < 0.99:
        return generate_suspicious_transaction()

    else:
        return generate_fraud_transaction()


def generate_transactions(count: int):
    """
    Generate multiple transactions.
    """

    transactions = []

    for _ in range(count):
        transactions.append(generate_transaction())

    return transactions

def generate_fraud_transactions(count: int):
    transactions = []

    for _ in range(count):
        transaction = generate_fraud_transaction()
        transactions.append(transaction)

    return transactions