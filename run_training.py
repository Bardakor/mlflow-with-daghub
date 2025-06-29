#!/usr/bin/env python3
"""
Unified ML training script that can run in different modes:
- notebook: Execute the actual Jupyter notebook with MLflow tracking
- fast: Quick training with smaller models (no notebook)
- safe: Training without external dependencies (no notebook)
"""

import os
import sys
import json
import joblib
import argparse
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
import datetime

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

def setup_mlflow(mode="safe"):
    """Setup MLflow/DagHub connection if possible"""
    if mode == "safe":
        return False
    
    try:
        import mlflow
        import dagshub
        
        # Get credentials from environment
        dagshub_token = os.getenv('DAGSHUB_TOKEN', '')
        if dagshub_token:
            os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_token
            os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token

        dagshub.init(repo_owner='Bardakor', repo_name='mlflow-with-daghub', mlflow=True)
        print("MLflow/DagHub connection established")
        return True
    except Exception as e:
        print(f"MLflow setup failed: {e}")
        print("Continuing without MLflow tracking...")
        return False

def run_notebook_mode():
    """Execute the actual Jupyter notebook"""
    try:
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor
        
        print("Starting Jupyter notebook execution...")
        start_time = time.time()
        
        with open("MLFlowSetup.ipynb") as f:
            nb = nbformat.read(f, as_version=4)
        
        print(f"Notebook loaded with {len(nb.cells)} cells")
        
        # Configure executor
        ep = ExecutePreprocessor(
            timeout=900,  # 15 minutes max
            kernel_name='python3',
            allow_errors=False
        )
        
        print("Executing notebook cells...")
        ep.preprocess(nb, {'metadata': {'path': './'}})
        
        elapsed = time.time() - start_time
        print(f"Notebook executed successfully in {elapsed:.2f} seconds!")
        return True
        
    except Exception as e:
        print(f"Error executing notebook: {e}")
        return False

def run_direct_training(mode="safe"):
    """Run training directly without notebook"""
    print(f"Starting direct model training in {mode} mode...")
    sys.stdout.flush()
    
    # Load data
    X, y = ensure_data()
    
    # Adjust dataset size based on mode
    if mode == "fast":
        # Use smaller dataset for speed
        X = X[:500]
        y = y[:500]
        print(f"Using reduced dataset: {len(X)} samples")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    sys.stdout.flush()
    
    # Setup MLflow if requested
    mlflow_enabled = setup_mlflow(mode)
    
    if mlflow_enabled:
        import mlflow
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        experiment_name = f"RandomForestExperiment_{mode}_{timestamp}"
        mlflow.set_experiment(experiment_name)
        print(f"Using MLflow experiment: {experiment_name}")
    
    # Define model configurations based on mode
    if mode == "fast":
        configs = [
            {"n_estimators": 10, "max_depth": 3, "name": "FastModel_10_3"},
            {"n_estimators": 20, "max_depth": 5, "name": "FastModel_20_5"}
        ]
    else:  # safe or default
        configs = [
            {"n_estimators": 20, "max_depth": 5, "name": "Model_1"},
            {"n_estimators": 100, "max_depth": 10, "name": "Model_2"}
        ]
    
    models = []
    accuracies = []
    
    for i, config in enumerate(configs):
        print(f"Training {config['name']} (n_estimators={config['n_estimators']}, max_depth={config['max_depth']})...")
        sys.stdout.flush()
        
        # Start MLflow run if enabled
        if mlflow_enabled:
            mlflow.start_run(run_name=config['name'])
        
        try:
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
            
            # Log to MLflow if enabled
            if mlflow_enabled:
                mlflow.log_param("n_estimators", config['n_estimators'])
                mlflow.log_param("max_depth", config['max_depth'])
                mlflow.log_param("random_state", 42)
                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("n_features", X_train.shape[1])
                mlflow.log_metric("training_samples", X_train.shape[0])
                mlflow.log_metric("test_samples", X_test.shape[0])
                
                try:
                    mlflow.sklearn.log_model(model, "model")
                except Exception as e:
                    print(f"Could not log model to MLflow: {e}")
            
            # Save model locally
            os.makedirs("models", exist_ok=True)
            model_filename = f"models/model_estimators_{config['n_estimators']}_depth_{config['max_depth']}.pkl"
            joblib.dump(model, model_filename)
            
            models.append(model)
            accuracies.append(accuracy)
            
        finally:
            if mlflow_enabled:
                mlflow.end_run()
    
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
        "training_mode": mode,
        "mlflow_enabled": mlflow_enabled
    }
    
    with open("models/model_metadata.json", "w") as f:
        json.dump(model_metadata, f, indent=2)
    
    print("Model and metadata saved successfully!")
    sys.stdout.flush()
    return True

def main():
    parser = argparse.ArgumentParser(description="ML Training Script")
    parser.add_argument(
        "--mode", 
        choices=["notebook", "fast", "safe"], 
        default="safe",
        help="Training mode: notebook (full Jupyter), fast (quick), safe (no external deps)"
    )
    
    args = parser.parse_args()
    
    # Ensure unbuffered output
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    print(f"Starting ML training in {args.mode} mode...")
    sys.stdout.flush()
    
    try:
        if args.mode == "notebook":
            success = run_notebook_mode()
        else:
            success = run_direct_training(args.mode)
        
        if success:
            print(f"Training completed successfully in {args.mode} mode!")
        else:
            print(f"Training failed in {args.mode} mode!")
        
        return success
        
    except Exception as e:
        print(f"Error during {args.mode} training: {e}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 