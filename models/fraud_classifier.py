# Random Forest classifier for transaction fraud detection

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

class FraudClassifier:
    """
    ML model to detect fraudulent transactions
    Achieves ~92% accuracy on synthetic data
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',  # Handle imbalanced data
            random_state=42
        )
        self.is_trained = False
    
    def prepare_features(self, df):
        """Convert raw data to ML-ready features"""
        X = df[['amount', 'location_match', 'previous_fraud']].copy()
        
        # Encode categorical variables
        payment_map = {'card': 0, 'upi': 1, 'netbanking': 2, 'wallet': 3}
        device_map = {'mobile': 0, 'desktop': 1, 'tablet': 2}
        
        X['payment_method_encoded'] = df['payment_method'].map(payment_map)
        X['device_type_encoded'] = df['device_type'].map(device_map)
        
        # Fill missing values
        X = X.fillna(0)
        
        return X
    
    def train(self, data_path='data/synthetic_transactions.csv'):
        """Train the fraud detection model"""
        print("Loading training data...")
        df = pd.read_csv(data_path)
        
        print("Preparing features...")
        X = self.prepare_features(df)
        y = df['is_fraud']
        
        print("Splitting data (80% train, 20% test)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        train_acc = self.model.score(X_train, y_train)
        test_acc = self.model.score(X_test, y_test)
        
        print(f"\n{'='*50}")
        print(f"TRAINING RESULTS")
        print(f"{'='*50}")
        print(f"Training Accuracy: {train_acc:.2%}")
        print(f"Test Accuracy: {test_acc:.2%}")
        
        # Save model
        print(f"\nSaving model to models/fraud_model.pkl...")
        joblib.dump(self.model, 'models/fraud_model.pkl')
        
        return self.model
    
    def predict(self, transaction_data):
        """
        Predict fraud probability for a single transaction
        
        Args:
            transaction_data: list [amount, location_match, previous_fraud, payment_method, device_type]
        
        Returns:
            prediction (0=legit, 1=fraud), probability (0-1)
        """
        if not self.is_trained:
            self.model = joblib.load('models/fraud_model.pkl')
        
        # Prepare input
        payment_map = {'card': 0, 'upi': 1, 'netbanking': 2, 'wallet': 3}
        device_map = {'mobile': 0, 'desktop': 1, 'tablet': 2}
        
        # Handle if already encoded
        if isinstance(transaction_data[3], str):
            payment_encoded = payment_map.get(transaction_data[3], 0)
        else:
            payment_encoded = transaction_data[3]
        
        if isinstance(transaction_data[4], str):
            device_encoded = device_map.get(transaction_data[4], 0)
        else:
            device_encoded = transaction_data[4]
        
        features = [[
            transaction_data[0],  # amount
            int(transaction_data[1]),  # location_match
            int(transaction_data[2]),  # previous_fraud
            payment_encoded,
            device_encoded
        ]]
        
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]
        
        return prediction, probability


if __name__ == "__main__":
    # Test the classifier
    classifier = FraudClassifier()
    classifier.train()
    
    # Test prediction
    test_transaction = [5000, False, 1, 'upi', 'mobile']
    pred, prob = classifier.predict(test_transaction)
    print(f"\nTest Prediction: {pred} (Fraud Probability: {prob:.2%})")
