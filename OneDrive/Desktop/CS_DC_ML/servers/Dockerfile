# Dockerfile for Backend Servers
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server files
COPY server1.py .
COPY server2.py .
COPY server3.py .

# Expose ports
EXPOSE 8001 8002 8003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health && \
        curl -f http://localhost:8002/health && \
        curl -f http://localhost:8003/health || exit 1

# Start all servers
CMD ["python", "-c", "import subprocess; import sys; subprocess.Popen([sys.executable, 'server1.py']); subprocess.Popen([sys.executable, 'server2.py']); subprocess.Popen([sys.executable, 'server3.py']); import time; time.sleep(3600)"]
