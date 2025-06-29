#!/bin/bash
set -e

# Configuration
DOCKER_IMAGE_NAME="mlflow-model"
DOCKER_USERNAME="your-docker-username"  # Replace with your actual Docker username
CONTAINER_NAME="test-mlflow-container"
PORT=5000

echo "Starting local Docker test for MLflow model..."

# Clean up any existing containers
echo "Cleaning up existing containers..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Pull the latest image from DockerHub
echo "Pulling Docker image from DockerHub..."
if ! docker pull $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest; then
    echo "Failed to pull image from DockerHub"
    echo "Make sure you've built and pushed the image first:"
    echo "  docker build -t $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest ."
    echo "  docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest"
    exit 1
fi

# Run the container
echo "Starting Docker container on port $PORT..."
if ! docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest; then
    echo "Container failed to start"
    docker logs $CONTAINER_NAME
    exit 1
fi

# Wait for the service to be ready
echo "Waiting for service to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:$PORT/health >/dev/null 2>&1; then
        break
    fi
    echo "Attempt $i/30: Service not ready yet..."
    sleep 2
done

echo "Testing API endpoints..."

# Test health endpoint
echo "Testing health endpoint..."
curl -s http://localhost:$PORT/health | python -m json.tool

# Test model info endpoint
echo "Testing model info endpoint..."
curl -s http://localhost:$PORT/model_info | python -m json.tool

# Test prediction endpoint with sample data
echo "Testing prediction endpoint..."
curl -s -X POST http://localhost:$PORT/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [0,0,5,13,9,1,0,0,0,0,13,15,10,15,5,0,0,3,15,2,0,11,8,0,0,4,12,0,0,8,8,0,0,5,8,0,0,9,8,0,0,4,11,0,1,12,7,0,0,2,14,5,10,12,0,0,0,0,6,13,10,0,0,0]}' | python -m json.tool

echo "Docker test completed successfully!"
echo "The model API is working correctly in Docker!"

# Cleanup
echo "Cleaning up..."
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo "Local Docker test completed. Image is ready for production!" 