# AI-Powered Secure Load Balancer Makefile

.PHONY: help setup train build run stop clean test logs dashboard traffic

# Default target
help:
	@echo "AI-Powered Secure Load Balancer - Available Commands:"
	@echo ""
	@echo "setup      - Install dependencies and train AI model"
	@echo "train      - Train the AI intrusion detection model"
	@echo "build      - Build Docker images"
	@echo "run        - Start all services with Docker"
	@echo "dev        - Start development environment"
	@echo "stop       - Stop all services"
	@echo "clean      - Clean up Docker resources"
	@echo "test       - Run tests and generate traffic"
	@echo "logs       - Show logs from all services"
	@echo "dashboard  - Open dashboard in browser"
	@echo "traffic    - Generate test traffic"

# Setup project
setup:
	@echo "🚀 Setting up AI-Powered Secure Load Balancer..."
	@mkdir -p logs data models config
	@pip install -r requirements.txt
	@$(MAKE) train
	@echo "✅ Setup completed!"

# Train AI model
train:
	@echo "🤖 Training AI intrusion detection model..."
	@cd ai_model && python train_model.py
	@echo "✅ Model training completed!"

# Build Docker images
build:
	@echo "🐳 Building Docker images..."
	@docker-compose build
	@echo "✅ Build completed!"

# Run production services
run:
	@echo "🚀 Starting production services..."
	@docker-compose up --build -d
	@echo "✅ Services started!"
	@echo "Load Balancer: http://localhost:8000"
	@echo "Dashboard: http://localhost:5000"

# Run development services
dev:
	@echo "🔧 Starting development services..."
	@docker-compose -f docker-compose.dev.yml up --build -d
	@echo "✅ Development services started!"
	@echo "Load Balancer: http://localhost:8000"
	@echo "Dashboard: http://localhost:5000"

# Stop services
stop:
	@echo "🛑 Stopping services..."
	@docker-compose down
	@docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
	@echo "✅ Services stopped!"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@docker-compose down -v
	@docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true
	@docker system prune -f
	@docker volume prune -f
	@echo "✅ Cleanup completed!"

# Run tests
test:
	@echo "🧪 Running tests..."
	@$(MAKE) traffic
	@echo "✅ Tests completed!"

# Generate traffic
traffic:
	@echo "🚦 Generating test traffic..."
	@docker-compose --profile testing up traffic-generator --build

# Show logs
logs:
	@echo "📋 Showing logs..."
	@docker-compose logs -f

# Dashboard logs
dashboard-logs:
	@echo "📊 Dashboard logs..."
	@docker-compose logs -f dashboard

# Load balancer logs
lb-logs:
	@echo "⚖️ Load balancer logs..."
	@docker-compose logs -f load-balancer

# Server logs
server-logs:
	@echo "🖥️ Server logs..."
	@docker-compose logs -f backend-server-1 backend-server-2 backend-server-3

# Open dashboard
dashboard:
	@echo "🌐 Opening dashboard..."
	@python -c "import webbrowser; webbrowser.open('http://localhost:5000')" 2>/dev/null || echo "Please open http://localhost:5000 in your browser"

# Health check
health:
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health || echo "❌ Load balancer not healthy"
	@curl -f http://localhost:5000/api/health || echo "❌ Dashboard not healthy"
	@curl -f http://localhost:8001/health || echo "❌ Server 1 not healthy"
	@curl -f http://localhost:8002/health || echo "❌ Server 2 not healthy"
	@curl -f http://localhost:8003/health || echo "❌ Server 3 not healthy"

# Metrics
metrics:
	@echo "📊 System metrics:"
	@curl -s http://localhost:8000/metrics | python -m json.tool || echo "❌ Could not fetch metrics"

# Quick test
quick-test:
	@echo "⚡ Quick test..."
	@echo "Testing normal request..."
	@curl -w "Time: %{time_total}s\n" -s http://localhost:8000/api/users > /dev/null
	@echo "Testing security..."
	@curl -w "Time: %{time_total}s\n" -s "http://localhost:8000/api/users?id=1' OR '1'='1" > /dev/null
	@echo "✅ Quick test completed!"

# Performance test
perf-test:
	@echo "🚀 Performance test..."
	@echo "Testing 1000 requests..."
	@if command -v ab >/dev/null 2>&1; then \
		ab -n 1000 -c 10 http://localhost:8000/api/users; \
	else \
		echo "Apache Bench (ab) not found. Install it for performance testing."; \
	fi

# Development setup (local)
dev-setup:
	@echo "🔧 Setting up local development environment..."
	@mkdir -p logs data models
	@pip install -r requirements.txt
	@echo "✅ Local development setup completed!"
	@echo "Run './start_servers.sh' to start backend servers"
	@echo "Run './start_load_balancer.sh' to start load balancer"
	@echo "Run './start_dashboard.sh' to start dashboard"

# Full reset
reset: clean
	@echo "🔄 Full reset..."
	@rm -rf logs/* data/* models/*
	@mkdir -p logs data models
	@$(MAKE) setup
	@echo "✅ Full reset completed!"

# Backup data
backup:
	@echo "💾 Backing up data..."
	@tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz logs/ data/ models/
	@echo "✅ Backup completed!"

# Development server (local)
dev-servers:
	@echo "🖥️ Starting local development servers..."
	@cd servers && python server1.py & \
	cd servers && python server2.py & \
	cd servers && python server3.py & \
	echo "✅ Servers started in background"

# Development load balancer (local)
dev-lb:
	@echo "⚖️ Starting local development load balancer..."
	@cd load_balancer && python load_balancer.py

# Development dashboard (local)
dev-dashboard:
	@echo "📊 Starting local development dashboard..."
	@cd dashboard && python app.py

# Install development tools
install-tools:
	@echo "🛠️ Installing development tools..."
	@pip install black flake8 pytest pytest-cov
	@echo "✅ Development tools installed!"

# Code formatting
format:
	@echo "🎨 Formatting code..."
	@black ai_model/ load_balancer/ servers/ traffic/ dashboard/
	@echo "✅ Code formatted!"

# Linting
lint:
	@echo "🔍 Linting code..."
	@flake8 ai_model/ load_balancer/ servers/ traffic/ dashboard/ --max-line-length=100
	@echo "✅ Linting completed!"

# Run all checks
check: format lint test
	@echo "✅ All checks completed!"
