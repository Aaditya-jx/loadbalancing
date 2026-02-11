"""
Load Balancer Configuration
"""

import os
from typing import List, Dict

class Config:
    # Load Balancer Settings
    HOST = os.getenv("LB_HOST", "0.0.0.0")
    PORT = int(os.getenv("LB_PORT", 8000))
    
    # Backend Servers
    BACKEND_SERVERS = [
        {"host": "localhost", "port": 8001, "weight": 1},
        {"host": "localhost", "port": 8002, "weight": 1},
        {"host": "localhost", "port": 8003, "weight": 1}
    ]
    
    # Load Balancing Algorithm
    ALGORITHM = os.getenv("LB_ALGORITHM", "least_connections")  # "round_robin", "least_connections", "weighted_round_robin"
    
    # Health Check Settings
    HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", 30))  # seconds
    HEALTH_CHECK_TIMEOUT = int(os.getenv("HEALTH_CHECK_TIMEOUT", 5))  # seconds
    HEALTH_CHECK_PATH = "/health"
    
    # Security Settings
    ENABLE_AI_SECURITY = os.getenv("ENABLE_AI_SECURITY", "false").lower() == "true"
    BLOCK_MALICIOUS_REQUESTS = os.getenv("BLOCK_MALICIOUS_REQUESTS", "true").lower() == "true"
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", os.path.join(os.path.dirname(__file__), "..", "logs", "load_balancer.log"))
    
    # Database Settings
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # "sqlite" or "mongodb"
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "logs", "load_balancer.db"))
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "load_balancer")
    
    # AI Model Settings
    MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(os.path.dirname(__file__), "..", "models"))
    MODEL_CONFIDENCE_THRESHOLD = float(os.getenv("MODEL_CONFIDENCE_THRESHOLD", 0.7))
    
    # Request Settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))  # seconds
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    # Metrics Settings
    METRICS_COLLECTION_INTERVAL = int(os.getenv("METRICS_COLLECTION_INTERVAL", 60))  # seconds
    
    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
