"""
Secure Load Balancer with AI-based Attack Detection
"""

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import time
import logging
from typing import Dict, List, Optional
import json
import sqlite3
from datetime import datetime
import uuid

from config import Config
from traffic_analyzer import TrafficFeatureExtractor
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_model.model_utils import predict_traffic_features

app = FastAPI(title="AI-Powered Secure Load Balancer")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackendServer:
    def __init__(self, host: str, port: int, weight: int = 1):
        self.host = host
        self.port = port
        self.weight = weight
        self.url = f"http://{host}:{port}"
        self.active_connections = 0
        self.total_requests = 0
        self.failed_requests = 0
        self.last_health_check = 0
        self.healthy = True
        self.response_times = []

class LoadBalancer:
    def __init__(self):
        self.servers = [
            BackendServer(s["host"], s["port"], s["weight"]) 
            for s in Config.BACKEND_SERVERS
        ]
        self.current_index = 0
        self.feature_extractor = TrafficFeatureExtractor()
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for logging"""
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                client_ip TEXT,
                method TEXT,
                path TEXT,
                server_url TEXT,
                status_code INTEGER,
                response_time REAL,
                is_malicious BOOLEAN,
                prediction TEXT,
                confidence REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                server_url TEXT,
                active_connections INTEGER,
                total_requests INTEGER,
                failed_requests INTEGER,
                avg_response_time REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_next_server(self) -> Optional[BackendServer]:
        """Select next server based on algorithm"""
        healthy_servers = [s for s in self.servers if s.healthy]
        
        if not healthy_servers:
            return None
        
        if Config.ALGORITHM == "round_robin":
            server = healthy_servers[self.current_index % len(healthy_servers)]
            self.current_index += 1
            return server
            
        elif Config.ALGORITHM == "least_connections":
            return min(healthy_servers, key=lambda s: s.active_connections)
            
        elif Config.ALGORITHM == "weighted_round_robin":
            weighted_servers = []
            for s in healthy_servers:
                weighted_servers.extend([s] * s.weight)
            server = weighted_servers[self.current_index % len(weighted_servers)]
            self.current_index += 1
            return server
        
        return healthy_servers[0]
    
    async def check_request_security(self, request: Request) -> Dict:
        """Check if request is malicious using AI model"""
        if not Config.ENABLE_AI_SECURITY:
            return {"is_malicious": False, "prediction": "normal", "confidence": 1.0}
        
        try:
            # Extract request data
            request_data = {
                "method": request.method,
                "path": str(request.url.path),
                "query_params": dict(request.query_params),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else "127.0.0.1",
                "body": await request.body()
            }
            
            # Extract features
            features = self.feature_extractor.extract_features(request_data)
            
            # Make prediction
            prediction = predict_traffic_features(features)
            
            if prediction:
                return prediction
            else:
                logger.warning("AI model prediction failed, allowing request")
                return {"is_malicious": False, "prediction": "normal", "confidence": 0.5}
                
        except Exception as e:
            logger.error(f"Security check error: {e}")
            return {"is_malicious": False, "prediction": "normal", "confidence": 0.5}
    
    def log_request(self, request_data: Dict, server: BackendServer, 
                   response_data: Dict, security_result: Dict):
        """Log request to database"""
        try:
            conn = sqlite3.connect(Config.SQLITE_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO requests 
                (id, timestamp, client_ip, method, path, server_url, status_code, 
                 response_time, is_malicious, prediction, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                datetime.now().isoformat(),
                request_data.get("client_ip"),
                request_data.get("method"),
                request_data.get("path"),
                server.url,
                response_data.get("status_code"),
                response_data.get("response_time"),
                security_result.get("is_malicious"),
                security_result.get("prediction"),
                security_result.get("confidence")
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Logging error: {e}")
    
    async def health_check_servers(self):
        """Periodic health check for backend servers"""
        while True:
            for server in self.servers:
                try:
                    async with httpx.AsyncClient(timeout=Config.HEALTH_CHECK_TIMEOUT) as client:
                        response = await client.get(f"{server.url}{Config.HEALTH_CHECK_PATH}")
                        server.healthy = response.status_code == 200
                except Exception:
                    server.healthy = False
                
                server.last_health_check = time.time()
            
            await asyncio.sleep(Config.HEALTH_CHECK_INTERVAL)

# Initialize load balancer
load_balancer = LoadBalancer()

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(load_balancer.health_check_servers())
    logger.info("Secure Load Balancer started")

@app.get("/")
async def root():
    return {"message": "AI-Powered Secure Load Balancer", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy", "servers": len(load_balancer.servers)}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(request: Request, path: str, background_tasks: BackgroundTasks):
    """Main proxy endpoint with security checking"""
    start_time = time.time()
    
    # Get request data
    request_data = {
        "method": request.method,
        "path": f"/{path}",
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client_ip": request.client.host if request.client else "127.0.0.1",
        "body": await request.body()
    }
    
    # Security check
    security_result = await load_balancer.check_request_security(request)
    
    if security_result.get("is_malicious") and Config.BLOCK_MALICIOUS_REQUESTS:
        logger.warning(f"Blocked malicious request: {security_result}")
        return JSONResponse(
            status_code=403,
            content={"error": "Request blocked by security system", "reason": security_result.get("prediction")}
        )
    
    # Get backend server
    server = load_balancer.get_next_server()
    if not server:
        raise HTTPException(status_code=503, detail="No healthy backend servers available")
    
    # Forward request
    try:
        server.active_connections += 1
        server.total_requests += 1
        
        url = f"{server.url}/{path}"
        headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
        
        async with httpx.AsyncClient(timeout=Config.REQUEST_TIMEOUT) as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                params=request.query_params,
                content=request_data["body"]
            )
        
        response_time = time.time() - start_time
        server.response_times.append(response_time)
        if len(server.response_times) > 100:
            server.response_times = server.response_times[-100:]
        
        # Log request in background
        response_data = {
            "status_code": response.status_code,
            "response_time": response_time
        }
        
        background_tasks.add_task(
            load_balancer.log_request,
            request_data, server, response_data, security_result
        )
        
        return JSONResponse(
            content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        server.failed_requests += 1
        logger.error(f"Proxy error: {e}")
        raise HTTPException(status_code=502, detail="Bad Gateway")
    
    finally:
        server.active_connections -= 1

@app.get("/metrics")
async def get_metrics():
    """Get load balancer metrics"""
    metrics = {
        "servers": [],
        "total_requests": sum(s.total_requests for s in load_balancer.servers),
        "total_failed": sum(s.failed_requests for s in load_balancer.servers),
        "algorithm": Config.ALGORITHM
    }
    
    for server in load_balancer.servers:
        avg_response_time = sum(server.response_times) / len(server.response_times) if server.response_times else 0
        metrics["servers"].append({
            "url": server.url,
            "healthy": server.healthy,
            "active_connections": server.active_connections,
            "total_requests": server.total_requests,
            "failed_requests": server.failed_requests,
            "avg_response_time": round(avg_response_time, 3)
        })
    
    return metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
