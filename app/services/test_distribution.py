from collections import Counter

from app.services.transaction_generator import generate_transaction

counter = Counter()

for _ in range(100):
    transaction = generate_transaction()

    if transaction["country"] in ["Russia", "Iran", "North Korea"]:
        counter["Fraud"] += 1
    elif transaction["amount"] >= 1500:
        counter["Suspicious"] += 1
    else:
        counter["Normal"] += 1

print(counter)