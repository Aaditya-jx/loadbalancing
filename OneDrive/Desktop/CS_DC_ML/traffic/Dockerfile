FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy traffic generator files
COPY traffic/traffic_generator.py .
COPY traffic/wait_for_lb.py .

# Environment variables
ENV PYTHONPATH=/app
ENV LOAD_BALANCER_URL=http://load-balancer:8000

# Run traffic generator
CMD ["python", "traffic_generator.py"]
