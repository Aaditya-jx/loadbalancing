# AI-Powered Secure Load Balancer - Streamlit Deployment Script (PowerShell)
# This script deploys the complete system with Streamlit dashboard

Write-Host "🚀 Starting AI-Powered Secure Load Balancer with Streamlit Dashboard" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green

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

# Build and start all services including Streamlit
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
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Load Balancer is healthy" -ForegroundColor Green
    } else {
        Write-Host "❌ Load Balancer is not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Load Balancer is not responding" -ForegroundColor Red
}

# Check Streamlit Dashboard
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501/_stcore/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Streamlit Dashboard is healthy" -ForegroundColor Green
    } else {
        Write-Host "❌ Streamlit Dashboard is not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Streamlit Dashboard is not responding" -ForegroundColor Red
}

# Check Backend Servers
foreach ($port in 8001, 8002, 8003) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Backend Server $port is healthy" -ForegroundColor Green
        } else {
            Write-Host "❌ Backend Server $port is not responding" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Backend Server $port is not responding" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "📊 Access Points:" -ForegroundColor Cyan
Write-Host "   🌐 Streamlit Dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "   ⚖️ Load Balancer:    http://localhost:8000" -ForegroundColor White
Write-Host "   🖥️ Backend Servers:   http://localhost:8001-8003" -ForegroundColor White
Write-Host ""
Write-Host "📋 Management Commands:" -ForegroundColor Cyan
Write-Host "   View logs:         docker-compose logs -f" -ForegroundColor Gray
Write-Host "   Stop services:     docker-compose down" -ForegroundColor Gray
Write-Host "   Restart services:  docker-compose restart" -ForegroundColor Gray
Write-Host "   Scale servers:     docker-compose up --scale backend-server-1=2" -ForegroundColor Gray
Write-Host ""
Write-Host "🎯 Streamlit Features:" -ForegroundColor Cyan
Write-Host "   🔄 Real-time updates every 5 seconds" -ForegroundColor Gray
Write-Host "   📊 Interactive charts and visualizations" -ForegroundColor Gray
Write-Host "   🛡️ AI security monitoring" -ForegroundColor Gray
Write-Host "   🖥️ Server health monitoring" -ForegroundColor Gray
Write-Host "   📈 Traffic analytics" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Open your browser and navigate to:" -ForegroundColor Yellow
Write-Host "   🎯 http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "📖 For more information, see README.md and DEPLOYMENT.md" -ForegroundColor Gray

# Ask if user wants to open Streamlit dashboard
$openDashboard = Read-Host "Do you want to open the Streamlit dashboard in your browser? (y/n)" -ForegroundColor Yellow
if ($openDashboard -eq 'y' -or $openDashboard -eq 'Y') {
    Start-Process "http://localhost:8501"
}

# Ask if user wants to view logs
$viewLogs = Read-Host "Do you want to view the service logs? (y/n)" -ForegroundColor Yellow
if ($viewLogs -eq 'y' -or $viewLogs -eq 'Y') {
    Write-Host "📋 Showing live logs (press Ctrl+C to exit)..." -ForegroundColor Blue
    docker-compose logs -f
}
