"""
Real-time Web Dashboard for AI-Powered Secure Load Balancer
Displays system metrics, attack detection, and server health
"""

from flask import Flask, render_template, jsonify
import sqlite3
import json
from datetime import datetime, timedelta
import os
import time

app = Flask(__name__, static_folder='static')

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "load_balancer.db")

class DashboardData:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_overview_stats(self):
        """Get overview statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total requests
        cursor.execute("SELECT COUNT(*) FROM requests")
        total_requests = cursor.fetchone()[0]
        
        # Blocked requests
        cursor.execute("SELECT COUNT(*) FROM requests WHERE is_malicious = 1")
        blocked_requests = cursor.fetchone()[0]
        
        # Attack types
        cursor.execute("""
            SELECT prediction, COUNT(*) as count 
            FROM requests 
            WHERE is_malicious = 1 
            GROUP BY prediction
        """)
        attack_types = dict(cursor.fetchall())
        
        # Last 24 hours stats
        yesterday = datetime.now() - timedelta(days=1)
        cursor.execute("""
            SELECT COUNT(*) FROM requests 
            WHERE timestamp > ?
        """, (yesterday.isoformat(),))
        requests_24h = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM requests 
            WHERE is_malicious = 1 AND timestamp > ?
        """, (yesterday.isoformat(),))
        attacks_24h = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_requests": total_requests,
            "blocked_requests": blocked_requests,
            "block_rate": round((blocked_requests / total_requests * 100) if total_requests > 0 else 0, 2),
            "attack_types": attack_types,
            "requests_24h": requests_24h,
            "attacks_24h": attacks_24h
        }
    
    def get_server_metrics(self):
        """Get server metrics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get latest server metrics
        cursor.execute("""
            SELECT server_url, active_connections, total_requests, 
                   failed_requests, avg_response_time, timestamp
            FROM server_metrics 
            ORDER BY timestamp DESC 
            LIMIT 20
        """)
        
        server_data = cursor.fetchall()
        
        # Organize by server
        servers = {}
        for row in server_data:
            server_url, active_conn, total_req, failed_req, avg_resp_time, timestamp = row
            if server_url not in servers:
                servers[server_url] = {
                    "url": server_url,
                    "active_connections": active_conn,
                    "total_requests": total_req,
                    "failed_requests": failed_req,
                    "avg_response_time": avg_resp_time,
                    "last_update": timestamp
                }
        
        conn.close()
        
        return list(servers.values())
    
    def get_traffic_timeline(self, hours=24):
        """Get traffic timeline data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        
        cursor.execute("""
            SELECT 
                datetime(timestamp) as hour,
                COUNT(*) as total_requests,
                SUM(CASE WHEN is_malicious = 1 THEN 1 ELSE 0 END) as attacks,
                AVG(response_time) as avg_response_time
            FROM requests 
            WHERE timestamp > ?
            GROUP BY strftime('%Y-%m-%d %H:00:00', timestamp)
            ORDER BY hour
        """, (since.isoformat(),))
        
        timeline = []
        for row in cursor.fetchall():
            hour, total, attacks, avg_resp_time = row
            timeline.append({
                "time": hour,
                "total_requests": total,
                "attacks": attacks,
                "normal_requests": total - attacks,
                "avg_response_time": round(avg_resp_time or 0, 3)
            })
        
        conn.close()
        return timeline
    
    def get_attack_distribution(self):
        """Get attack type distribution"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT prediction, COUNT(*) as count
            FROM requests 
            WHERE is_malicious = 1
            GROUP BY prediction
            ORDER BY count DESC
        """)
        
        attacks = [{"type": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        conn.close()
        return attacks
    
    def get_recent_requests(self, limit=50):
        """Get recent requests"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, client_ip, method, path, server_url, 
                   status_code, response_time, is_malicious, prediction, confidence
            FROM requests 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        requests = []
        for row in cursor.fetchall():
            timestamp, client_ip, method, path, server_url, status_code, response_time, is_malicious, prediction, confidence = row
            requests.append({
                "timestamp": timestamp,
                "client_ip": client_ip,
                "method": method,
                "path": path,
                "server_url": server_url,
                "status_code": status_code,
                "response_time": response_time,
                "is_malicious": bool(is_malicious),
                "prediction": prediction,
                "confidence": confidence
            })
        
        conn.close()
        return requests

dashboard_data = DashboardData()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/servers')
def servers():
    return render_template('servers.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/api/overview')
def api_overview():
    """API endpoint for overview statistics"""
    try:
        stats = dashboard_data.get_overview_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/servers')
def api_servers():
    """API endpoint for server metrics"""
    try:
        servers = dashboard_data.get_server_metrics()
        return jsonify(servers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/timeline')
def api_timeline():
    """API endpoint for traffic timeline"""
    try:
        hours = int(request.args.get('hours', 24))
        timeline = dashboard_data.get_traffic_timeline(hours)
        return jsonify(timeline)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attacks')
def api_attacks():
    """API endpoint for attack distribution"""
    try:
        attacks = dashboard_data.get_attack_distribution()
        return jsonify(attacks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/requests')
def api_requests():
    """API endpoint for recent requests"""
    try:
        limit = int(request.args.get('limit', 50))
        requests = dashboard_data.get_recent_requests(limit)
        return jsonify(requests)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def api_health():
    """API health check"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    # Ensure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Ensure static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
