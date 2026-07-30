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
    ("Apple", "Electronics"),
    ("Netflix", "Entertainment"),
    ("Uber", "Transportation"),
    ("Starbucks", "Food"),
    ("Shell", "Fuel"),
    ("Best Buy", "Electronics"),
    ("Airbnb", "Travel"),
    ("McDonald's", "Food"),
]

COUNTRIES = [
    ("USA", "New York"),
    ("USA", "Chicago"),
    ("Canada", "Toronto"),
    ("India", "Mumbai"),
    ("India", "Bangalore"),
    ("UK", "London"),
    ("Germany", "Berlin"),
    ("Singapore", "Singapore"),
]

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Wallet",
]


def generate_transaction():
    """Generate one realistic transaction."""

    merchant_name, merchant_category = random.choice(MERCHANTS)
    country, city = random.choice(COUNTRIES)

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "merchant_id": f"MER{random.randint(100,999)}",
        "merchant_name": merchant_name,
        "merchant_category": merchant_category,
        "amount": Decimal(str(round(random.uniform(5, 5000), 2))),
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