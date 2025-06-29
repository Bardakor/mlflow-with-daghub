#!/usr/bin/env python3
"""
Comprehensive test script for the ML model API.
Tests all endpoints and validates the Docker container functionality.
"""

import requests
import json
import time
import numpy as np
from sklearn.datasets import load_digits

def test_api(base_url="http://localhost:5000"):
    """Test all API endpoints."""
    print(f"Testing API at {base_url}")
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Model info
    print("\n2. Testing model info endpoint...")
    try:
        response = requests.get(f"{base_url}/model_info", timeout=10)
        print(f"Status: {response.status_code}")
        model_info = response.json()
        print(f"Model info: {json.dumps(model_info, indent=2)}")
        assert response.status_code == 200
        assert "model_type" in model_info
        print("✅ Model info test passed")
    except Exception as e:
        print(f"❌ Model info test failed: {e}")
        return False
    
    # Test 3: Prediction with sample data
    print("\n3. Testing prediction endpoint...")
    try:
        # Load sample data from sklearn digits dataset
        digits = load_digits()
        sample_features = digits.data[0].tolist()  # First sample
        
        payload = {"features": sample_features}
        response = requests.post(f"{base_url}/predict", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        print(f"Status: {response.status_code}")
        prediction_result = response.json()
        print(f"Prediction: {json.dumps(prediction_result, indent=2)}")
        
        assert response.status_code == 200
        assert "prediction" in prediction_result
        assert "probabilities" in prediction_result
        assert isinstance(prediction_result["prediction"], int)
        assert len(prediction_result["probabilities"]) == 10  # 10 digit classes
        print("✅ Prediction test passed")
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        return False
    
    # Test 4: Invalid prediction request
    print("\n4. Testing invalid prediction request...")
    try:
        invalid_payload = {"features": [1, 2, 3]}  # Wrong number of features
        response = requests.post(f"{base_url}/predict", 
                               json=invalid_payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        print(f"Status: {response.status_code}")
        assert response.status_code == 400
        print("✅ Invalid request test passed")
    except Exception as e:
        print(f"❌ Invalid request test failed: {e}")
        return False
    
    print("\n🎉 All API tests passed!")
    return True

def wait_for_api(base_url="http://localhost:5000", max_attempts=30):
    """Wait for the API to become available."""
    print(f"Waiting for API to become available at {base_url}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ API is ready after {attempt + 1} attempts")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
        print(f"Attempt {attempt + 1}/{max_attempts}...")
    
    print(f"❌ API did not become available after {max_attempts} attempts")
    return False

if __name__ == "__main__":
    import sys
    
    base_url = "http://localhost:5000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # Wait for API to be ready
    if wait_for_api(base_url):
        # Run tests
        success = test_api(base_url)
        sys.exit(0 if success else 1)
    else:
        print("❌ API not available for testing")
        sys.exit(1)