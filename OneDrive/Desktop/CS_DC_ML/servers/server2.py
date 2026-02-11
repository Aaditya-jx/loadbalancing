"""
Backend Server 2 - Flask Application
Port: 8002
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
SERVER_ID = "server-2"
SERVER_PORT = 8002

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
    # Different dataset for server 2
    users = [
        {"id": 4, "name": "David", "email": "david@example.com"},
        {"id": 5, "name": "Eve", "email": "eve@example.com"},
        {"id": 6, "name": "Frank", "email": "frank@example.com"}
    ]
    
    time.sleep(random.uniform(0.15, 0.35))
    
    return jsonify({
        "server_id": SERVER_ID,
        "users": users,
        "total": len(users)
    })

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    users = {
        4: {"id": 4, "name": "David", "email": "david@example.com"},
        5: {"id": 5, "name": "Eve", "email": "eve@example.com"},
        6: {"id": 6, "name": "Frank", "email": "frank@example.com"}
    }
    
    time.sleep(random.uniform(0.08, 0.25))
    
    if user_id in users:
        return jsonify({
            "server_id": SERVER_ID,
            "user": users[user_id]
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/products')
def get_products():
    # Different product catalog for server 2
    products = [
        {"id": 5, "name": "Headphones", "price": 149.99, "category": "Electronics"},
        {"id": 6, "name": "Webcam", "price": 89.99, "category": "Electronics"},
        {"id": 7, "name": "USB Hub", "price": 39.99, "category": "Electronics"},
        {"id": 8, "name": "Desk Lamp", "price": 49.99, "category": "Furniture"}
    ]
    
    time.sleep(random.uniform(0.12, 0.45))
    
    return jsonify({
        "server_id": SERVER_ID,
        "products": products,
        "total": len(products)
    })

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'GET':
        orders = [
            {"id": 201, "user_id": 4, "total": 239.98, "status": "completed"},
            {"id": 202, "user_id": 5, "total": 89.99, "status": "processing"},
            {"id": 203, "user_id": 6, "total": 189.98, "status": "shipped"}
        ]
        
        time.sleep(random.uniform(0.25, 0.55))
        
        return jsonify({
            "server_id": SERVER_ID,
            "orders": orders,
            "total": len(orders)
        })
    
    elif request.method == 'POST':
        order_data = request.get_json()
        
        time.sleep(random.uniform(0.35, 0.65))
        
        new_order = {
            "id": random.randint(2000, 2999),
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
            {"id": 3, "title": f"Server2 Result for '{query}'", "category": category or "general"},
            {"id": 4, "title": f"Server2 Another result for '{query}'", "category": category or "general"}
        ]
    
    time.sleep(random.uniform(0.15, 0.35))
    
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
        "total_users": 2180,
        "active_users": 567,
        "total_orders": 7890,
        "revenue": 234567.89,
        "server_id": SERVER_ID,
        "uptime": time.time()
    }
    
    time.sleep(random.uniform(0.22, 0.42))
    
    return jsonify(stats)

@app.route('/api/analytics')
def analytics():
    # Analytics endpoint unique to server 2
    analytics_data = {
        "page_views": 45678,
        "unique_visitors": 12345,
        "bounce_rate": 0.35,
        "avg_session_duration": 245.6,
        "conversion_rate": 0.045,
        "server_id": SERVER_ID
    }
    
    time.sleep(random.uniform(0.3, 0.6))
    
    return jsonify(analytics_data)

@app.route('/api/reports')
def reports():
    # Reports endpoint unique to server 2
    reports_data = {
        "daily_sales": [120, 145, 167, 189, 201, 223, 245],
        "weekly_traffic": [1200, 1350, 1400, 1550, 1600, 1750, 1800],
        "monthly_revenue": [45000, 48000, 52000, 49000, 53000, 56000],
        "server_id": SERVER_ID
    }
    
    time.sleep(random.uniform(0.4, 0.7))
    
    return jsonify(reports_data)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    time.sleep(random.uniform(0.6, 1.2))
    
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
