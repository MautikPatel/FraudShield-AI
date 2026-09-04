from app.services.transaction_generator import generate_transaction

for _ in range(5):
    print(generate_transaction())