#!/bin/bash

# Script to test the Docker image locally
# This script builds the image, runs it, tests it, and cleans up

set -e

# Configuration
IMAGE_NAME="mlflow-model"
CONTAINER_NAME="mlflow-test"
PORT="5000"

echo "🚀 Starting local Docker test for MLflow model..."

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Build the Docker image
echo "🏗️  Building Docker image..."
docker build -t $IMAGE_NAME .

# Run the container
echo "🏃 Running Docker container..."
docker run -d \
    --name $CONTAINER_NAME \
    -p $PORT:5000 \
    $IMAGE_NAME

# Wait for the container to be ready and test
echo "⏳ Waiting for container to be ready..."
sleep 15

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "❌ Container failed to start"
    docker logs $CONTAINER_NAME
    exit 1
fi

# Test the API
echo "🧪 Testing API endpoints..."
python test_api.py http://localhost:$PORT

# Show container logs
echo "📝 Container logs:"
docker logs $CONTAINER_NAME

# Test completed successfully
echo "✅ Docker test completed successfully!"
echo "🎉 The model API is working correctly in Docker!"

# Cleanup will happen automatically due to trap 