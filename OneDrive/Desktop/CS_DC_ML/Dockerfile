# Multi-stage Dockerfile for AI-Powered Secure Load Balancer
FROM python:3.9-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage for AI Model Training
FROM base as model-trainer

# Copy AI model files
COPY ai_model/ ./ai_model/

# Create necessary directories
RUN mkdir -p data models logs

# Train the model
RUN python ai_model/train_model.py

# Stage for Load Balancer
FROM base as load-balancer

# Copy application files
COPY load_balancer/ ./load_balancer/
COPY ai_model/ ./ai_model/

# Copy trained model from trainer stage
COPY --from=model-trainer /app/models ./models

# Create necessary directories
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV LB_HOST=0.0.0.0
ENV LB_PORT=8000
ENV ENABLE_AI_SECURITY=true
ENV BLOCK_MALICIOUS_REQUESTS=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the load balancer
CMD ["python", "load_balancer/load_balancer.py"]
