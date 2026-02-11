"""
Backend Server 1 - Flask Application
Port: 8001
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
SERVER_ID = "server-1"
SERVER_PORT = 8001

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
    # Simulate database query
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]
    
    # Simulate processing time
    time.sleep(random.uniform(0.1, 0.3))
    
    return jsonify({
        "server_id": SERVER_ID,
        "users": users,
        "total": len(users)
    })

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    # Simulate database query
    users = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
        3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    }
    
    time.sleep(random.uniform(0.05, 0.2))
    
    if user_id in users:
        return jsonify({
            "server_id": SERVER_ID,
            "user": users[user_id]
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/products')
def get_products():
    # Simulate product catalog
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
        {"id": 2, "name": "Mouse", "price": 29.99, "category": "Electronics"},
        {"id": 3, "name": "Keyboard", "price": 79.99, "category": "Electronics"},
        {"id": 4, "name": "Monitor", "price": 299.99, "category": "Electronics"}
    ]
    
    time.sleep(random.uniform(0.1, 0.4))
    
    return jsonify({
        "server_id": SERVER_ID,
        "products": products,
        "total": len(products)
    })

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'GET':
        # Simulate order retrieval
        orders = [
            {"id": 101, "user_id": 1, "total": 109.98, "status": "completed"},
            {"id": 102, "user_id": 2, "total": 79.99, "status": "processing"},
            {"id": 103, "user_id": 3, "total": 379.98, "status": "shipped"}
        ]
        
        time.sleep(random.uniform(0.2, 0.5))
        
        return jsonify({
            "server_id": SERVER_ID,
            "orders": orders,
            "total": len(orders)
        })
    
    elif request.method == 'POST':
        # Simulate order creation
        order_data = request.get_json()
        
        time.sleep(random.uniform(0.3, 0.6))
        
        new_order = {
            "id": random.randint(1000, 9999),
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
    
    # Simulate search functionality
    results = []
    if query:
        results = [
            {"id": 1, "title": f"Result for '{query}' - {SERVER_ID}", "category": category or "general"},
            {"id": 2, "title": f"Another result for '{query}' - {SERVER_ID}", "category": category or "general"}
        ]
    
    time.sleep(random.uniform(0.1, 0.3))
    
    return jsonify({
        "server_id": SERVER_ID,
        "query": query,
        "category": category,
        "results": results,
        "total": len(results)
    })

@app.route('/api/dashboard')
def dashboard():
    # Simulate dashboard data
    stats = {
        "total_users": 1250,
        "active_users": 342,
        "total_orders": 4567,
        "revenue": 125432.50,
        "server_id": SERVER_ID,
        "uptime": time.time()
    }
    
    time.sleep(random.uniform(0.2, 0.4))
    
    return jsonify(stats)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Simulate file upload
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Simulate processing time
    time.sleep(random.uniform(0.5, 1.0))
    
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
