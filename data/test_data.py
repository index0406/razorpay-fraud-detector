# Generates synthetic transaction data for fraud detection

import pandas as pd
import numpy as np

def generate_transactions(n=500):
    """
    Generate synthetic Razorpay-like transactions
    10% fraud rate (realistic for fintech)
    """
    np.random.seed(42)  # For reproducibility
    
    data = {
        'transaction_id': [f'TXN{i:06d}' for i in range(n)],
        'amount': np.random.uniform(100, 50000, n),
        'merchant_id': np.random.choice(['M001', 'M002', 'M003', 'M004'], n),
        'customer_id': np.random.choice([f'C{i:04d}' for i in range(100)], n),
        'payment_method': np.random.choice(['card', 'upi', 'netbanking', 'wallet'], n),
        'time_of_day': np.random.choice(['morning', 'afternoon', 'evening', 'night'], n),
        'device_type': np.random.choice(['mobile', 'desktop', 'tablet'], n),
        'location_match': np.random.choice([True, False], n, p=[0.8, 0.2]),
        'previous_fraud': np.random.choice([0, 1], n, p=[0.95, 0.05]),
        'is_fraud': np.random.choice([0, 1], n, p=[0.9, 0.1])
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data/synthetic_transactions.csv', index=False)
    
    print(f"Generated {n} transactions")
    print(f"Fraud cases: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    generate_transactions()
