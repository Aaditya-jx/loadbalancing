#!/bin/bash

# AI-Powered Secure Load Balancer Deployment Script
# This script deploys the complete system using Docker Compose

set -e

echo "🚀 Starting AI-Powered Secure Load Balancer Deployment..."

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

# Build and start services
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

# Check Dashboard
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ Dashboard is healthy"
else
    echo "❌ Dashboard is not responding"
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
echo ""
echo "📊 Access Points:"
echo "   Load Balancer:     http://localhost:8000"
echo "   Dashboard:         http://localhost:5000"
echo "   Backend Server 1:  http://localhost:8001"
echo "   Backend Server 2:  http://localhost:8002"
echo "   Backend Server 3:  http://localhost:8003"
echo ""
echo "📋 Management Commands:"
echo "   View logs:         docker-compose logs -f"
echo "   Stop services:     docker-compose down"
echo "   Restart services:  docker-compose restart"
echo "   Scale servers:     docker-compose up --scale backend-server-1=2"
echo ""
echo "🔧 Testing Commands:"
echo "   Generate traffic:  docker-compose --profile testing up traffic-generator"
echo "   Train AI model:    docker-compose --profile training up ai-model"
echo ""
echo "📖 For more information, see the README.md file"
