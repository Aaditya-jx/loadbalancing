# 🚀 AI-Powered Secure Load Balancer - Deployment Guide

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Manual Deployment](#manual-deployment)
- [Docker Deployment](#docker-deployment)
- [Service Configuration](#service-configuration)
- [Monitoring & Management](#monitoring--management)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

## 🔧 Prerequisites

### Required Software
- **Docker Desktop** (v20.10+)
- **Docker Compose** (v2.0+)
- **Git** (for cloning)
- **PowerShell** (Windows) or **Bash** (Linux/Mac)

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 10GB free space
- **CPU**: Minimum 2 cores, Recommended 4+ cores
- **Network**: Internet connection for package downloads

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CS_DC_ML
```

### 2. Deploy with PowerShell (Windows)
```powershell
.\deploy.ps1
```

### 3. Deploy with Bash (Linux/Mac)
```bash
chmod +x deploy.sh
./deploy.sh
```

### 4. Access the System
- **Dashboard**: http://localhost:5000
- **Load Balancer**: http://localhost:8000
- **Backend Servers**: http://localhost:8001-8003

## 🐳 Docker Deployment

### Using Docker Compose

#### Build and Start All Services
```bash
docker-compose up --build -d
```

#### Start Specific Services
```bash
# Start only core services
docker-compose up -d load-balancer backend-server-1 backend-server-2 backend-server-3 dashboard

# Start with traffic generator for testing
docker-compose --profile testing up -d

# Start with AI model training
docker-compose --profile training up -d
```

#### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

#### View Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f load-balancer
docker-compose logs -f dashboard
```

### Service Health Checks
```bash
# Check all services
docker-compose ps

# Check specific service health
curl http://localhost:8000/health  # Load Balancer
curl http://localhost:5000/api/health  # Dashboard
curl http://localhost:8001/health  # Backend Server 1
```

## 📊 Service Configuration

### Load Balancer
- **Port**: 8000
- **Algorithm**: Least Connections
- **AI Security**: Enabled
- **Health Check**: Every 30 seconds

### Backend Servers
- **Server 1**: Port 8001
- **Server 2**: Port 8002  
- **Server 3**: Port 8003
- **Health Check**: Every 30 seconds

### Dashboard
- **Port**: 5000
- **Database**: SQLite (logs/load_balancer.db)
- **Real-time Updates**: Every 5 seconds

### Environment Variables
Copy `env.example` to `.env` and modify as needed:

```bash
# Load Balancer Settings
ENABLE_AI_SECURITY=true
MODEL_CONFIDENCE_THRESHOLD=0.7
LB_ALGORITHM=least_connections

# Database Settings
SQLITE_DB_PATH=/app/logs/load_balancer.db

# Performance Settings
MAX_CONNECTIONS=1000
CONNECTION_TIMEOUT=30
```

## 📈 Monitoring & Management

### Dashboard Features
- **Real-time Metrics**: Live system monitoring
- **Multi-page Interface**: Analytics, Security, Servers, Logs
- **Interactive Charts**: Traffic patterns, attack detection
- **Server Management**: Health monitoring and control

### Management Commands

#### Scaling Services
```bash
# Scale backend servers
docker-compose up --scale backend-server-1=2 --scale backend-server-2=2

# Scale traffic generation
docker-compose up --scale traffic-generator=3
```

#### Service Updates
```bash
# Update specific service
docker-compose up --build -d load-balancer

# Update all services
docker-compose up --build -d
```

#### Backup and Restore
```bash
# Backup database
docker cp secure-lb-dashboard:/app/logs/load_balancer.db ./backup/

# Restore database
docker cp ./backup/load_balancer.db secure-lb-dashboard:/app/logs/
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Docker Desktop Not Running
**Solution**: Start Docker Desktop and wait for it to fully initialize.

#### 2. Port Conflicts
**Error**: `Port already in use`
**Solution**: 
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

#### 3. Build Failures
**Error**: `ModuleNotFoundError` or dependency issues
**Solution**:
```bash
# Clean rebuild
docker-compose down --rmi all
docker-compose up --build -d
```

#### 4. Health Check Failures
**Error**: Services showing unhealthy
**Solution**:
```bash
# Check service logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>
```

#### 5. Database Issues
**Error**: `unable to open database file`
**Solution**:
```bash
# Create logs directory
mkdir -p logs

# Check permissions
docker-compose exec dashboard ls -la /app/logs/
```

### Performance Issues

#### High Memory Usage
```bash
# Monitor resource usage
docker stats

# Optimize Docker memory limits
# In Docker Desktop: Settings > Resources > Memory
```

#### Slow Response Times
```bash
# Check service health
curl -w "@curl-format.txt" http://localhost:8000/health

# Monitor logs for errors
docker-compose logs -f load-balancer
```

## 🏭 Production Deployment

### Security Considerations

#### 1. Environment Configuration
```bash
# Use production environment
ENV NODE_ENV=production

# Set secure secrets
SECRET_KEY=<your-secret-key>
DB_PASSWORD=<secure-password>
```

#### 2. Network Security
```bash
# Use custom networks
docker network create --driver bridge secure-lb-prod

# Expose only necessary ports
ports:
  - "80:8000"  # Load Balancer
  - "443:5000" # Dashboard (HTTPS)
```

#### 3. SSL/TLS Configuration
```bash
# Enable HTTPS
docker-compose --profile production up -d nginx

# Configure SSL certificates
# Place certificates in nginx/ssl/
```

### Performance Optimization

#### 1. Resource Limits
```yaml
services:
  load-balancer:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

#### 2. Database Optimization
```bash
# Use PostgreSQL for production
# Configure connection pooling
# Enable query logging
```

#### 3. Caching
```bash
# Add Redis for caching
# Configure application cache
# Enable CDN for static assets
```

### Monitoring and Logging

#### 1. Centralized Logging
```bash
# Use ELK stack or similar
# Configure log aggregation
# Set up log rotation
```

#### 2. Metrics Collection
```bash
# Enable Prometheus metrics
# Configure Grafana dashboards
# Set up alerting
```

#### 3. Health Monitoring
```bash
# External health checks
# Uptime monitoring
# Performance metrics
```

## 📞 Support

### Getting Help
- **Documentation**: Check this guide and README.md
- **Logs**: Use `docker-compose logs` for troubleshooting
- **Health Checks**: Verify all services are healthy
- **Community**: Check issues and discussions

### Emergency Procedures

#### System Recovery
```bash
# Full system restart
docker-compose down
docker-compose up --build -d

# Data recovery from backup
docker cp backup/load_balancer.db secure-lb-dashboard:/app/logs/
docker-compose restart dashboard
```

#### Service Isolation
```bash
# Stop problematic service
docker-compose stop <service-name>

# Run service independently
docker run -p 8000:8000 cs_dc_ml-load-balancer
```

## 🔄 Updates and Maintenance

### Regular Maintenance
1. **Update dependencies**: Update requirements.txt
2. **Security patches**: Update base Docker images
3. **Database maintenance**: Clean old logs, optimize indexes
4. **Performance tuning**: Monitor and adjust resource limits

### Update Process
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d

# Verify health
docker-compose ps
curl http://localhost:8000/health
```

---

## 🎉 Success!

Your AI-Powered Secure Load Balancer is now deployed and running! 

### Next Steps:
1. **Explore the Dashboard**: Visit http://localhost:5000
2. **Generate Traffic**: Use the traffic generator for testing
3. **Monitor Performance**: Check system metrics and logs
4. **Customize Configuration**: Modify environment variables as needed

For more information, see the [README.md](README.md) file or check the project documentation.
