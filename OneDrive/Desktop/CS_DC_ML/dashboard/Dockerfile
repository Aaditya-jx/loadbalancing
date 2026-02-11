# Dockerfile for Dashboard
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard files
COPY dashboard/app.py .
COPY dashboard/templates/ ./templates/
COPY dashboard/static/ ./static/

# Create necessary directories
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Environment variables
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the dashboard
CMD ["python", "app.py"]
