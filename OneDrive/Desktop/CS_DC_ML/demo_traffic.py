#!/usr/bin/env python3
"""
Real-Time Traffic Demo for AI-Powered Secure Load Balancer
Generates realistic traffic patterns to showcase monitoring capabilities
"""

import requests
import time
import random
import threading
import json
from datetime import datetime

class TrafficDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.running = True
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'attacks_blocked': 0
        }
        
    def normal_traffic(self):
        """Generate normal user traffic"""
        endpoints = [
            '/api/users',
            '/api/products', 
            '/api/orders',
            '/api/dashboard',
            '/api/search',
            '/api/profile',
            '/api/settings'
        ]
        
        methods = ['GET', 'POST', 'PUT']
        
        print("🚀 Starting normal traffic generation...")
        
        while self.running:
            try:
                endpoint = random.choice(endpoints)
                method = random.choice(methods)
                
                # Add some realistic parameters
                if method == 'GET':
                    if '?' in endpoint:
                        url = f"{self.base_url}{endpoint}&page={random.randint(1,10)}"
                    else:
                        url = f"{self.base_url}{endpoint}?page={random.randint(1,10)}"
                else:
                    url = f"{self.base_url}{endpoint}"
                
                start_time = time.time()
                response = requests.request(method, url, timeout=5)
                end_time = time.time()
                
                self.stats['total_requests'] += 1
                self.stats['successful_requests'] += 1
                
                print(f"✅ {method} {endpoint} - {response.status_code} - {(end_time - start_time)*1000:.1f}ms")
                
            except Exception as e:
                self.stats['total_requests'] += 1
                self.stats['failed_requests'] += 1
                print(f"❌ Failed request: {e}")
            
            # Random delay between requests (0.5-3 seconds)
            time.sleep(random.uniform(0.5, 3.0))
    
    def attack_traffic(self):
        """Generate malicious traffic to demonstrate security"""
        attacks = [
            # SQL Injection
            {'method': 'GET', 'path': '/api/users?id=1\' OR \'1\'=\'1', 'type': 'sql_injection'},
            {'method': 'POST', 'path': '/api/login', 'data': '{"username":"admin","password":"\' OR 1=1 --"}', 'type': 'sql_injection'},
            
            # XSS
            {'method': 'GET', 'path': '/api/search?q=<script>alert(1)</script>', 'type': 'xss'},
            {'method': 'POST', 'path': '/api/comment', 'data': '{"comment":"<img src=x onerror=alert(1)>"}', 'type': 'xss'},
            
            # Path Traversal
            {'method': 'GET', 'path': '/api/files/../../../etc/passwd', 'type': 'path_traversal'},
            {'method': 'GET', 'path': '/api/config/../../windows/system32/drivers/etc/hosts', 'type': 'path_traversal'},
            
            # Command Injection
            {'method': 'POST', 'path': '/api/ping', 'data': '{"host":"127.0.0.1; rm -rf /"}', 'type': 'command_injection'},
            {'method': 'GET', 'path': '/api/exec?cmd=ls%20-la', 'type': 'command_injection'},
            
            # DoS
            {'method': 'GET', 'path': '/api/heavy?size=1000000', 'type': 'dos'},
            {'method': 'POST', 'path': '/api/upload', 'data': 'A' * 1000000, 'type': 'dos'},
        ]
        
        print("🔥 Starting attack traffic generation...")
        
        while self.running:
            try:
                attack = random.choice(attacks)
                method = attack['method']
                path = attack['path']
                attack_type = attack['type']
                
                url = f"{self.base_url}{path}"
                
                if method == 'POST' and 'data' in attack:
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(url, data=attack['data'], headers=headers, timeout=5)
                else:
                    response = requests.get(url, timeout=5)
                
                self.stats['total_requests'] += 1
                
                if response.status_code in [403, 401, 400]:
                    self.stats['attacks_blocked'] += 1
                    print(f"🛡️ {attack_type.upper()} BLOCKED - {method} {path[:50]}... - {response.status_code}")
                else:
                    self.stats['successful_requests'] += 1
                    print(f"⚠️  {attack_type.upper()} ALLOWED - {method} {path[:50]}... - {response.status_code}")
                
            except Exception as e:
                self.stats['total_requests'] += 1
                self.stats['failed_requests'] += 1
                print(f"🚨 {attack_type.upper()} ERROR - {e}")
            
            # Attacks are less frequent (2-8 seconds apart)
            time.sleep(random.uniform(2, 8))
    
    def load_testing(self):
        """Generate high load for performance testing"""
        print("⚡ Starting load testing...")
        
        while self.running:
            try:
                # Send burst of requests
                threads = []
                for i in range(20):
                    thread = threading.Thread(target=self.single_request)
                    threads.append(thread)
                    thread.start()
                
                # Wait for all requests to complete
                for thread in threads:
                    thread.join()
                
                print(f"📊 Burst completed - Total: {self.stats['total_requests']}")
                
                # Rest between bursts
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Load testing error: {e}")
    
    def single_request(self):
        """Single request for load testing"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            self.stats['total_requests'] += 1
            self.stats['successful_requests'] += 1
        except:
            self.stats['total_requests'] += 1
            self.stats['failed_requests'] += 1
    
    def print_stats(self):
        """Print traffic statistics"""
        while self.running:
            time.sleep(10)
            print("\n" + "="*60)
            print("📊 TRAFFIC STATISTICS")
            print("="*60)
            print(f"Total Requests:     {self.stats['total_requests']}")
            print(f"Successful:         {self.stats['successful_requests']}")
            print(f"Failed:             {self.stats['failed_requests']}")
            print(f"Attacks Blocked:    {self.stats['attacks_blocked']}")
            print(f"Success Rate:       {(self.stats['successful_requests']/max(self.stats['total_requests'],1))*100:.1f}%")
            print("="*60)
    
    def start_demo(self):
        """Start the complete traffic demo"""
        print("🎭 Starting AI-Powered Load Balancer Traffic Demo")
        print("="*60)
        print("📊 Open dashboard: http://localhost:5000")
        print("🛡️ Security Center: http://localhost:5000/security")
        print("📈 Analytics: http://localhost:5000/analytics")
        print("🖥️ Servers: http://localhost:5000/servers")
        print("="*60)
        
        # Start traffic threads
        normal_thread = threading.Thread(target=self.normal_traffic)
        attack_thread = threading.Thread(target=self.attack_traffic)
        load_thread = threading.Thread(target=self.load_testing)
        stats_thread = threading.Thread(target=self.print_stats)
        
        normal_thread.daemon = True
        attack_thread.daemon = True
        load_thread.daemon = True
        stats_thread.daemon = True
        
        normal_thread.start()
        attack_thread.start()
        load_thread.start()
        stats_thread.start()
        
        try:
            print("\n🎯 Demo running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping demo...")
            self.running = False
            time.sleep(2)
            
            print("\n🎉 Demo Complete!")
            print("📊 Check your dashboard for real-time monitoring results!")

if __name__ == "__main__":
    demo = TrafficDemo()
    demo.start_demo()
