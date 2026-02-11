#!/bin/bash

# AI-Powered Secure Load Balancer Setup Script

set -e

echo "🚀 Setting up AI-Powered Secure Load Balancer..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data models config

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version OK: $python_version"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Train AI model
echo "🤖 Training AI intrusion detection model..."
cd ai_model
python3 train_model.py
cd ..

echo "✅ AI model training completed!"

# Create startup scripts
echo "📜 Creating startup scripts..."

# Load balancer startup script
cat > start_load_balancer.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Secure Load Balancer..."
cd load_balancer
python3 load_balancer.py
EOF

# Servers startup script
cat > start_servers.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Backend Servers..."
cd servers

# Start servers in background
python3 server1.py &
SERVER1_PID=$!

python3 server2.py &
SERVER2_PID=$!

python3 server3.py &
SERVER3_PID=$!

echo "✅ Servers started!"
echo "Server 1 PID: $SERVER1_PID"
echo "Server 2 PID: $SERVER2_PID"
echo "Server 3 PID: $SERVER3_PID"

# Wait for user input to stop
echo "Press Ctrl+C to stop all servers..."
trap "kill $SERVER1_PID $SERVER2_PID $SERVER3_PID; exit" INT
wait
EOF

# Dashboard startup script
cat > start_dashboard.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Dashboard..."
cd dashboard
python3 app.py
EOF

# Traffic generator script
cat > generate_traffic.sh << 'EOF'
#!/bin/bash
echo "🚀 Generating Traffic..."
cd traffic
python3 traffic_generator.py
EOF

# Make scripts executable
chmod +x start_load_balancer.sh start_servers.sh start_dashboard.sh generate_traffic.sh

echo "✅ Startup scripts created!"

# Create Docker startup script
cat > docker_start.sh << 'EOF'
#!/bin/bash
echo "🐳 Starting with Docker..."

# Build and start services
docker-compose up --build -d

echo "✅ Services started!"
echo "Load Balancer: http://localhost:8000"
echo "Dashboard: http://localhost:5000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
EOF

chmod +x docker_start.sh

# Create Docker stop script
cat > docker_stop.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping Docker services..."
docker-compose down
echo "✅ Services stopped!"
EOF

chmod +x docker_stop.sh

echo "✅ Docker scripts created!"

# Create performance test script
cat > performance_test.sh << 'EOF'
#!/bin/bash
echo "⚡ Running Performance Test..."

# Test normal load balancing
echo "📊 Testing normal load balancing..."
curl -w "@curl-format.txt" -s http://localhost:8000/api/users > /dev/null

# Test with security enabled
echo "🛡️ Testing security features..."
curl -w "@curl-format.txt" -s "http://localhost:8000/api/users?id=1' OR '1'='1" > /dev/null

echo "✅ Performance test completed!"
EOF

# Create curl format file
cat > curl-format.txt << 'EOF'
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
EOF

chmod +x performance_test.sh

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Start backend servers: ./start_servers.sh"
echo "2. Start load balancer: ./start_load_balancer.sh"
echo "3. Start dashboard: ./start_dashboard.sh"
echo "4. Generate traffic: ./generate_traffic.sh"
echo ""
echo "🐳 Or use Docker:"
echo "1. Start all services: ./docker_start.sh"
echo "2. Stop all services: ./docker_stop.sh"
echo ""
echo "🌐 Access points:"
echo "- Load Balancer: http://localhost:8000"
echo "- Dashboard: http://localhost:5000"
echo "- Health Check: http://localhost:8000/health"
echo "- Metrics: http://localhost:8000/metrics"
