#!/bin/bash

# AI-Powered Secure Load Balancer - Streamlit Deployment Script
# This script deploys the complete system with Streamlit dashboard

set -e

echo "🚀 Starting AI-Powered Secure Load Balancer with Streamlit Dashboard"
echo "=================================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p models logs data

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans

# Build and start all services including Streamlit
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check Load Balancer
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Load Balancer is healthy"
else
    echo "❌ Load Balancer is not responding"
fi

# Check Streamlit Dashboard
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Streamlit Dashboard is healthy"
else
    echo "❌ Streamlit Dashboard is not responding"
fi

# Check Backend Servers
for port in 8001 8002 8003; do
    if curl -f http://localhost:$port/health > /dev/null 2>&1; then
        echo "✅ Backend Server $port is healthy"
    else
        echo "❌ Backend Server $port is not responding"
    fi
done

echo ""
echo "🎉 Deployment Complete!"
echo "=================================================================="
echo "📊 Access Points:"
echo "   🌐 Streamlit Dashboard: http://localhost:8501"
echo "   ⚖️ Load Balancer:    http://localhost:8000"
echo "   🖥️ Backend Servers:   http://localhost:8001-8003"
echo ""
echo "📋 Management Commands:"
echo "   View logs:         docker-compose logs -f"
echo "   Stop services:     docker-compose down"
echo "   Restart services:  docker-compose restart"
echo "   Scale servers:     docker-compose up --scale backend-server-1=2"
echo ""
echo "🎯 Streamlit Features:"
echo "   🔄 Real-time updates every 5 seconds"
echo "   📊 Interactive charts and visualizations"
echo "   🛡️ AI security monitoring"
echo "   🖥️ Server health monitoring"
echo "   📈 Traffic analytics"
echo ""
echo "🌐 Open your browser and navigate to:"
echo "   🎯 http://localhost:8501"
echo ""
echo "📖 For more information, see README.md and DEPLOYMENT.md"
