from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    accuracy_score,
)
import pandas as pd
import joblib
import os


class FraudClassifier:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )

        self.is_trained = False

        self.feature_columns = [
            "amount",
            "location_match",
            "previous_fraud",
            "payment_method_encoded",
            "device_type_encoded",
            "transactions_last_1h",
            "transactions_last_24h",
            "transaction_hour",
            "merchant_category_encoded",
            "account_age_days",
            "is_international"
        ]

        # Dashboard metrics
        self.metrics = {
            "accuracy": 0.0,
            "roc_auc": 0.0,
            "pr_auc": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0
        }

        self.feature_importance = []

        self.test_predictions = None
        self.test_probabilities = None
        self.y_test = None

    # ============================================================
    # FEATURE PREPARATION
    # ============================================================

    def prepare_features(self, df):

        X = df.copy()

        payment_map = {
            "card": 0,
            "upi": 1,
            "netbanking": 2,
            "wallet": 3
        }

        device_map = {
            "mobile": 0,
            "desktop": 1,
            "tablet": 2
        }

        merchant_map = {
            "Electronics": 0,
            "Grocery": 1,
            "Travel": 2,
            "Fashion": 3,
            "Food": 4,
            "Entertainment": 5,
            "Utilities": 6
        }

        X["payment_method_encoded"] = (
            X["payment_method"]
            .astype(str)
            .str.lower()
            .map(payment_map)
        )

        X["device_type_encoded"] = (
            X["device_type"]
            .astype(str)
            .str.lower()
            .map(device_map)
        )

        X["merchant_category_encoded"] = (
            X["merchant_category"]
            .map(merchant_map)
        )

        X["location_match"] = (
            X["location_match"]
            .apply(
                lambda value:
                1 if str(value).strip().lower()
                in ["true", "1", "yes"]
                else 0
            )
        )

        X["previous_fraud"] = (
            X["previous_fraud"]
            .apply(
                lambda value:
                1 if str(value).strip().lower()
                in ["true", "1", "yes"]
                else 0
            )
        )

        X["is_international"] = (
            X["is_international"]
            .apply(
                lambda value:
                1 if str(value).strip().lower()
                in ["true", "1", "yes"]
                else 0
            )
        )

        X = X[self.feature_columns]

        return X.fillna(0)

    # ============================================================
    # TRAIN
    # ============================================================

    def train(
        self,
        data_path="data/synthetic_transactions.csv"
    ):

        print("\nLoading training data...")

        df = pd.read_csv(data_path)

        print(f"Transactions: {len(df)}")
        print(f"Fraud cases: {df['is_fraud'].sum()}")

        X = self.prepare_features(df)
        y = df["is_fraud"].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        print("\nTraining Random Forest...")

        self.model.fit(
            X_train,
            y_train
        )

        self.is_trained = True

        predictions = self.model.predict(X_test)

        probabilities = (
            self.model
            .predict_proba(X_test)[:, 1]
        )

        # Store for dashboard
        self.test_predictions = predictions
        self.test_probabilities = probabilities
        self.y_test = y_test

        report = classification_report(
            y_test,
            predictions,
            output_dict=True,
            zero_division=0
        )

        # ========================================================
        # STORE METRICS
        # ========================================================

        self.metrics = {
            "accuracy": float(
                accuracy_score(
                    y_test,
                    predictions
                )
            ),
            "roc_auc": float(
                roc_auc_score(
                    y_test,
                    probabilities
                )
            ),
            "pr_auc": float(
                average_precision_score(
                    y_test,
                    probabilities
                )
            ),
            "precision": float(
                report["1"]["precision"]
            ),
            "recall": float(
                report["1"]["recall"]
            ),
            "f1": float(
                report["1"]["f1-score"]
            )
        }

        print("\n" + "=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)

        print(
            classification_report(
                y_test,
                predictions,
                digits=4,
                zero_division=0
            )
        )

        print(
            "Accuracy:",
            round(self.metrics["accuracy"], 4)
        )

        print(
            "ROC-AUC:",
            round(self.metrics["roc_auc"], 4)
        )

        print(
            "PR-AUC:",
            round(self.metrics["pr_auc"], 4)
        )

        print(
            "Precision:",
            round(self.metrics["precision"], 4)
        )

        print(
            "Recall:",
            round(self.metrics["recall"], 4)
        )

        print(
            "\nConfusion Matrix:"
        )

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        # ========================================================
        # FEATURE IMPORTANCE
        # ========================================================

        importance = pd.DataFrame({
            "feature": self.feature_columns,
            "importance": self.model.feature_importances_
        }).sort_values(
            "importance",
            ascending=False
        )

        self.feature_importance = [
            {
                "feature": row["feature"],
                "importance": float(row["importance"])
            }
            for _, row in importance.iterrows()
        ]

        print("\nFeature Importance:")
        print(
            importance.to_string(
                index=False
            )
        )

        # ========================================================
        # SAVE MODEL
        # ========================================================

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            self.model,
            "models/fraud_model.pkl"
        )

        print(
            "\nModel saved to "
            "models/fraud_model.pkl"
        )

        return self.model

    # ============================================================
    # PREDICT
    # ============================================================

    def predict(self, transaction_data):

        if not self.is_trained:

            self.model = joblib.load(
                "models/fraud_model.pkl"
            )

            self.is_trained = True

        payment_map = {
            "card": 0,
            "upi": 1,
            "netbanking": 2,
            "wallet": 3
        }

        device_map = {
            "mobile": 0,
            "desktop": 1,
            "tablet": 2
        }

        merchant_map = {
            "Electronics": 0,
            "Grocery": 1,
            "Travel": 2,
            "Fashion": 3,
            "Food": 4,
            "Entertainment": 5,
            "Utilities": 6
        }

        features = [[
            transaction_data["amount"],

            int(
                transaction_data["location_match"]
            ),

            int(
                transaction_data["previous_fraud"]
            ),

            payment_map.get(
                str(
                    transaction_data["payment_method"]
                ).lower(),
                0
            ),

            device_map.get(
                str(
                    transaction_data["device_type"]
                ).lower(),
                0
            ),

            transaction_data[
                "transactions_last_1h"
            ],

            transaction_data[
                "transactions_last_24h"
            ],

            transaction_data[
                "transaction_hour"
            ],

            merchant_map.get(
                transaction_data["merchant_category"],
                0
            ),

            transaction_data[
                "account_age_days"
            ],

            int(
                transaction_data["is_international"]
            )
        ]]

        prediction = self.model.predict(
            features
        )[0]

        probability = self.model.predict_proba(
            features
        )[0][1]

        return (
            int(prediction),
            float(probability)
        )
