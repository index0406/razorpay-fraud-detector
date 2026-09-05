# Flask API for fraud detection

from flask import Flask, request, jsonify, render_template
from models.fraud_classifier import FraudClassifier
import os

app = Flask(__name__)

# Initialize model
print("Initializing Fraud Classifier...")
fraud_classifier = FraudClassifier()
fraud_classifier.train()
print("Model loaded successfully!")

@app.route('/')
def home():
    """Home page with interactive form"""
    return render_template('index.html')

@app.route('/api/v1/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': fraud_classifier.is_trained,
        'service': 'Razorpay Fraud Detector'
    })

@app.route('/api/v1/risk-score', methods=['POST'])
def risk_score():
    """
    Calculate transaction risk score
    
    Input JSON:
    {
        "transaction_id": "TXN123456",
        "amount": 5000,
        "location_match": false,
        "previous_fraud": 1,
        "payment_method": "upi",
        "device_type": "mobile"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features
        fraud_features = [
            data.get('amount', 0),
            data.get('location_match', True),
            data.get('previous_fraud', 0),
            data.get('payment_method', 'card'),
            data.get('device_type', 'desktop')
        ]
        
        # Get fraud prediction
        fraud_pred, fraud_prob = fraud_classifier.predict(fraud_features)
        
        # Calculate risk score (70% weight on fraud probability)
        risk_score = fraud_prob * 0.7
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = 'LOW'
            recommendation = 'APPROVE'
        elif risk_score < 0.6:
            risk_level = 'MEDIUM'
            recommendation = 'REVIEW'
        else:
            risk_level = 'HIGH'
            recommendation = 'BLOCK'
        
        response = {
            'transaction_id': data.get('transaction_id', 'UNKNOWN'),
            'risk_score': round(risk_score, 3),
            'risk_level': risk_level,
            'fraud_probability': round(fraud_prob, 3),
            'recommendation': recommendation,
            'model_version': 'v1.0'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500

if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"Razorpay Fraud Detector API")
    print(f"{'='*60}")
    print(f"Starting server...")
    
    # For Render deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
