from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import json

app = Flask(__name__)

# Load the model and metadata
model_path = "models/best_model.pkl"
metadata_path = "models/model_metadata.json"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# Load metadata if available
metadata = {}
if os.path.exists(metadata_path):
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

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
            "probabilities": probability,
            "model_info": metadata
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/model_info', methods=['GET'])
def model_info():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    info = {
        "model_type": type(model).__name__,
        "n_estimators": getattr(model, 'n_estimators', 'N/A'),
        "max_depth": getattr(model, 'max_depth', 'N/A'),
        "n_features": getattr(model, 'n_features_in_', 'N/A')
    }
    
    # Add metadata if available
    if metadata:
        info.update(metadata)
    
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)