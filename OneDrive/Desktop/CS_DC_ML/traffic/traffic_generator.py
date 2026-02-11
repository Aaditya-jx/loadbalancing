"""
Traffic Generator for Load Balancer Testing
Simulates both normal and attack traffic patterns
"""

import asyncio
import aiohttp
import time
import random
import json
import logging
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrafficGenerator:
    def __init__(self, load_balancer_url: str = "http://localhost:8000"):
        self.load_balancer_url = load_balancer_url
        self.session = None
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'blocked_requests': 0,
            'normal_requests': 0,
            'attack_requests': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Normal traffic patterns
        self.normal_endpoints = [
            "/", "/health", "/api/users", "/api/products", "/api/dashboard",
            "/api/users/1", "/api/users/2", "/api/users/3",
            "/api/search?q=test", "/api/search?q=product", "/api/orders"
        ]
        
        self.normal_methods = ["GET", "POST"]
        self.normal_headers = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        ]
        
        # Attack traffic patterns
        self.attack_patterns = {
            'sql_injection': [
                "/api/users?id=1' OR '1'='1",
                "/api/search?q='; DROP TABLE users; --",
                "/api/orders?user_id=1 UNION SELECT * FROM users"
            ],
            'xss': [
                "/api/search?q=<script>alert('xss')</script>",
                "/api/users?name=<img src=x onerror=alert('xss')>",
                "/api/dashboard?data=javascript:alert('xss')"
            ],
            'path_traversal': [
                "/api/users/../../../etc/passwd",
                "/api/files/..\\..\\..\\windows\\system32\\config\\sam",
                "/api/upload/../../../../root/.ssh/id_rsa"
            ],
            'command_injection': [
                "/api/search?q=; cat /etc/passwd",
                "/api/users?name=| whoami",
                "/api/orders?data=`id`"
            ],
            'dos_simulation': [
                "/api/users" * 100,  # Long path
                "/api/search?q=" + "A" * 10000,  # Large query parameter
                "/" + "A" * 5000  # Very long path
            ],
            'suspicious_user_agents': [
                {"User-Agent": "sqlmap/1.6.12"},
                {"User-Agent": "Nikto/2.1.6"},
                {"User-Agent": "nmap scripting engine"},
                {"User-Agent": "python-requests/2.28.1"},
                {"User-Agent": "curl/7.68.0"}
            ]
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def generate_normal_request(self) -> Dict:
        """Generate a normal HTTP request"""
        endpoint = random.choice(self.normal_endpoints)
        method = random.choice(self.normal_methods)
        headers = random.choice(self.normal_headers).copy()
        
        # Add some random query parameters for variety
        if '?' not in endpoint and random.random() > 0.7:
            endpoint += f"?random={random.randint(1, 1000)}"
        
        # Generate request body for POST requests
        body = None
        if method == "POST":
            if 'orders' in endpoint:
                body = json.dumps({
                    "user_id": random.randint(1, 9),
                    "total": round(random.uniform(10.0, 500.0), 2)
                })
                headers["Content-Type"] = "application/json"
            elif 'upload' in endpoint:
                body = f"Sample file content {random.randint(1, 1000)}"
                headers["Content-Type"] = "text/plain"
        
        return {
            "method": method,
            "url": f"{self.load_balancer_url}{endpoint}",
            "headers": headers,
            "body": body,
            "type": "normal"
        }
    
    def generate_attack_request(self) -> Dict:
        """Generate a malicious HTTP request"""
        attack_types = list(self.attack_patterns.keys())
        attack_type = random.choice(attack_types)
        
        if attack_type == 'suspicious_user_agents':
            headers = random.choice(self.attack_patterns[attack_type])
            endpoint = random.choice(self.normal_endpoints)
            method = "GET"
            body = None
        else:
            patterns = self.attack_patterns[attack_type]
            endpoint = random.choice(patterns)
            method = "GET"
            headers = random.choice(self.normal_headers).copy()
            body = None
        
        return {
            "method": method,
            "url": f"{self.load_balancer_url}{endpoint}",
            "headers": headers,
            "body": body,
            "type": "attack",
            "attack_type": attack_type
        }
    
    async def send_request(self, request_data: Dict) -> Dict:
        """Send a single HTTP request"""
        start_time = time.time()
        
        try:
            kwargs = {
                "headers": request_data["headers"],
                "timeout": aiohttp.ClientTimeout(total=10)
            }
            
            if request_data["body"]:
                kwargs["data"] = request_data["body"]
            
            async with self.session.request(
                request_data["method"],
                request_data["url"],
                **kwargs
            ) as response:
                response_time = time.time() - start_time
                response_text = await response.text()
                
                # Try to parse JSON response
                try:
                    response_json = await response.json()
                except:
                    response_json = {"raw_response": response_text[:500]}
                
                return {
                    "status_code": response.status,
                    "response_time": response_time,
                    "response": response_json,
                    "success": True,
                    "blocked": response.status == 403,
                    "request_type": request_data["type"],
                    "attack_type": request_data.get("attack_type", "none")
                }
                
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "status_code": 0,
                "response_time": response_time,
                "response": {"error": str(e)},
                "success": False,
                "blocked": False,
                "request_type": request_data["type"],
                "attack_type": request_data.get("attack_type", "none")
            }
    
    async def generate_traffic_burst(self, num_requests: int, attack_ratio: float = 0.3):
        """Generate a burst of traffic with specified attack ratio"""
        tasks = []
        
        for i in range(num_requests):
            if random.random() < attack_ratio:
                request_data = self.generate_attack_request()
                self.stats['attack_requests'] += 1
            else:
                request_data = self.generate_normal_request()
                self.stats['normal_requests'] += 1
            
            self.stats['total_requests'] += 1
            tasks.append(self.send_request(request_data))
        
        # Execute all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Update statistics
        for result in results:
            if isinstance(result, Exception):
                self.stats['failed_requests'] += 1
            else:
                if result["success"]:
                    self.stats['successful_requests'] += 1
                else:
                    self.stats['failed_requests'] += 1
                
                if result["blocked"]:
                    self.stats['blocked_requests'] += 1
        
        return results
    
    async def continuous_traffic(self, duration: int, requests_per_second: int = 10, attack_ratio: float = 0.2):
        """Generate continuous traffic for specified duration"""
        logger.info(f"Starting continuous traffic generation: {duration}s, {requests_per_second} req/s, {attack_ratio*100}% attacks")
        
        end_time = time.time() + duration
        interval = 1.0 / requests_per_second
        
        while time.time() < end_time:
            batch_start = time.time()
            
            # Generate a batch of requests
            batch_size = min(requests_per_second, 5)  # Limit batch size for better control
            await self.generate_traffic_burst(batch_size, attack_ratio)
            
            # Wait for next interval
            elapsed = time.time() - batch_start
            if elapsed < interval:
                await asyncio.sleep(interval - elapsed)
    
    def print_statistics(self):
        """Print traffic generation statistics"""
        if self.stats['start_time'] and self.stats['end_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
            rps = self.stats['total_requests'] / duration if duration > 0 else 0
        else:
            duration = 0
            rps = 0
        
        print("\n" + "="*60)
        print("TRAFFIC GENERATION STATISTICS")
        print("="*60)
        print(f"Total Requests:     {self.stats['total_requests']}")
        print(f"Successful:         {self.stats['successful_requests']}")
        print(f"Failed:             {self.stats['failed_requests']}")
        print(f"Blocked:            {self.stats['blocked_requests']}")
        print(f"Normal Requests:    {self.stats['normal_requests']}")
        print(f"Attack Requests:    {self.stats['attack_requests']}")
        print(f"Duration:           {duration:.2f} seconds")
        print(f"Requests/Second:    {rps:.2f}")
        
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
            block_rate = (self.stats['blocked_requests'] / self.stats['total_requests']) * 100
            attack_rate = (self.stats['attack_requests'] / self.stats['total_requests']) * 100
            
            print(f"Success Rate:       {success_rate:.2f}%")
            print(f"Block Rate:         {block_rate:.2f}%")
            print(f"Attack Rate:        {attack_rate:.2f}%")
        
        print("="*60)

async def main():
    """Main traffic generation function"""
    # Configuration
    LOAD_BALANCER_URL = "http://localhost:8000"
    
    print("AI-Powered Secure Load Balancer - Traffic Generator")
    print("=" * 60)
    
    async with TrafficGenerator(LOAD_BALANCER_URL) as generator:
        generator.stats['start_time'] = time.time()
        
        try:
            # Phase 1: Normal traffic warm-up
            print("\nPhase 1: Normal traffic warm-up (30 seconds)")
            await generator.continuous_traffic(duration=30, requests_per_second=5, attack_ratio=0.0)
            
            # Phase 2: Mixed traffic with moderate attacks
            print("\nPhase 2: Mixed traffic with moderate attacks (60 seconds)")
            await generator.continuous_traffic(duration=60, requests_per_second=10, attack_ratio=0.2)
            
            # Phase 3: High attack intensity
            print("\nPhase 3: High attack intensity (30 seconds)")
            await generator.continuous_traffic(duration=30, requests_per_second=15, attack_ratio=0.5)
            
            # Phase 4: Burst attack simulation
            print("\nPhase 4: Burst attack simulation")
            for i in range(5):
                print(f"  Burst {i+1}/5")
                await generator.generate_traffic_burst(50, attack_ratio=0.8)
                await asyncio.sleep(2)
            
            # Phase 5: Return to normal traffic
            print("\nPhase 5: Return to normal traffic (30 seconds)")
            await generator.continuous_traffic(duration=30, requests_per_second=8, attack_ratio=0.1)
            
        except KeyboardInterrupt:
            print("\nTraffic generation interrupted by user")
        
        finally:
            generator.stats['end_time'] = time.time()
            generator.print_statistics()

if __name__ == "__main__":
    # Check if load balancer is running
    import aiohttp
    
    async def check_load_balancer():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8000/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        return True
        except:
            pass
        return False
    
    # Run traffic generation
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTraffic generation stopped by user")
