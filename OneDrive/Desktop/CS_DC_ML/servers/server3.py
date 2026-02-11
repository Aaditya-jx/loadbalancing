"""
Backend Server 3 - Flask Application
Port: 8003
"""

from flask import Flask, request, jsonify
import time
import random
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
SERVER_ID = "server-3"
SERVER_PORT = 8003

@app.route('/')
def index():
    return jsonify({
        "message": f"Hello from Backend Server {SERVER_ID}",
        "server_id": SERVER_ID,
        "port": SERVER_PORT,
        "timestamp": time.time()
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "server_id": SERVER_ID,
        "port": SERVER_PORT
    })

@app.route('/api/users')
def get_users():
    # Different dataset for server 3
    users = [
        {"id": 7, "name": "Grace", "email": "grace@example.com"},
        {"id": 8, "name": "Henry", "email": "henry@example.com"},
        {"id": 9, "name": "Iris", "email": "iris@example.com"}
    ]
    
    time.sleep(random.uniform(0.2, 0.4))
    
    return jsonify({
        "server_id": SERVER_ID,
        "users": users,
        "total": len(users)
    })

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    users = {
        7: {"id": 7, "name": "Grace", "email": "grace@example.com"},
        8: {"id": 8, "name": "Henry", "email": "henry@example.com"},
        9: {"id": 9, "name": "Iris", "email": "iris@example.com"}
    }
    
    time.sleep(random.uniform(0.1, 0.3))
    
    if user_id in users:
        return jsonify({
            "server_id": SERVER_ID,
            "user": users[user_id]
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/products')
def get_products():
    # Different product catalog for server 3
    products = [
        {"id": 9, "name": "Smartphone", "price": 699.99, "category": "Electronics"},
        {"id": 10, "name": "Tablet", "price": 399.99, "category": "Electronics"},
        {"id": 11, "name": "Smartwatch", "price": 299.99, "category": "Electronics"},
        {"id": 12, "name": "Chair", "price": 199.99, "category": "Furniture"}
    ]
    
    time.sleep(random.uniform(0.15, 0.5))
    
    return jsonify({
        "server_id": SERVER_ID,
        "products": products,
        "total": len(products)
    })

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'GET':
        orders = [
            {"id": 301, "user_id": 7, "total": 999.98, "status": "completed"},
            {"id": 302, "user_id": 8, "total": 399.99, "status": "processing"},
            {"id": 303, "user_id": 9, "total": 499.98, "status": "shipped"}
        ]
        
        time.sleep(random.uniform(0.3, 0.6))
        
        return jsonify({
            "server_id": SERVER_ID,
            "orders": orders,
            "total": len(orders)
        })
    
    elif request.method == 'POST':
        order_data = request.get_json()
        
        time.sleep(random.uniform(0.4, 0.7))
        
        new_order = {
            "id": random.randint(3000, 3999),
            "user_id": order_data.get("user_id", 1),
            "total": order_data.get("total", 0.0),
            "status": "created",
            "server_id": SERVER_ID
        }
        
        return jsonify({
            "message": "Order created successfully",
            "order": new_order
        }), 201

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    results = []
    if query:
        results = [
            {"id": 5, "title": f"Server3 Result for '{query}'", "category": category or "general"},
            {"id": 6, "title": f"Server3 Another result for '{query}'", "category": category or "general"}
        ]
    
    time.sleep(random.uniform(0.2, 0.4))
    
    return jsonify({
        "server_id": SERVER_ID,
        "query": query,
        "category": category,
        "results": results,
        "total": len(results)
    })

@app.route('/api/dashboard')
def dashboard():
    stats = {
        "total_users": 3450,
        "active_users": 789,
        "total_orders": 12345,
        "revenue": 456789.12,
        "server_id": SERVER_ID,
        "uptime": time.time()
    }
    
    time.sleep(random.uniform(0.25, 0.45))
    
    return jsonify(stats)

@app.route('/api/notifications')
def notifications():
    # Notifications endpoint unique to server 3
    notifications_data = [
        {"id": 1, "message": "New user registration", "type": "info", "timestamp": time.time()},
        {"id": 2, "message": "Order completed", "type": "success", "timestamp": time.time() - 3600},
        {"id": 3, "message": "Server maintenance scheduled", "type": "warning", "timestamp": time.time() - 7200}
    ]
    
    time.sleep(random.uniform(0.1, 0.3))
    
    return jsonify({
        "server_id": SERVER_ID,
        "notifications": notifications_data,
        "unread": len(notifications_data)
    })

@app.route('/api/settings')
def settings():
    # Settings endpoint unique to server 3
    settings_data = {
        "app_name": "Secure Load Balancer Demo",
        "version": "1.0.0",
        "maintenance_mode": False,
        "max_connections": 1000,
        "timeout": 30,
        "server_id": SERVER_ID
    }
    
    time.sleep(random.uniform(0.15, 0.35))
    
    return jsonify(settings_data)

@app.route('/api/logs')
def logs():
    # Logs endpoint unique to server 3
    logs_data = [
        {"timestamp": time.time() - 300, "level": "INFO", "message": f"Request processed on {SERVER_ID}"},
        {"timestamp": time.time() - 600, "level": "WARN", "message": f"High load detected on {SERVER_ID}"},
        {"timestamp": time.time() - 900, "level": "INFO", "message": f"Health check passed on {SERVER_ID}"}
    ]
    
    time.sleep(random.uniform(0.2, 0.4))
    
    return jsonify({
        "server_id": SERVER_ID,
        "logs": logs_data,
        "total": len(logs_data)
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    time.sleep(random.uniform(0.7, 1.4))
    
    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename,
        "server_id": SERVER_ID,
        "size": len(file.read())
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "server_id": SERVER_ID}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "server_id": SERVER_ID}), 500

if __name__ == '__main__':
    logger.info(f"Starting Backend Server {SERVER_ID} on port {SERVER_PORT}")
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=False)
