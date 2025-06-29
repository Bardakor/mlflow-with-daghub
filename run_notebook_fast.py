#!/usr/bin/env python3
"""
Fast version of notebook execution for local testing.
Uses smaller models and reduced data for quicker iteration.
"""

import os
import json
import joblib
import mlflow
import mlflow.sklearn
import dagshub
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
import datetime
import sys

def setup_dagshub():
    """Setup DagHub connection"""
    try:
        # Get credentials from environment or use defaults for local development
        dagshub_token = os.getenv('DAGSHUB_TOKEN', '')
        if dagshub_token:
            os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_token
            os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token

        dagshub.init(repo_owner='Bardakor', repo_name='mlflow-with-daghub', mlflow=True)
        print("DagHub connection established")
        sys.stdout.flush()
        return True
    except Exception as e:
        print(f"DagHub setup failed: {e}")
        print("Continuing with local MLflow...")
        sys.stdout.flush()
        return False

def train_fast_models():
    """Train models with reduced complexity for faster execution"""
    print("Starting fast model training...")
    sys.stdout.flush()
    
    # Load data
    data = load_digits()
    
    # Use smaller dataset for speed
    X_sample = data.data[:500]  # Use only 500 samples instead of 1797
    y_sample = data.target[:500]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_sample, y_sample, test_size=0.2, random_state=42
    )
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples")
    sys.stdout.flush()
    
    # Setup MLflow experiment
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_name = f"FastRandomForestExperiment_{timestamp}"
    mlflow.set_experiment(experiment_name)
    print(f"Using experiment: {experiment_name}")
    sys.stdout.flush()
    
    models = []
    accuracies = []
    
    # Train two smaller models
    configs = [
        {"n_estimators": 10, "max_depth": 3, "name": "FastModel_10_3"},
        {"n_estimators": 20, "max_depth": 5, "name": "FastModel_20_5"}
    ]
    
    for i, config in enumerate(configs):
        print(f"Training model {i+1}/2: {config['name']}")
        sys.stdout.flush()
        
        with mlflow.start_run(run_name=config['name']):
            # Train model
            model = RandomForestClassifier(
                n_estimators=config['n_estimators'],
                max_depth=config['max_depth'],
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Make predictions
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            
            # Log to MLflow
            mlflow.log_param("n_estimators", config['n_estimators'])
            mlflow.log_param("max_depth", config['max_depth'])
            mlflow.log_param("random_state", 42)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("n_features", X_train.shape[1])
            mlflow.log_metric("training_samples", X_train.shape[0])
            mlflow.log_metric("test_samples", X_test.shape[0])
            
            # Try to log model
            try:
                mlflow.sklearn.log_model(model, "model")
            except Exception as e:
                print(f"Could not log model to MLflow: {e}")
                sys.stdout.flush()
            
            # Save locally
            os.makedirs("models", exist_ok=True)
            filename = f"models/model_estimators_{config['n_estimators']}_depth_{config['max_depth']}.pkl"
            joblib.dump(model, filename)
            
            models.append(model)
            accuracies.append(accuracy)
            
            print(f"Model {config['name']} - Accuracy: {accuracy:.4f}")
            sys.stdout.flush()
    
    # Save best model
    best_idx = accuracies.index(max(accuracies))
    best_model = models[best_idx]
    best_config = configs[best_idx]
    best_accuracy = accuracies[best_idx]
    
    print(f"Best model: {best_config['name']} with accuracy {best_accuracy:.4f}")
    sys.stdout.flush()
    
    # Save best model
    joblib.dump(best_model, "models/best_model.pkl")
    
    # Save metadata
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
        "dataset": "sklearn.datasets.load_digits (sample)",
        "training_date": datetime.datetime.now().isoformat(),
        "training_mode": "fast"
    }
    
    with open("models/model_metadata.json", "w") as f:
        json.dump(model_metadata, f, indent=2)
    
    print("Best model and metadata saved!")
    sys.stdout.flush()
    return True

def main():
    """Main execution function"""
    print("Fast notebook execution starting...")
    sys.stdout.flush()
    
    try:
        # Setup DagHub (optional for local testing)
        setup_dagshub()
        
        # Train models
        train_fast_models()
        
        print("Fast notebook execution completed successfully!")
        sys.stdout.flush()
        return True
        
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.stdout.flush()
        return False

if __name__ == "__main__":
    import sys
    # Ensure unbuffered output
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    success = main()
    sys.exit(0 if success else 1) 