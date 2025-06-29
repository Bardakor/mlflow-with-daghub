from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the model
model_path = "models/best_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get data from request
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()
        
        return jsonify({
            "prediction": int(prediction),
            "probabilities": probability
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/model_info', methods=['GET'])
def model_info():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    return jsonify({
        "model_type": type(model).__name__,
        "n_estimators": getattr(model, 'n_estimators', 'N/A'),
        "max_depth": getattr(model, 'max_depth', 'N/A'),
        "n_features": getattr(model, 'n_features_in_', 'N/A')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)