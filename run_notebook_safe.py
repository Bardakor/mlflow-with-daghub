#!/usr/bin/env python3
"""
Safe notebook execution that avoids DagHub connection issues.
This version runs the ML training without trying to connect to DagHub.
"""

import os
import json
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
import datetime
import sys

def ensure_data():
    """Ensure data is available"""
    print("Checking data availability...")
    
    if os.path.exists("data/raw_dataset.csv"):
        print("Using existing raw_dataset.csv")
        import pandas as pd
        data = pd.read_csv("data/raw_dataset.csv")
        
        # Extract features and target
        if 'target' in data.columns:
            X = data.drop('target', axis=1).values
            y = data['target'].values
        else:
            # Assume last column is target
            X = data.iloc[:, :-1].values
            y = data.iloc[:, -1].values
            
        print(f"Loaded data from CSV: {X.shape[0]} samples, {X.shape[1]} features")
        return X, y
    else:
        print("Loading sklearn digits dataset...")
        digits = load_digits()
        print(f"Loaded sklearn data: {digits.data.shape[0]} samples, {digits.data.shape[1]} features")
        return digits.data, digits.target

def train_models():
    """Train models without DagHub/MLflow integration"""
    print("Starting model training without external dependencies...")
    sys.stdout.flush()
    
    # Load data
    X, y = ensure_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    sys.stdout.flush()
    
    # Train two models like in the notebook
    models = []
    accuracies = []
    configs = [
        {"n_estimators": 20, "max_depth": 5, "name": "Model_1"},
        {"n_estimators": 100, "max_depth": 10, "name": "Model_2"}
    ]
    
    for i, config in enumerate(configs):
        print(f"Training {config['name']} (n_estimators={config['n_estimators']}, max_depth={config['max_depth']})...")
        sys.stdout.flush()
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=config['n_estimators'],
            max_depth=config['max_depth'],
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"{config['name']} accuracy: {accuracy:.4f}")
        sys.stdout.flush()
        
        # Save model
        os.makedirs("models", exist_ok=True)
        model_filename = f"models/model_estimators_{config['n_estimators']}_depth_{config['max_depth']}.pkl"
        joblib.dump(model, model_filename)
        
        models.append(model)
        accuracies.append(accuracy)
    
    # Save best model
    best_idx = accuracies.index(max(accuracies))
    best_model = models[best_idx]
    best_config = configs[best_idx]
    best_accuracy = accuracies[best_idx]
    
    print(f"Best model: {best_config['name']} with accuracy {best_accuracy:.4f}")
    sys.stdout.flush()
    
    # Save best model
    joblib.dump(best_model, "models/best_model.pkl")
    
    # Generate metadata
    model_metadata = {
        "model_type": "RandomForestClassifier",
        "accuracy": best_accuracy,
        "parameters": {
            "n_estimators": best_config['n_estimators'],
            "max_depth": best_config['max_depth'],
            "random_state": 42
        },
        "features": X_train.shape[1],
        "training_samples": X_train.shape[0],
        "test_samples": X_test.shape[0],
        "dataset": "sklearn.datasets.load_digits" if not os.path.exists("data/raw_dataset.csv") else "data/raw_dataset.csv",
        "training_date": datetime.datetime.now().isoformat(),
        "training_mode": "safe"
    }
    
    with open("models/model_metadata.json", "w") as f:
        json.dump(model_metadata, f, indent=2)
    
    print("Model and metadata saved successfully!")
    sys.stdout.flush()
    return True

def main():
    """Main execution function"""
    print("Safe notebook execution starting...")
    sys.stdout.flush()
    
    try:
        train_models()
        print("Safe notebook execution completed successfully!")
        sys.stdout.flush()
        return True
        
    except Exception as e:
        print(f"Error during safe execution: {e}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return False

if __name__ == "__main__":
    # Ensure unbuffered output
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    success = main()
    sys.exit(0 if success else 1) 