import requests
import numpy as np
from sklearn.datasets import load_digits

def test_api(base_url="http://localhost:5000"):
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure it's running.")
        return
    
    # Test model info
    response = requests.get(f"{base_url}/model_info")
    print(f"Model info: {response.json()}")
    
    # Test prediction with sample data
    data = load_digits()
    sample_features = data.data[0].tolist()  # First sample
    
    payload = {"features": sample_features}
    response = requests.post(f"{base_url}/predict", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Prediction: {result['prediction']}")
        print(f"Probabilities: {result['probabilities'][:3]}...")  # Show first 3 probabilities
    else:
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    test_api()