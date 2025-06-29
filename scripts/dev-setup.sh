#!/bin/bash
set -e

echo "=== MLOps Development Setup ==="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python package is installed
package_installed() {
    python -c "import $1" 2>/dev/null
}

# Check Python version
echo "Checking Python version..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_VERSION=$(python --version | cut -d' ' -f2)
    echo "Python $PYTHON_VERSION found"
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.11+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if requirements are already installed
echo "Checking installed packages..."
REQUIREMENTS_CHANGED=false

if [ ! -f ".venv/.requirements_installed" ] || [ "requirements.txt" -nt ".venv/.requirements_installed" ]; then
    echo "Requirements changed or not installed - installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .venv/.requirements_installed
    echo "Dependencies installed successfully"
else
    echo "Dependencies already up to date"
fi

# Check if models exist
if [ ! -f "models/best_model.pkl" ]; then
    echo "No trained model found - would you like to train one? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Training model using safe mode..."
        python run_training.py --mode safe
    fi
else
    echo "Trained model found"
fi

# Check if data exists
if [ ! -f "data/raw_dataset.csv" ]; then
    echo "No dataset found - creating sample data..."
    python create_sample_data.py
else
    echo "Dataset found"
fi

echo ""
echo "=== Setup Complete ==="
echo "To activate the environment: source .venv/bin/activate"
echo "To run the API: python app.py"
echo "To test the API: python test_api.py"
echo "To train models: python run_training.py --mode safe"
echo ""
echo "For Docker development:"
echo "  docker-compose -f docker-compose.dev.yml up --build"
echo "For training in Docker:"
echo "  docker-compose -f docker-compose.dev.yml --profile training up mlflow-train"
echo "" 