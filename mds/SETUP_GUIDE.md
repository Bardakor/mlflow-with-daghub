# MLOps Pipeline Setup Guide

This guide will walk you through setting up a complete MLOps pipeline with GitHub, DagHub, DVC, Docker, and DockerHub.

## Overview

This project creates an end-to-end MLOps pipeline that:
1. Tracks ML experiments with MLflow on DagHub
2. Manages data with DVC
3. Builds and deploys models in Docker containers
4. Automatically pushes images to DockerHub via GitHub Actions
5. Provides a REST API for model inference

## Prerequisites

- Git and GitHub account
- DagHub account (free at https://dagshub.com)
- DockerHub account (free at https://hub.docker.com)
- Python 3.11+
- Docker installed locally

## Step 1: GitHub Repository Setup

1. Fork or clone this repository to your GitHub account
2. Ensure you have push access to the repository

## Step 2: DagHub Setup

1. **Create a DagHub account** at https://dagshub.com
2. **Create a new repository** on DagHub or connect your GitHub repo
3. **Get your DagHub token**:
   - Go to https://dagshub.com/user/settings/tokens
   - Create a new token with read/write permissions
   - Save this token - you'll need it for GitHub secrets

## Step 3: DockerHub Setup

1. **Create a DockerHub account** at https://hub.docker.com
2. **Create a new repository** (e.g., `your-username/mlflow-model`)
3. **Get your DockerHub credentials**:
   - Username: Your DockerHub username
   - Password: Your DockerHub password or access token

## Step 4: GitHub Secrets Configuration

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

```
DAGSHUB_USERNAME=your-dagshub-username
DAGSHUB_TOKEN=your-dagshub-token-from-step-2
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password-or-token
```

## Step 5: Update Repository References

Update the following files with your repository information:

### .dvc/config
```
['remote "origin"']
    url = https://dagshub.com/YOUR-USERNAME/YOUR-REPO-NAME.dvc
```

### .github/workflows/ci-cd.yml
The workflow references `Bardakor/mlflow-with-daghub` - update this to your repository.

## Step 6: Local Testing (Optional but Recommended)

### Test the API locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the notebook to train models
python run_notebook.py

# Generate model metadata
python generate_metadata.py

# Test the API
python app.py &
sleep 5
python test_api.py
```

### Test Docker locally:
```bash
# Run the comprehensive Docker test
./test_docker_local.sh
```

## Step 7: Push to GitHub and Trigger Pipeline

```bash
# Commit all changes
git add -A
git commit -m "Setup MLOps pipeline with DagHub, DVC, and Docker"

# Push to main branch (this will trigger the pipeline)
git push origin main
```

## Step 8: Monitor the Pipeline

1. **GitHub Actions**: Go to your repository → Actions tab to monitor the build
2. **DagHub Experiments**: Visit https://dagshub.com/YOUR-USERNAME/YOUR-REPO-NAME.mlflow to see experiments
3. **DockerHub**: Check your DockerHub repository for the pushed image

## Step 9: Test the Deployed Image

Once the pipeline completes successfully:

```bash
# Pull the image from DockerHub
docker pull YOUR-DOCKERHUB-USERNAME/mlflow-model:latest

# Run the container
docker run -d -p 5000:5000 --name mlflow-api YOUR-DOCKERHUB-USERNAME/mlflow-model:latest

# Test the API
python test_api.py http://localhost:5000

# Clean up
docker stop mlflow-api
docker rm mlflow-api
```

## Pipeline Components

### Files Overview:

- **MLFlowSetup.ipynb**: Original notebook with ML experiments
- **app.py**: Flask REST API for model serving
- **generate_metadata.py**: Script to generate model metadata
- **test_api.py**: Comprehensive API testing script
- **test_docker_local.sh**: Local Docker testing script
- **.github/workflows/ci-cd.yml**: GitHub Actions pipeline
- **Dockerfile**: Container definition
- **.dvc/config**: DVC configuration for data management

### API Endpoints:

- `GET /health`: Health check endpoint
- `GET /model_info`: Get model information and metadata
- `POST /predict`: Make predictions (expects JSON with "features" array)

### Example API Usage:

```python
import requests
import numpy as np
from sklearn.datasets import load_digits

# Load sample data
digits = load_digits()
sample_features = digits.data[0].tolist()

# Make prediction
response = requests.post(
    "http://localhost:5000/predict",
    json={"features": sample_features}
)

print(response.json())
```

## Troubleshooting

### Common Issues:

1. **DVC Pull Fails**: Ensure DAGSHUB_TOKEN has correct permissions
2. **Docker Build Fails**: Check if model files exist in the models/ directory
3. **API Tests Fail**: Ensure the model was trained and saved properly
4. **GitHub Actions Fail**: Check that all secrets are correctly configured

### Debug Commands:

```bash
# Check DVC status
dvc status

# Verify model files
ls -la models/

# Test Docker build manually
docker build -t test-image .

# Check container logs
docker logs container-name
```

## Expected Results

After successful setup, you should have:

1. ✅ ML experiments tracked in DagHub
2. ✅ Data managed with DVC
3. ✅ Automated Docker builds on GitHub
4. ✅ Docker image pushed to DockerHub
5. ✅ Working REST API for model inference
6. ✅ Comprehensive testing pipeline

## Recording Your Demo

For your submission, record a screen showing:

1. **DagHub experiments page** with your ML runs
2. **GitHub Actions** showing successful pipeline execution
3. **DockerHub repository** with your uploaded image
4. **Local Docker test** pulling and running the image from DockerHub
5. **API testing** showing the model serving predictions

Good luck! 🚀 