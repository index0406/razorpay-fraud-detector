# Razorpay AI Risk Manager

### Hybrid Machine Learning + Behavioral Fraud Detection System

Razorpay AI Risk Manager is an end-to-end fraud detection application designed to evaluate payment transactions using a combination of **machine learning predictions** and **explainable behavioral risk rules**.

The system analyzes transaction attributes, generates an AI-based fraud probability, calculates behavioral risk signals, combines both scores into a hybrid risk score, and produces an automated **APPROVE / REVIEW / BLOCK** decision.

The dashboard is fully data-driven using the project's synthetic transaction dataset and trained Random Forest model.

---

## 🚀 Project Overview

Modern payment systems need to identify suspicious transactions quickly while minimizing false positives.

This project implements a hybrid fraud detection architecture:

```text
Transaction
     │
     ▼
Feature Processing
     │
     ├───────────────┐
     ▼               ▼
Random Forest    Behavioral
ML Model         Risk Engine
     │               │
     │               │
     └───────┬───────┘
             ▼
      Hybrid Risk Score
             │
             ▼
      Risk Classification
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
    APPROVE REVIEW BLOCK
```

The hybrid score combines:

```text
60% Machine Learning Risk
+
40% Behavioral Risk
=
Final Hybrid Risk Score
```

---

## ✨ Key Features

### Machine Learning Fraud Detection

The project uses a **Random Forest Classifier** with:

* 300 estimators
* Maximum depth of 12
* Minimum samples per leaf of 3
* Balanced class weights
* Fixed random state for reproducibility

The model predicts:

* Fraud / non-fraud
* Fraud probability
* Model risk score

---

### Explainable Behavioral Risk Engine

In addition to the ML model, the system evaluates transaction behavior using explainable rules.

Risk signals include:

* Very high transaction amount
* Location mismatch
* Previous fraud history
* High transaction velocity
* Extreme daily transaction volume
* New account
* Unusual transaction time
* International transaction

Each detected signal contributes to a behavioral risk score between **0 and 100**.

---

### Hybrid Risk Decision

The final risk score is calculated as:

```text
Hybrid Risk Score
=
(ML Fraud Probability × 0.60)
+
(Behavioral Risk Score × 0.40)
```

Risk levels:

|    Score | Risk Level | Decision |
| -------: | ---------- | -------- |
|  0–29.99 | LOW        | APPROVE  |
| 30–69.99 | MEDIUM     | REVIEW   |
|   70–100 | HIGH       | BLOCK    |

---

## 📊 Data-Driven Dashboard

The dashboard is connected directly to:

```text
data/synthetic_transactions.csv
```

Rather than using hard-coded demo values, the dashboard calculates its analytics dynamically.

### KPI Metrics

* Transactions analyzed
* Fraud rate
* Fraud cases
* Blocked transaction value
* Number of blocked transactions
* Model accuracy

### Risk Analytics

* Hourly risk activity
* Average hybrid risk by transaction hour
* Transaction activity by hour
* Approve / Review / Block distribution
* Top behavioral risk factors

### Model Performance

The dashboard exposes:

* Accuracy
* ROC-AUC
* PR-AUC
* Precision
* Recall
* F1 Score

---

## 🧠 Machine Learning Features

The Random Forest model uses the following transaction features:

| Feature                     | Description                                           |
| --------------------------- | ----------------------------------------------------- |
| `amount`                    | Transaction amount                                    |
| `location_match`            | Whether transaction location matches expected profile |
| `previous_fraud`            | Previous fraud history                                |
| `payment_method_encoded`    | Encoded payment method                                |
| `device_type_encoded`       | Encoded device type                                   |
| `transactions_last_1h`      | Transactions in previous hour                         |
| `transactions_last_24h`     | Transactions in previous 24 hours                     |
| `transaction_hour`          | Hour of transaction                                   |
| `merchant_category_encoded` | Encoded merchant category                             |
| `account_age_days`          | Age of customer account                               |
| `is_international`          | International transaction indicator                   |

---

## 🗂️ Project Structure

```text
razorpay-ai-risk-manager/
│
├── app.py
│
├── data/
│   ├── synthetic_transactions.csv
│   └── test_data.py
│
├── models/
│   ├── fraud_classifier.py
│   └── fraud_model.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ How the System Works

### 1. Dataset Generation

If the transaction dataset does not exist, the application generates it automatically using:

```text
data/test_data.py
```

The dataset contains transaction information such as amount, payment method, device, transaction velocity, account age, and fraud labels.

---

### 2. Model Training

When the application starts, the Random Forest classifier loads:

```text
data/synthetic_transactions.csv
```

The categorical variables are encoded and the dataset is split into:

```text
80% Training
20% Testing
```

The split uses stratification to preserve the fraud/non-fraud class distribution.

---

### 3. Model Evaluation

The trained model is evaluated using:

```text
Accuracy
ROC-AUC
PR-AUC
Precision
Recall
F1 Score
Confusion Matrix
```

Feature importance is also calculated to understand which transaction attributes contribute most to model predictions.

---

### 4. Transaction Risk Analysis

When a transaction is submitted through the dashboard:

```text
Frontend
   │
   ▼
POST /api/v1/risk-score
   │
   ▼
Random Forest Prediction
   │
   ▼
Behavioral Risk Engine
   │
   ▼
Hybrid Risk Score
   │
   ▼
Risk Level
   │
   ▼
APPROVE / REVIEW / BLOCK
```

The response also contains explainable risk factors.

---

## 🔌 API Endpoints

### Health Check

```http
GET /api/v1/health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "Razorpay AI Risk Manager",
  "risk_engine": "Hybrid ML + Behavioral Rules",
  "model_version": "v2.0"
}
```

---

### Risk Score

```http
POST /api/v1/risk-score
```

Example request:

```json
{
  "transaction_id": "TXN_20260905_001",
  "amount": 5000,
  "location_match": true,
  "previous_fraud": false,
  "payment_method": "upi",
  "device_type": "mobile",
  "transactions_last_1h": 2,
  "transactions_last_24h": 8,
  "transaction_hour": 14,
  "merchant_category": "Electronics",
  "account_age_days": 365,
  "is_international": false
}
```

Example response:

```json
{
  "transaction_id": "TXN_20260905_001",
  "risk_score": 18.42,
  "risk_level": "LOW",
  "fraud_probability": 0.0834,
  "ml_risk_score": 8.34,
  "behavioral_risk_score": 33,
  "recommendation": "APPROVE",
  "risk_factors": [],
  "model_prediction": 0,
  "model_version": "v2.0",
  "risk_engine": "Hybrid ML + Behavioral Rules"
}
```

---

### Dashboard Metrics

```http
GET /api/v1/dashboard-metrics
```

This endpoint dynamically calculates:

```text
Transactions analyzed
Fraud count
Fraud rate
Blocked value
Approve / Review / Block distribution
Hourly risk activity
Risk factors
Model metrics
Feature importance
```

This makes the dashboard reflect the actual dataset and model instead of static placeholder values.

---

## 🖥️ Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/razorpay-ai-risk-manager.git

cd razorpay-ai-risk-manager
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Recommended `requirements.txt`:

```text
Flask
pandas
scikit-learn
joblib
numpy
```

---

### 4. Run the application

```bash
python app.py
```

The application starts on:

```text
http://127.0.0.1:5000
```

Open the URL in your browser to access the dashboard.

---

## 🧪 Example Risk Scenarios

### Low Risk

```text
Amount: ₹5,000
Location Match: Yes
Previous Fraud: No
Velocity: Low
Account Age: 365 days
International: No
```

Expected result:

```text
LOW RISK
APPROVE
```

---

### Medium Risk

```text
Amount: ₹25,000
Location Match: No
Previous Fraud: No
Transactions Last 1h: 5
Account Age: 20 days
International: Yes
```

Possible result:

```text
MEDIUM RISK
REVIEW
```

---

### High Risk

```text
Amount: ₹1,20,000
Location Match: No
Previous Fraud: Yes
Transactions Last 1h: 12
Transactions Last 24h: 50
Account Age: 3 days
International: Yes
```

Expected result:

```text
HIGH RISK
BLOCK
```

---

## 📈 Model Explainability

The system provides two complementary explanations.

### ML Signal

The Random Forest generates a fraud probability:

```text
Fraud Probability = 0–100%
```

### Behavioral Signal

The rules engine identifies specific transaction behaviors:

```text
Previous Fraud History
Location Mismatch
High Transaction Velocity
Unusual Transaction Time
High Transaction Amount
New Account
International Transaction
```

This combination makes the system more interpretable than relying only on a black-box prediction.

---

## 🛠️ Technology Stack

### Backend

```text
Python
Flask
Pandas
Scikit-learn
Joblib
```

### Machine Learning

```text
Random Forest
Classification
Feature Encoding
Train/Test Split
ROC-AUC
PR-AUC
Precision
Recall
F1 Score
```

### Frontend

```text
HTML5
CSS3
JavaScript
SVG
Responsive UI
REST API
```

### Data

```text
Synthetic Transaction Dataset
CSV
```

---

## 🔐 Design Considerations

This project is intended as a **fraud detection prototype / portfolio project** using synthetic transaction data.

For a production payment system, additional capabilities would be required, including:

* Real-time streaming transaction ingestion
* Model monitoring
* Data drift detection
* Threshold optimization
* Online learning
* Customer-level behavioral history
* Feature store integration
* Authentication and authorization
* Audit logging
* Model version management
* Human review workflows
* Production-grade observability

---

## 🔮 Future Enhancements

Potential future improvements include:

```text
Real-time transaction streaming
        ↓
Advanced behavioral profiling
        ↓
Gradient Boosting / XGBoost
        ↓
Anomaly Detection
        ↓
Model Explainability with SHAP
        ↓
Real-time alerting
        ↓
Fraud investigation workflow
```

Additional dashboard enhancements could include:

* Transaction explorer
* Fraud investigation page
* Model drift monitoring
* Feature importance visualization
* Confusion matrix visualization
* ROC and Precision-Recall curves
* Date-range filtering
* Merchant-level fraud analytics
* Payment-method fraud analytics
* Device-risk analytics

---

## 🎯 Project Objective

The primary objective of Razorpay AI Risk Manager is to demonstrate how **machine learning and explainable behavioral intelligence can work together to detect suspicious payment transactions and support automated risk decisions**.

The project combines:

```text
Machine Learning
        +
Behavioral Intelligence
        +
Explainability
        +
Real-Time API
        +
Data-Driven Dashboard
```

to create a complete fraud detection workflow.

---

## 👨‍💻 Author

**Snehal Jadhav**

Computer Engineering | AI/ML | Data Analytics | Python

---

## ⭐ Project Highlights

```text
✓ End-to-end ML fraud detection
✓ Random Forest classifier
✓ Hybrid ML + rule-based risk engine
✓ Explainable risk factors
✓ REST API
✓ Real-time transaction analysis
✓ Data-driven analytics dashboard
✓ Model performance monitoring
✓ Automated APPROVE / REVIEW / BLOCK decisions
✓ Responsive frontend
```

---

## 📄 License

This project is intended for educational, demonstration, and portfolio purposes.
