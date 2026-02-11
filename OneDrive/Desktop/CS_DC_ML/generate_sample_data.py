import sqlite3
import random
import os
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate sample data for the dashboard"""
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(__file__), 'logs', 'load_balancer.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    servers = ['http://localhost:8001', 'http://localhost:8002', 'http://localhost:8003']
    attack_types = ['sql_injection', 'xss', 'path_traversal', 'command_injection', 'dos', 'brute_force']
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/dashboard', '/api/search']
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    
    # Generate requests
    print("Generating sample requests...")
    for i in range(100):
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))
        server_url = random.choice(servers)
        is_malicious = random.random() > 0.2
        attack_type = random.choice(attack_types) if is_malicious else None
        prediction = attack_type if is_malicious else 'normal'
        confidence = random.uniform(0.7, 1.0) if is_malicious else random.uniform(0.8, 1.0)
        
        sql = "INSERT INTO requests (id, timestamp, client_ip, method, path, server_url, status_code, response_time, is_malicious, prediction, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (
            f'req-{i+1}',
            timestamp.isoformat(),
            f'192.168.1.{random.randint(1, 254)}',
            random.choice(methods),
            random.choice(endpoints),
            server_url,
            random.choice([200, 201, 400, 403, 404, 500]),
            round(random.uniform(10, 200), 2),
            is_malicious,
            prediction,
            confidence
        )
        cursor.execute(sql, values)
    
    # Generate server metrics
    print("Generating server metrics...")
    for server_url in servers:
        sql = "INSERT INTO server_metrics (timestamp, server_url, active_connections, total_requests, failed_requests, avg_response_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (
            datetime.now().isoformat(),
            server_url,
            random.randint(5, 50),
            random.randint(100, 1000),
            random.randint(0, 10),
            round(random.uniform(20, 100), 2)
        )
        print(f"SQL: {sql}")
        print(f"Values: {values}")
        print(f"Number of values: {len(values)}")
        cursor.execute(sql, values)
    
    conn.commit()
    conn.close()
    print("Sample data generated successfully!")

if __name__ == "__main__":
    generate_sample_data()
