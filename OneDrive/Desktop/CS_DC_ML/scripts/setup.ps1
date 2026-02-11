# AI-Powered Secure Load Balancer Setup Script (PowerShell)

Write-Host "🚀 Setting up AI-Powered Secure Load Balancer..." -ForegroundColor Green

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Blue
New-Item -ItemType Directory -Force -Path "logs", "data", "models", "config" | Out-Null

# Check Python version
Write-Host "🐍 Checking Python version..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue
try {
    pip install -r requirements.txt
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Train AI model
Write-Host "🤖 Training AI intrusion detection model..." -ForegroundColor Blue
try {
    Set-Location ai_model
    python train_model.py
    Set-Location ..
    Write-Host "✅ AI model training completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to train AI model" -ForegroundColor Red
    exit 1
}

# Create startup scripts
Write-Host "📜 Creating startup scripts..." -ForegroundColor Blue

# Load balancer startup script
$loadBalancerScript = @'
@echo off
echo 🚀 Starting Secure Load Balancer...
cd load_balancer
python load_balancer.py
'@
Out-File -FilePath "start_load_balancer.bat" -Encoding ASCII -InputObject $loadBalancerScript

# Servers startup script
$serversScript = @'
@echo off
echo 🚀 Starting Backend Servers...
cd servers

start "Server 1" python server1.py
start "Server 2" python server2.py
start "Server 3" python server3.py

echo ✅ Servers started!
echo Press any key to stop all servers...
pause > nul

taskkill /f /im python.exe
'@
Out-File -FilePath "start_servers.bat" -Encoding ASCII -InputObject $serversScript

# Dashboard startup script
$dashboardScript = @'
@echo off
echo 🚀 Starting Dashboard...
cd dashboard
python app.py
'@
Out-File -FilePath "start_dashboard.bat" -Encoding ASCII -InputObject $dashboardScript

# Traffic generator script
$trafficScript = @'
@echo off
echo 🚀 Generating Traffic...
cd traffic
python traffic_generator.py
'@
Out-File -FilePath "generate_traffic.bat" -Encoding ASCII -InputObject $trafficScript

# Docker startup script
$dockerStartScript = @'
@echo off
echo 🐳 Starting with Docker...
docker-compose up --build -d

echo ✅ Services started!
echo Load Balancer: http://localhost:8000
echo Dashboard: http://localhost:5000
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
'@
Out-File -FilePath "docker_start.bat" -Encoding ASCII -InputObject $dockerStartScript

# Docker stop script
$dockerStopScript = @'
@echo off
echo 🛑 Stopping Docker services...
docker-compose down
echo ✅ Services stopped!
'@
Out-File -FilePath "docker_stop.bat" -Encoding ASCII -InputObject $dockerStopScript

Write-Host "✅ Startup scripts created!" -ForegroundColor Green

# Create performance test script
$perfTestScript = @'
@echo off
echo ⚡ Running Performance Test...

echo 📊 Testing normal load balancing...
curl -s http://localhost:8000/api/users > nul

echo 🛡️ Testing security features...
curl -s "http://localhost:8000/api/users?id=1' OR '1'='1" > nul

echo ✅ Performance test completed!
'@
Out-File -FilePath "performance_test.bat" -Encoding ASCII -InputObject $perfTestScript

Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "1. Start backend servers: start_servers.bat"
Write-Host "2. Start load balancer: start_load_balancer.bat"
Write-Host "3. Start dashboard: start_dashboard.bat"
Write-Host "4. Generate traffic: generate_traffic.bat"
Write-Host ""
Write-Host "🐳 Or use Docker:" -ForegroundColor Yellow
Write-Host "1. Start all services: docker_start.bat"
Write-Host "2. Stop all services: docker_stop.bat"
Write-Host ""
Write-Host "🌐 Access points:" -ForegroundColor Yellow
Write-Host "- Load Balancer: http://localhost:8000"
Write-Host "- Dashboard: http://localhost:5000"
Write-Host "- Health Check: http://localhost:8000/health"
Write-Host "- Metrics: http://localhost:8000/metrics"
