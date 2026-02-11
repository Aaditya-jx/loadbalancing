# AI-Powered Secure Load Balancer Demo Script (PowerShell)

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("full", "quick", "setup", "start", "test", "traffic", "metrics", "cleanup", "help")]
    [string]$Command = "full"
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor $Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Colors.Red
}

function Write-Step {
    param([string]$Message)
    Write-Host "[STEP] $Message" -ForegroundColor $Colors.Blue
}

# Check if Docker is running
function Test-DockerRunning {
    try {
        $null = docker info 2>$null
        Write-Status "Docker is running"
        return $true
    } catch {
        Write-Error "Docker is not running. Please start Docker first."
        return $false
    }
}

# Step 1: Setup
function Setup-Demo {
    Write-Step "Setting up demo environment..."
    
    # Create directories
    New-Item -ItemType Directory -Force -Path "logs", "data", "models" | Out-Null
    
    # Install dependencies
    Write-Status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Train AI model
    Write-Status "Training AI model..."
    Set-Location ai_model
    python train_model.py
    Set-Location ..
    
    Write-Status "Setup completed"
}

# Step 2: Start services
function Start-Services {
    Write-Step "Starting all services..."
    
    docker-compose up --build -d
    
    Write-Status "Services started"
    Write-Warning "Waiting for services to be ready..."
    Start-Sleep -Seconds 10
}

# Step 3: Health check
function Test-Health {
    Write-Step "Performing health check..."
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
        Write-Status "Load balancer: Healthy"
    } catch {
        Write-Warning "Load balancer: Not healthy"
    }
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -TimeoutSec 5
        Write-Status "Dashboard: Healthy"
    } catch {
        Write-Warning "Dashboard: Not healthy"
    }
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5
        Write-Status "Server 1: Healthy"
    } catch {
        Write-Warning "Server 1: Not healthy"
    }
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 5
        Write-Status "Server 2: Healthy"
    } catch {
        Write-Warning "Server 2: Not healthy"
    }
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8003/health" -TimeoutSec 5
        Write-Status "Server 3: Healthy"
    } catch {
        Write-Warning "Server 3: Not healthy"
    }
    
    Write-Status "Health check completed"
}

# Step 4: Generate normal traffic
function New-NormalTraffic {
    Write-Step "Generating normal traffic..."
    
    Write-Status "Testing normal load balancing..."
    for ($i = 1; $i -le 10; $i++) {
        try {
            $null = Invoke-RestMethod -Uri "http://localhost:8000/api/users" -TimeoutSec 5
            Write-Host "." -NoNewline
        } catch {
            Write-Host "E" -NoNewline -ForegroundColor Red
        }
    }
    Write-Host ""
    
    Write-Status "Testing different endpoints..."
    try {
        $null = Invoke-RestMethod -Uri "http://localhost:8000/api/products" -TimeoutSec 5
        $null = Invoke-RestMethod -Uri "http://localhost:8000/api/dashboard" -TimeoutSec 5
        $null = Invoke-RestMethod -Uri "http://localhost:8000/api/search?q=test" -TimeoutSec 5
    } catch {
        Write-Warning "Some endpoint tests failed"
    }
    
    Write-Status "Normal traffic generated"
}

# Step 5: Test security features
function Test-Security {
    Write-Step "Testing security features..."
    
    Write-Status "Testing SQL Injection detection..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/users?id=1' OR '1'='1" -TimeoutSec 5
        Write-Warning "SQL Injection may not have been blocked"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 403) {
            Write-Status "✅ SQL Injection attack blocked"
        } else {
            Write-Warning "SQL Injection test failed with unexpected error"
        }
    }
    
    Write-Status "Testing XSS detection..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/search?q=<script>alert('xss')</script>" -TimeoutSec 5
        Write-Warning "XSS attack may not have been blocked"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 403) {
            Write-Status "✅ XSS attack blocked"
        } else {
            Write-Warning "XSS test failed with unexpected error"
        }
    }
    
    Write-Status "Testing Path Traversal detection..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/users/../../../etc/passwd" -TimeoutSec 5
        Write-Warning "Path Traversal attack may not have been blocked"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 403) {
            Write-Status "✅ Path Traversal attack blocked"
        } else {
            Write-Warning "Path Traversal test failed with unexpected error"
        }
    }
    
    Write-Status "Security testing completed"
}

# Step 6: Load testing
function Test-Load {
    Write-Step "Performing load testing..."
    
    # Simple load test using PowerShell
    Write-Status "Running PowerShell load test..."
    $jobs = @()
    $startTime = Get-Date
    
    for ($i = 1; $i -le 100; $i++) {
        $job = Start-Job -ScriptBlock {
            try {
                $null = Invoke-RestMethod -Uri "http://localhost:8000/api/users" -TimeoutSec 10
                return 1
            } catch {
                return 0
            }
        }
        $jobs += $job
    }
    
    $results = $jobs | Wait-Job | Receive-Job
    $successCount = ($results | Where-Object { $_ -eq 1 }).Count
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    Write-Host "Load Test Results:"
    Write-Host "Total Requests: 100"
    Write-Host "Successful: $successCount"
    Write-Host "Failed: $(100 - $successCount)"
    Write-Host "Duration: $([math]::Round($duration, 2)) seconds"
    Write-Host "Requests/Second: $([math]::Round(100 / $duration, 2))"
    
    # Cleanup jobs
    $jobs | Remove-Job
    
    Write-Status "Load test completed"
}

# Step 7: Show metrics
function Show-Metrics {
    Write-Step "Displaying system metrics..."
    
    try {
        $metrics = Invoke-RestMethod -Uri "http://localhost:8000/metrics" -TimeoutSec 5
        $metrics | ConvertTo-Json -Depth 10
    } catch {
        Write-Warning "Could not fetch metrics"
    }
}

# Step 8: Open dashboard
function Open-Dashboard {
    Write-Step "Opening monitoring dashboard..."
    
    try {
        Start-Process "http://localhost:5000"
        Write-Status "Dashboard opened in browser"
    } catch {
        Write-Warning "Could not open dashboard automatically"
        Write-Host "Please open http://localhost:5000 in your browser"
    }
}

# Step 9: Generate mixed traffic
function New-MixedTraffic {
    Write-Step "Generating mixed traffic pattern..."
    
    Write-Status "Starting traffic generator..."
    try {
        # Run traffic generator for 60 seconds
        $job = Start-Job -ScriptBlock {
            Set-Location traffic
            python traffic_generator.py
        }
        
        # Wait for 60 seconds or until job completes
        $job | Wait-Job -Timeout 60 | Out-Null
        $job | Remove-Job
        
        Write-Status "Mixed traffic generation completed"
    } catch {
        Write-Warning "Traffic generation failed"
    }
}

# Step 10: Show final stats
function Show-FinalStats {
    Write-Step "Displaying final statistics..."
    
    Write-Host "📊 Final System Statistics:"
    Write-Host "=========================="
    
    try {
        $overview = Invoke-RestMethod -Uri "http://localhost:5000/api/overview" -TimeoutSec 5
        $overview | ConvertTo-Json -Depth 10
    } catch {
        Write-Warning "Dashboard API not available"
    }
    
    Write-Host ""
    Write-Host "🌐 Access Points:"
    Write-Host "- Load Balancer: http://localhost:8000"
    Write-Host "- Dashboard: http://localhost:5000"
    Write-Host "- Health Check: http://localhost:8000/health"
    Write-Host "- Metrics: http://localhost:8000/metrics"
}

# Cleanup function
function Invoke-Cleanup {
    Write-Step "Cleaning up demo environment..."
    
    try {
        docker-compose down
        Write-Status "Cleanup completed"
    } catch {
        Write-Warning "Cleanup failed"
    }
}

# Main demo function
function Invoke-FullDemo {
    Write-Host "🎬 AI-Powered Secure Load Balancer Demo" -ForegroundColor $Colors.Blue
    Write-Host "========================================" -ForegroundColor $Colors.Blue
    Write-Host ""
    
    Write-Host "Starting comprehensive demo..."
    Write-Host ""
    
    # Run demo steps
    Setup-Demo
    Start-Services
    Test-Health
    New-NormalTraffic
    Test-Security
    Test-Load
    Show-Metrics
    Open-Dashboard
    New-MixedTraffic
    Show-FinalStats
    
    Write-Host ""
    Write-Status "🎉 Demo completed successfully!"
    Write-Host ""
    Write-Host "The system is now running. You can:"
    Write-Host "- Monitor the dashboard at http://localhost:5000"
    Write-Host "- Test the load balancer at http://localhost:8000"
    Write-Host "- Generate more traffic with: .\scripts\demo.ps1 traffic"
    Write-Host "- Stop everything with: .\scripts\demo.ps1 cleanup"
    Write-Host ""
    Write-Host "Press Ctrl+C to stop all services and cleanup."
    
    # Wait for user interrupt
    try {
        while ($true) {
            Start-Sleep -Seconds 5
        }
    } catch [System.Management.Automation.HaltCommandException] {
        Invoke-Cleanup
    }
}

# Quick demo (without cleanup)
function Invoke-QuickDemo {
    Write-Host "Running quick demo..."
    Write-Host ""
    
    if (-not (Test-DockerRunning)) {
        return
    }
    
    Setup-Demo
    Start-Services
    Start-Sleep -Seconds 5
    Test-Health
    New-NormalTraffic
    Test-Security
    Show-Metrics
    Open-Dashboard
    
    Write-Status "🎉 Quick demo completed!"
    Write-Host "Services are running. Use '.\scripts\demo.ps1 cleanup' to stop them."
}

# Help function
function Show-Help {
    Write-Host "AI-Powered Secure Load Balancer Demo Script (PowerShell)"
    Write-Host "======================================================="
    Write-Host ""
    Write-Host "Usage: .\scripts\demo.ps1 [COMMAND]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  full      - Run complete demo with cleanup"
    Write-Host "  quick     - Run quick demo (services stay running)"
    Write-Host "  setup     - Setup demo environment only"
    Write-Host "  start     - Start services only"
    Write-Host "  test      - Run security tests only"
    Write-Host "  traffic   - Generate traffic only"
    Write-Host "  metrics   - Show metrics only"
    Write-Host "  cleanup   - Stop and cleanup services"
    Write-Host "  help      - Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\scripts\demo.ps1 full     # Run complete demo"
    Write-Host "  .\scripts\demo.ps1 quick    # Quick demo without cleanup"
    Write-Host "  .\scripts\demo.ps1 test     # Just test security features"
}

# Main script logic
switch ($Command) {
    "full" {
        if (Test-DockerRunning) {
            Invoke-FullDemo
        }
    }
    "quick" {
        if (Test-DockerRunning) {
            Invoke-QuickDemo
        }
    }
    "setup" {
        Setup-Demo
    }
    "start" {
        if (Test-DockerRunning) {
            Start-Services
        }
    }
    "test" {
        Test-Security
    }
    "traffic" {
        New-MixedTraffic
    }
    "metrics" {
        Show-Metrics
    }
    "cleanup" {
        Invoke-Cleanup
    }
    "help" {
        Show-Help
    }
    default {
        Write-Error "Unknown command: $Command"
        Show-Help
        exit 1
    }
}
