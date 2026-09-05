# ============================================================
# RAZORPAY AI RISK MANAGER
# Hybrid ML + Behavioral Risk Engine
# Data-Driven Dashboard
# ============================================================

from flask import Flask, request, jsonify, render_template
from models.fraud_classifier import FraudClassifier

import os
import pandas as pd


app = Flask(__name__)


# ============================================================
# INITIALIZE MODEL
# ============================================================

print("Initializing Fraud Classifier...")

fraud_classifier = FraudClassifier()


# ============================================================
# DATASET PATH
# ============================================================

DATA_PATH = "data/synthetic_transactions.csv"


# ============================================================
# GENERATE DATASET IF MISSING
# ============================================================

if not os.path.exists(DATA_PATH):

    print("Generating transaction dataset...")

    from data.test_data import generate_realistic_data

    generate_realistic_data()


# ============================================================
# TRAIN MODEL
# ============================================================

print("\nTraining Fraud Detection Model...")

fraud_classifier.train(
    data_path=DATA_PATH
)

print("\nModel loaded successfully!")


# ============================================================
# BOOLEAN NORMALIZER
# ============================================================

def normalize_bool(value):
    """
    Convert common CSV/API boolean representations
    into a real Python boolean.
    """

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return bool(value)

    return str(value).strip().lower() in [
        "true",
        "1",
        "yes",
        "y",
        "on"
    ]


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return render_template("index.html")


@app.route(
    "/api/v1/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status": "healthy",

        "model_loaded":
            fraud_classifier.is_trained,

        "service":
            "Razorpay AI Risk Manager",

        "risk_engine":
            "Hybrid ML + Behavioral Rules",

        "model_version":
            "v2.0"
    })


# ============================================================
# HYBRID BEHAVIORAL RISK ENGINE
# ============================================================

def calculate_behavioral_risk(data):
    """
    Calculates an explainable behavioral risk score from 0-100.
    """

    score = 0

    risk_factors = []


    # ========================================================
    # 1. TRANSACTION AMOUNT
    # ========================================================

    amount = float(
        data["amount"]
    )

    if amount >= 100000:

        score += 20

        risk_factors.append({

            "name":
                "Very high transaction amount",

            "severity":
                "HIGH",

            "message":
                "Transaction value exceeds ?1,00,000"
        })

    elif amount >= 50000:

        score += 15

        risk_factors.append({

            "name":
                "High transaction amount",

            "severity":
                "MEDIUM",

            "message":
                "Transaction value exceeds ?50,000"
        })

    elif amount >= 10000:

        score += 8

        risk_factors.append({

            "name":
                "Elevated transaction amount",

            "severity":
                "LOW",

            "message":
                "Transaction value exceeds ?10,000"
        })


    # ========================================================
    # 2. LOCATION MISMATCH
    # ========================================================

    if not normalize_bool(
        data["location_match"]
    ):

        score += 20

        risk_factors.append({

            "name":
                "Location mismatch",

            "severity":
                "HIGH",

            "message":
                "Transaction location differs from expected location"
        })


    # ========================================================
    # 3. PREVIOUS FRAUD HISTORY
    # ========================================================

    if normalize_bool(
        data["previous_fraud"]
    ):

        score += 25

        risk_factors.append({

            "name":
                "Previous fraud history",

            "severity":
                "HIGH",

            "message":
                "Account has previously been associated with fraud"
        })


    # ========================================================
    # 4. 1-HOUR VELOCITY
    # ========================================================

    tx_1h = int(
        data["transactions_last_1h"]
    )

    if tx_1h >= 10:

        score += 20

        risk_factors.append({

            "name":
                "Extreme transaction velocity",

            "severity":
                "HIGH",

            "message":
                f"{tx_1h} transactions detected in the last hour"
        })

    elif tx_1h >= 5:

        score += 12

        risk_factors.append({

            "name":
                "High transaction velocity",

            "severity":
                "MEDIUM",

            "message":
                f"{tx_1h} transactions detected in the last hour"
        })

    elif tx_1h >= 3:

        score += 5

        risk_factors.append({

            "name":
                "Elevated transaction velocity",

            "severity":
                "LOW",

            "message":
                f"{tx_1h} transactions detected in the last hour"
        })


    # ========================================================
    # 5. 24-HOUR VELOCITY
    # ========================================================

    tx_24h = int(
        data["transactions_last_24h"]
    )

    if tx_24h >= 40:

        score += 15

        risk_factors.append({

            "name":
                "Extreme daily transaction volume",

            "severity":
                "HIGH",

            "message":
                f"{tx_24h} transactions detected in 24 hours"
        })

    elif tx_24h >= 20:

        score += 10

        risk_factors.append({

            "name":
                "High daily transaction volume",

            "severity":
                "MEDIUM",

            "message":
                f"{tx_24h} transactions detected in 24 hours"
        })


    # ========================================================
    # 6. ACCOUNT AGE
    # ========================================================

    account_age = int(
        data["account_age_days"]
    )

    if account_age <= 7:

        score += 15

        risk_factors.append({

            "name":
                "Very new account",

            "severity":
                "HIGH",

            "message":
                "Account is less than 7 days old"
        })

    elif account_age < 30:

        score += 8

        risk_factors.append({

            "name":
                "New account",

            "severity":
                "MEDIUM",

            "message":
                "Account is less than 30 days old"
        })


    # ========================================================
    # 7. UNUSUAL TRANSACTION TIME
    # ========================================================

    hour = int(
        data["transaction_hour"]
    )

    if 0 <= hour <= 5:

        score += 10

        risk_factors.append({

            "name":
                "Unusual transaction time",

            "severity":
                "MEDIUM",

            "message":
                "Transaction occurred between midnight and 5 AM"
        })


    # ========================================================
    # 8. INTERNATIONAL TRANSACTION
    # ========================================================

    if normalize_bool(
        data["is_international"]
    ):

        score += 8

        risk_factors.append({

            "name":
                "International transaction",

            "severity":
                "MEDIUM",

            "message":
                "Transaction originated from an international location"
        })


    # ========================================================
    # CAP SCORE
    # ========================================================

    score = min(
        score,
        100
    )

    return score, risk_factors


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    return "LOW"


# ============================================================
# RECOMMENDATION
# ============================================================

def get_recommendation(risk_level):

    if risk_level == "HIGH":
        return "BLOCK"

    elif risk_level == "MEDIUM":
        return "REVIEW"

    return "APPROVE"


# ============================================================
# RISK SCORE API
# ============================================================

@app.route(
    "/api/v1/risk-score",
    methods=["POST"]
)
def risk_score():

    try:

        data = request.get_json()


        # ====================================================
        # CHECK REQUEST
        # ====================================================

        if not data:

            return jsonify({

                "error":
                    "No transaction data provided"

            }), 400


        # ====================================================
        # REQUIRED FIELDS
        # ====================================================

        required_fields = [

            "amount",
            "location_match",
            "previous_fraud",
            "payment_method",
            "device_type",
            "transactions_last_1h",
            "transactions_last_24h",
            "transaction_hour",
            "merchant_category",
            "account_age_days",
            "is_international"
        ]


        missing = [

            field

            for field in required_fields

            if field not in data
        ]


        if missing:

            return jsonify({

                "error":
                    "Missing fields",

                "fields":
                    missing

            }), 400


        # ====================================================
        # NORMALIZE BOOLEANS
        # ====================================================

        data["location_match"] = normalize_bool(
            data["location_match"]
        )

        data["previous_fraud"] = normalize_bool(
            data["previous_fraud"]
        )

        data["is_international"] = normalize_bool(
            data["is_international"]
        )


        # ====================================================
        # ML MODEL
        # ====================================================

        fraud_pred, fraud_prob = (
            fraud_classifier.predict(data)
        )

        ml_score = (
            fraud_prob * 100
        )


        # ====================================================
        # BEHAVIORAL ENGINE
        # ====================================================

        behavioral_score, risk_factors = (
            calculate_behavioral_risk(data)
        )


        # ====================================================
        # HYBRID RISK SCORE
        # ====================================================
        #
        # 60% ML
        # 40% behavioral
        #
        # ====================================================

        hybrid_score = (

            (ml_score * 0.60)

            +

            (behavioral_score * 0.40)
        )


        hybrid_score = min(
            max(
                hybrid_score,
                0
            ),
            100
        )


        # ====================================================
        # ADD MODEL SIGNAL
        # ====================================================

        if fraud_prob >= 0.70:

            risk_factors.insert(

                0,

                {

                    "name":
                        "High ML fraud probability",

                    "severity":
                        "HIGH",

                    "message":
                        (
                            f"AI model estimates "
                            f"{fraud_prob * 100:.1f}% "
                            f"fraud probability"
                        )
                }
            )

        elif fraud_prob >= 0.30:

            risk_factors.insert(

                0,

                {

                    "name":
                        "Elevated ML fraud probability",

                    "severity":
                        "MEDIUM",

                    "message":
                        (
                            f"AI model estimates "
                            f"{fraud_prob * 100:.1f}% "
                            f"fraud probability"
                        )
                }
            )


        # ====================================================
        # RISK LEVEL
        # ====================================================

        risk_level = get_risk_level(
            hybrid_score
        )


        recommendation = get_recommendation(
            risk_level
        )


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "transaction_id":
                data.get(
                    "transaction_id",
                    "UNKNOWN"
                ),

            "risk_score":
                round(
                    hybrid_score,
                    2
                ),

            "risk_level":
                risk_level,

            "fraud_probability":
                round(
                    fraud_prob,
                    4
                ),

            "ml_risk_score":
                round(
                    ml_score,
                    2
                ),

            "behavioral_risk_score":
                round(
                    behavioral_score,
                    2
                ),

            "recommendation":
                recommendation,

            "risk_factors":
                risk_factors,

            "model_prediction":
                fraud_pred,

            "model_version":
                "v2.0",

            "risk_engine":
                "Hybrid ML + Behavioral Rules"
        })


    except Exception as e:

        print(
            "\nERROR:",
            str(e)
        )

        return jsonify({

            "error":
                str(e),

            "type":
                type(e).__name__

        }), 500


# ============================================================
# DATA-DRIVEN DASHBOARD METRICS
# ============================================================

@app.route(
    "/api/v1/dashboard-metrics",
    methods=["GET"]
)
def dashboard_metrics():

    try:

        # ====================================================
        # LOAD DATASET
        # ====================================================

        if not os.path.exists(DATA_PATH):

            return jsonify({

                "error":
                    "Transaction dataset not found"
            }), 404


        df = pd.read_csv(
            DATA_PATH
        )


        if df.empty:

            return jsonify({

                "error":
                    "Transaction dataset is empty"
            }), 400


        # ====================================================
        # BASIC DATASET METRICS
        # ====================================================

        total_transactions = int(
            len(df)
        )


        fraud_count = int(
            pd.to_numeric(
                df["is_fraud"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )


        fraud_rate = (

            fraud_count
            /
            total_transactions
            *
            100

            if total_transactions
            else 0
        )


        # ====================================================
        # MODEL PREDICTIONS
        # ====================================================

        X = fraud_classifier.prepare_features(
            df
        )


        predictions = (
            fraud_classifier.model.predict(
                X
            )
        )


        probabilities = (
            fraud_classifier
            .model
            .predict_proba(X)[:, 1]
        )


        # ====================================================
        # DECISION COUNTS
        # ====================================================

        decision_counts = {

            "approve": 0,

            "review": 0,

            "block": 0
        }


        # ====================================================
        # RISK LEVEL COUNTS
        # ====================================================

        risk_level_counts = {

            "LOW": 0,

            "MEDIUM": 0,

            "HIGH": 0
        }


        # ====================================================
        # BLOCKED VALUE
        # ====================================================

        blocked_value = 0.0


        # ====================================================
        # RISK FACTOR COUNTS
        # ====================================================

        factor_counts = {}


        # ====================================================
        # HOURLY ACTIVITY
        # ====================================================

        hourly_scores = {

            hour: []

            for hour in range(24)
        }


        hourly_transactions = {

            hour: 0

            for hour in range(24)
        }


        # ====================================================
        # PROCESS TRANSACTIONS
        # ====================================================

        for index, row in df.iterrows():

            transaction = row.to_dict()


            # -----------------------------------------------
            # NORMALIZE BOOLEAN VALUES
            # -----------------------------------------------

            transaction[
                "location_match"
            ] = normalize_bool(
                transaction["location_match"]
            )


            transaction[
                "previous_fraud"
            ] = normalize_bool(
                transaction["previous_fraud"]
            )


            transaction[
                "is_international"
            ] = normalize_bool(
                transaction["is_international"]
            )


            # -----------------------------------------------
            # ML SCORE
            # -----------------------------------------------

            ml_probability = float(
                probabilities[index]
            )


            ml_score = (
                ml_probability * 100
            )


            # -----------------------------------------------
            # BEHAVIORAL SCORE
            # -----------------------------------------------

            behavioral_score, factors = (
                calculate_behavioral_risk(
                    transaction
                )
            )


            # -----------------------------------------------
            # HYBRID SCORE
            # -----------------------------------------------

            hybrid_score = (

                (ml_score * 0.60)

                +

                (behavioral_score * 0.40)
            )


            hybrid_score = min(
                max(
                    hybrid_score,
                    0
                ),
                100
            )


            # -----------------------------------------------
            # RISK LEVEL
            # -----------------------------------------------

            risk_level = get_risk_level(
                hybrid_score
            )


            # -----------------------------------------------
            # DECISION
            # -----------------------------------------------

            recommendation = (
                get_recommendation(
                    risk_level
                )
            )


            decision_key = (
                recommendation.lower()
            )


            decision_counts[
                decision_key
            ] += 1


            # -----------------------------------------------
            # BLOCKED VALUE
            # -----------------------------------------------

            if recommendation == "BLOCK":

                blocked_value += float(
                    transaction["amount"]
                )


            # -----------------------------------------------
            # RISK LEVEL COUNTS
            # -----------------------------------------------

            risk_level_counts[
                risk_level
            ] += 1


            # -----------------------------------------------
            # ML RISK FACTORS
            # -----------------------------------------------

            if ml_probability >= 0.70:

                factor_name = (
                    "High ML fraud probability"
                )

                factor_counts[
                    factor_name
                ] = (

                    factor_counts.get(
                        factor_name,
                        0
                    )
                    +
                    1
                )

            elif ml_probability >= 0.30:

                factor_name = (
                    "Elevated ML fraud probability"
                )

                factor_counts[
                    factor_name
                ] = (

                    factor_counts.get(
                        factor_name,
                        0
                    )
                    +
                    1
                )


            # -----------------------------------------------
            # BEHAVIORAL FACTORS
            # -----------------------------------------------

            for factor in factors:

                factor_name = factor.get(
                    "name",
                    "Risk Signal"
                )


                factor_counts[
                    factor_name
                ] = (

                    factor_counts.get(
                        factor_name,
                        0
                    )
                    +
                    1
                )


            # -----------------------------------------------
            # HOURLY ACTIVITY
            # -----------------------------------------------

            hour = int(
                transaction[
                    "transaction_hour"
                ]
            )


            if hour in hourly_scores:

                hourly_scores[
                    hour
                ].append(
                    hybrid_score
                )


                hourly_transactions[
                    hour
                ] += 1


        # ====================================================
        # HOURLY RISK ACTIVITY
        # ====================================================

        risk_activity = []


        for hour in range(24):

            scores = (
                hourly_scores[hour]
            )


            average_risk = (

                sum(scores)
                /
                len(scores)

                if scores

                else 0
            )


            risk_activity.append({

                "hour":
                    hour,

                "transactions":
                    hourly_transactions[
                        hour
                    ],

                "average_risk":
                    round(
                        average_risk,
                        2
                    )
            })


        # ====================================================
        # TOP RISK FACTORS
        # ====================================================

        risk_factors = sorted(

            [

                {
                    "name":
                        name,

                    "count":
                        count
                }

                for name, count
                in factor_counts.items()

            ],

            key=lambda item:
                item["count"],

            reverse=True

        )[:8]


        # ====================================================
        # MODEL METRICS
        # ====================================================

        model_metrics = {

            "accuracy":
                round(
                    fraud_classifier.metrics[
                        "accuracy"
                    ] * 100,
                    2
                ),

            "roc_auc":
                round(
                    fraud_classifier.metrics[
                        "roc_auc"
                    ],
                    4
                ),

            "pr_auc":
                round(
                    fraud_classifier.metrics[
                        "pr_auc"
                    ],
                    4
                ),

            "precision":
                round(
                    fraud_classifier.metrics[
                        "precision"
                    ] * 100,
                    2
                ),

            "recall":
                round(
                    fraud_classifier.metrics[
                        "recall"
                    ] * 100,
                    2
                ),

            "f1":
                round(
                    fraud_classifier.metrics[
                        "f1"
                    ] * 100,
                    2
                )
        }


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "transactions_analyzed":
                total_transactions,

            "fraud_count":
                fraud_count,

            "fraud_rate":
                round(
                    fraud_rate,
                    2
                ),

            "blocked_value":
                round(
                    blocked_value,
                    2
                ),

            "decisions":
                decision_counts,

            "risk_levels":
                risk_level_counts,

            "risk_activity":
                risk_activity,

            "risk_factors":
                risk_factors,

            "model_metrics":
                model_metrics,

            "feature_importance":
                fraud_classifier.feature_importance,

            "model_version":
                "v2.0",

            "risk_engine":
                "Hybrid ML + Behavioral Rules"
        })


    except Exception as e:

        print(
            "\nDASHBOARD ANALYTICS ERROR:",
            str(e)
        )

        return jsonify({

            "error":
                str(e),

            "type":
                type(e).__name__

        }), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    print("\n" + "=" * 60)

    print(
        "RAZORPAY AI RISK MANAGER"
    )

    print(
        "Hybrid Fraud Detection Engine"
    )

    print("=" * 60)

    print(
        f"Server: http://127.0.0.1:{port}"
    )

    print(
        "Risk Engine: ML + Behavioral Intelligence"
    )

    print(
        "Dashboard: Data-Driven Analytics"
    )

    print("=" * 60 + "\n")


    app.run(

        debug=False,

        host="0.0.0.0",

        port=port
    )
