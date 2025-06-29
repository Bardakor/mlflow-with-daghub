import mlflow
import mlflow.sklearn
import dagshub
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
import joblib

def main():
    # Initialize DagHub (you'll need to replace with your actual repo)
    # dagshub.init(repo_owner='your_github_username', repo_name='mlflow-with-daghub', mlflow=True)
    
    # For now, we'll use environment variables for the MLFlow tracking URI
    if 'MLFLOW_TRACKING_URI' in os.environ:
        mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    
    # Load data
    data = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
    
    # Set experiment
    experiment_name = "RandomForestExperiment"
    mlflow.set_experiment(experiment_name)
    
    def train_and_log_model(n_estimators, max_depth, run_name):
        with mlflow.start_run(run_name=run_name):
            # Train model
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
            model.fit(X_train, y_train)
            
            # Make predictions
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            
            # Log parameters and metrics
            mlflow.log_param("n_estimators", n_estimators)
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_metric("accuracy", accuracy)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Save model locally for Docker
            os.makedirs("models", exist_ok=True)
            joblib.dump(model, "models/best_model.pkl")
            
            print(f"Model {run_name}: n_estimators={n_estimators}, max_depth={max_depth}, accuracy={accuracy:.4f}")
            
            return model, accuracy
    
    # Train models
    print("Training models...")
    model1, acc1 = train_and_log_model(n_estimators=20, max_depth=5, run_name="model_1")
    model2, acc2 = train_and_log_model(n_estimators=100, max_depth=10, run_name="model_2")
    
    # Save the better model
    best_model = model1 if acc1 > acc2 else model2
    joblib.dump(best_model, "models/best_model.pkl")
    
    print(f"Best model saved with accuracy: {max(acc1, acc2):.4f}")

if __name__ == "__main__":
    main()