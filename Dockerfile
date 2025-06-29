FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY run_notebook.py .
COPY generate_metadata.py .
COPY MLFlowSetup.ipynb .

# Create models and data directories
RUN mkdir -p models data

# Copy models and data if they exist
COPY models ./models
COPY data ./data

# Set environment variables for MLflow/DagHub
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]