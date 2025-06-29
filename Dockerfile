FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (this layer rarely changes)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy ONLY requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies (this layer only rebuilds when requirements.txt changes)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code (this layer rebuilds when code changes)
COPY app.py .
COPY generate_metadata.py .
COPY create_sample_data.py .
COPY run_training.py .

# Create directories
RUN mkdir -p models data

# Copy trained models (if they exist locally)
COPY models/ ./models/

# Ensure data is available
RUN python create_sample_data.py

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
# Can be overridden for development: docker run -it image bash
CMD ["python", "app.py"]