#!/bin/bash

# AI-Powered Secure Load Balancer Demo Script

set -e

echo "🎬 AI-Powered Secure Load Balancer Demo"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_status "Docker is running"
}

# Step 1: Setup
setup_demo() {
    print_step "Setting up demo environment..."
    make setup
    print_status "Setup completed"
}

# Step 2: Start services
start_services() {
    print_step "Starting all services..."
    make run
    print_status "Services started"
    
    # Wait for services to be ready
    print_warning "Waiting for services to be ready..."
    sleep 10
}

# Step 3: Health check
health_check() {
    print_step "Performing health check..."
    make health
    print_status "Health check completed"
}

# Step 4: Generate normal traffic
generate_normal_traffic() {
    print_step "Generating normal traffic..."
    
    echo "📊 Testing normal load balancing..."
    for i in {1..10}; do
        curl -s "http://localhost:8000/api/users" > /dev/null
        echo -n "."
    done
    echo ""
    
    echo "📊 Testing different endpoints..."
    curl -s "http://localhost:8000/api/products" > /dev/null
    curl -s "http://localhost:8000/api/dashboard" > /dev/null
    curl -s "http://localhost:8000/api/search?q=test" > /dev/null
    
    print_status "Normal traffic generated"
}

# Step 5: Test security features
test_security() {
    print_step "Testing security features..."
    
    echo "🛡️ Testing SQL Injection detection..."
    response=$(curl -s -w "%{http_code}" "http://localhost:8000/api/users?id=1' OR '1'='1")
    if [[ "$response" == *"403"* ]]; then
        print_status "✅ SQL Injection attack blocked"
    else
        print_warning "⚠️  SQL Injection may not have been blocked"
    fi
    
    echo "🛡️ Testing XSS detection..."
    response=$(curl -s -w "%{http_code}" "http://localhost:8000/api/search?q=<script>alert('xss')</script>")
    if [[ "$response" == *"403"* ]]; then
        print_status "✅ XSS attack blocked"
    else
        print_warning "⚠️  XSS attack may not have been blocked"
    fi
    
    echo "🛡️ Testing Path Traversal detection..."
    response=$(curl -s -w "%{http_code}" "http://localhost:8000/api/users/../../../etc/passwd")
    if [[ "$response" == *"403"* ]]; then
        print_status "✅ Path Traversal attack blocked"
    else
        print_warning "⚠️  Path Traversal attack may not have been blocked"
    fi
    
    print_status "Security testing completed"
}

# Step 6: Load testing
load_test() {
    print_step "Performing load testing..."
    
    if command -v ab >/dev/null 2>&1; then
        echo "🚀 Running Apache Bench load test..."
        ab -n 500 -c 10 http://localhost:8000/api/users
        print_status "Load test completed"
    else
        print_warning "Apache Bench (ab) not found. Skipping load test."
        echo "Install with: sudo apt-get install apache2-utils"
    fi
}

# Step 7: Show metrics
show_metrics() {
    print_step "Displaying system metrics..."
    make metrics
}

# Step 8: Open dashboard
open_dashboard() {
    print_step "Opening monitoring dashboard..."
    make dashboard
}

# Step 9: Generate mixed traffic
generate_mixed_traffic() {
    print_step "Generating mixed traffic pattern..."
    
    echo "🚦 Starting traffic generator..."
    timeout 60s make traffic || true
    print_status "Mixed traffic generation completed"
}

# Step 10: Show final stats
show_final_stats() {
    print_step "Displaying final statistics..."
    
    echo "📊 Final System Statistics:"
    echo "=========================="
    
    # Get overview from dashboard API
    if curl -s http://localhost:5000/api/overview > /dev/null 2>&1; then
        curl -s http://localhost:5000/api/overview | python -m json.tool || echo "Could not format JSON"
    else
        print_warning "Dashboard API not available"
    fi
    
    echo ""
    echo "🌐 Access Points:"
    echo "- Load Balancer: http://localhost:8000"
    echo "- Dashboard: http://localhost:5000"
    echo "- Health Check: http://localhost:8000/health"
    echo "- Metrics: http://localhost:8000/metrics"
}

# Cleanup function
cleanup() {
    print_step "Cleaning up demo environment..."
    make stop
    print_status "Cleanup completed"
}

# Main demo function
run_demo() {
    echo "Starting comprehensive demo..."
    echo ""
    
    # Run demo steps
    setup_demo
    start_services
    health_check
    generate_normal_traffic
    test_security
    load_test
    show_metrics
    open_dashboard
    generate_mixed_traffic
    show_final_stats
    
    echo ""
    print_status "🎉 Demo completed successfully!"
    echo ""
    echo "The system is now running. You can:"
    echo "- Monitor the dashboard at http://localhost:5000"
    echo "- Test the load balancer at http://localhost:8000"
    echo "- Generate more traffic with: make traffic"
    echo "- Stop everything with: make stop"
    echo ""
    echo "Press Ctrl+C to stop all services and cleanup."
    
    # Wait for user interrupt
    trap cleanup EXIT
    while true; do
        sleep 5
    done
}

# Quick demo (without cleanup)
quick_demo() {
    echo "Running quick demo..."
    echo ""
    
    check_docker
    setup_demo
    start_services
    sleep 5
    health_check
    generate_normal_traffic
    test_security
    show_metrics
    open_dashboard
    
    print_status "🎉 Quick demo completed!"
    echo "Services are running. Use 'make stop' to stop them."
}

# Help function
show_help() {
    echo "AI-Powered Secure Load Balancer Demo Script"
    echo "==========================================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  full      - Run complete demo with cleanup"
    echo "  quick     - Run quick demo (services stay running)"
    echo "  setup     - Setup demo environment only"
    echo "  start     - Start services only"
    echo "  test      - Run security tests only"
    echo "  traffic   - Generate traffic only"
    echo "  metrics   - Show metrics only"
    echo "  cleanup   - Stop and cleanup services"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 full     # Run complete demo"
    echo "  $0 quick    # Quick demo without cleanup"
    echo "  $0 test     # Just test security features"
}

# Main script logic
case "${1:-full}" in
    "full")
        check_docker
        run_demo
        ;;
    "quick")
        check_docker
        quick_demo
        ;;
    "setup")
        setup_demo
        ;;
    "start")
        check_docker
        start_services
        ;;
    "test")
        test_security
        ;;
    "traffic")
        generate_mixed_traffic
        ;;
    "metrics")
        show_metrics
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
