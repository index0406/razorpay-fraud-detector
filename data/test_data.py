# Generates synthetic transaction data for fraud detection
import pandas as pd
import numpy as np
import os


def generate_realistic_data(n=20000):
    """
    Generate realistic payment transaction data.

    Fraud labels are generated from correlated transaction-risk
    patterns rather than randomly.
    """

    np.random.seed(42)

    os.makedirs("data", exist_ok=True)

    payment_methods = ["upi", "card", "netbanking", "wallet"]
    devices = ["mobile", "desktop", "tablet"]
    locations = ["Pune", "Mumbai", "Delhi", "Bangalore", "Hyderabad",
                 "Chennai", "Kolkata", "Ahmedabad"]
    merchants = [
        "Electronics",
        "Grocery",
        "Travel",
        "Fashion",
        "Food",
        "Entertainment",
        "Utilities"
    ]

    # -----------------------------
    # Base transaction information
    # -----------------------------

    amount = np.random.lognormal(
        mean=np.log(800),
        sigma=1.1,
        size=n
    )

    amount = np.clip(amount, 50, 100000)

    payment_method = np.random.choice(
        payment_methods,
        n,
        p=[0.45, 0.30, 0.15, 0.10]
    )

    device_type = np.random.choice(
        devices,
        n,
        p=[0.65, 0.25, 0.10]
    )

    location = np.random.choice(
        locations,
        n
    )

    location_match = np.random.choice(
        [True, False],
        n,
        p=[0.94, 0.06]
    )

    previous_fraud = np.random.choice(
        [0, 1],
        n,
        p=[0.97, 0.03]
    )

    transactions_last_1h = np.random.poisson(
        lam=1.5,
        size=n
    )

    transactions_last_24h = np.random.poisson(
        lam=8,
        size=n
    )

    transaction_hour = np.random.randint(
        0,
        24,
        size=n
    )

    merchant_category = np.random.choice(
        merchants,
        n
    )

    account_age_days = np.random.randint(
        1,
        2000,
        size=n
    )

    is_international = np.random.choice(
        [0, 1],
        n,
        p=[0.90, 0.10]
    )

    # -------------------------------------
    # Create a fraud-risk score
    # -------------------------------------

    fraud_score = np.zeros(n)

    # High transaction amount
    fraud_score += np.where(
        amount > 10000,
        2.0,
        0
    )

    fraud_score += np.where(
        amount > 50000,
        2.0,
        0
    )

    # Location mismatch
    fraud_score += np.where(
        location_match == False,
        2.5,
        0
    )

    # Previous fraud history
    fraud_score += previous_fraud * 3.5

    # High transaction velocity
    fraud_score += np.where(
        transactions_last_1h >= 5,
        3.0,
        0
    )

    fraud_score += np.where(
        transactions_last_24h >= 20,
        2.0,
        0
    )

    # Unusual hours
    unusual_hour = (
        (transaction_hour <= 5) |
        (transaction_hour >= 23)
    )

    fraud_score += np.where(
        unusual_hour,
        1.5,
        0
    )

    # International transaction
    fraud_score += is_international * 1.5

    # New accounts are slightly riskier
    fraud_score += np.where(
        account_age_days < 30,
        1.5,
        0
    )

    # Certain payment patterns
    fraud_score += np.where(
        payment_method == "card",
        0.3,
        0
    )

    # Add some randomness so the model isn't perfect
    fraud_score += np.random.normal(
        0,
        1.0,
        n
    )

    # -------------------------------------
    # Convert risk score into fraud label
    # -------------------------------------

    # Approximately a few percent fraud,
    # much more realistic for a demo dataset
    threshold = np.percentile(
        fraud_score,
        97
    )

    is_fraud = (
        fraud_score >= threshold
    ).astype(int)

    # -------------------------------------
    # Build dataframe
    # -------------------------------------

    df = pd.DataFrame({
        "transaction_id": [
            f"TXN{i:08d}"
            for i in range(1, n + 1)
        ],
        "amount": np.round(amount, 2),
        "location": location,
        "location_match": location_match,
        "previous_fraud": previous_fraud,
        "payment_method": payment_method,
        "device_type": device_type,
        "transactions_last_1h": transactions_last_1h,
        "transactions_last_24h": transactions_last_24h,
        "transaction_hour": transaction_hour,
        "merchant_category": merchant_category,
        "account_age_days": account_age_days,
        "is_international": is_international,
        "is_fraud": is_fraud
    })

    output_path = "data/synthetic_transactions.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("=" * 60)
    print("TRANSACTION DATASET GENERATED")
    print("=" * 60)

    print(f"Total transactions : {len(df)}")
    print(f"Fraud transactions : {df['is_fraud'].sum()}")
    print(
        f"Fraud rate         : "
        f"{df['is_fraud'].mean() * 100:.2f}%"
    )

    print(f"\nSaved to: {output_path}")

    return df


if __name__ == "__main__":
    generate_realistic_data()
