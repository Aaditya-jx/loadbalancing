# AI-Powered Secure Load Balancer Deployment Script (PowerShell)
# This script deploys the complete system using Docker Compose

Write-Host "🚀 Starting AI-Powered Secure Load Balancer Deployment..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info > $null 2>&1
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
try {
    docker-compose --version > $null 2>&1
    Write-Host "✅ Docker Compose is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose and try again." -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Blue
New-Item -ItemType Directory -Force -Path "models" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "data" | Out-Null

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down --remove-orphans

# Build and start services
Write-Host "🔨 Building and starting services..." -ForegroundColor Blue
docker-compose up --build -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Blue

# Check Load Balancer
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Load Balancer is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ Load Balancer is not responding" -ForegroundColor Red
}

# Check Dashboard
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Dashboard is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ Dashboard is not responding" -ForegroundColor Red
}

# Check Backend Servers
foreach ($port in 8001, 8002, 8003) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/health" -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ Backend Server $port is healthy" -ForegroundColor Green
    } catch {
        Write-Host "❌ Backend Server $port is not responding" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access Points:" -ForegroundColor Cyan
Write-Host "   Load Balancer:     http://localhost:8000" -ForegroundColor White
Write-Host "   Dashboard:         http://localhost:5000" -ForegroundColor White
Write-Host "   Backend Server 1:  http://localhost:8001" -ForegroundColor White
Write-Host "   Backend Server 2:  http://localhost:8002" -ForegroundColor White
Write-Host "   Backend Server 3:  http://localhost:8003" -ForegroundColor White
Write-Host ""
Write-Host "📋 Management Commands:" -ForegroundColor Cyan
Write-Host "   View logs:         docker-compose logs -f" -ForegroundColor Gray
Write-Host "   Stop services:     docker-compose down" -ForegroundColor Gray
Write-Host "   Restart services:  docker-compose restart" -ForegroundColor Gray
Write-Host "   Scale servers:     docker-compose up --scale backend-server-1=2" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Testing Commands:" -ForegroundColor Cyan
Write-Host "   Generate traffic:  docker-compose --profile testing up traffic-generator" -ForegroundColor Gray
Write-Host "   Train AI model:    docker-compose --profile training up ai-model" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 For more information, see the README.md file" -ForegroundColor Gray

# Ask if user wants to open the dashboard
$openDashboard = Read-Host "Do you want to open the dashboard in your browser? (y/n)"
if ($openDashboard -eq 'y' -or $openDashboard -eq 'Y') {
    Start-Process "http://localhost:5000"
}

# Ask if user wants to view logs
$viewLogs = Read-Host "Do you want to view the service logs? (y/n)"
if ($viewLogs -eq 'y' -or $viewLogs -eq 'Y') {
    docker-compose logs -f
}
