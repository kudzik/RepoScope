# RepoScope Deployment Guide

Complete guide for deploying RepoScope in various environments.

## 🚀 Quick Deployment

### Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🐳 Docker Deployment

### Dockerfile (Backend)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
```

### Dockerfile (Frontend)

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - '8000:8000'
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - '3000:3000'
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Instance

```bash
# Launch EC2 instance (Ubuntu 20.04)
# Install dependencies
sudo apt update
sudo apt install python3-pip nodejs npm nginx

# Clone repository
git clone https://github.com/your-org/reposcope.git
cd reposcope

# Backend setup
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
npm run build

# Configure Nginx
sudo nano /etc/nginx/sites-available/reposcope
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### Systemd Services

```ini
# /etc/systemd/system/reposcope-backend.service
[Unit]
Description=RepoScope Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/reposcope/backend
Environment=PATH=/home/ubuntu/reposcope/backend/.venv/bin
ExecStart=/home/ubuntu/reposcope/backend/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Google Cloud Platform

#### App Engine (Backend)

```yaml
# app.yaml
runtime: python39
service: backend

env_variables:
  ENVIRONMENT: production
  LOG_LEVEL: info

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

handlers:
  - url: /.*
    script: auto
```

#### Cloud Run (Frontend)

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

EXPOSE 8080
CMD ["npm", "start"]
```

### Azure Deployment

#### Azure App Service

```bash
# Create resource group
az group create --name reposcope-rg --location eastus

# Create app service plan
az appservice plan create --name reposcope-plan --resource-group reposcope-rg --sku B1

# Create web app
az webapp create --name reposcope-app --resource-group reposcope-rg --plan reposcope-plan --runtime "PYTHON|3.9"
```

#### Azure Container Instances

```yaml
# azure-deploy.yml
apiVersion: 2018-10-01
location: eastus
name: reposcope
properties:
  containers:
    - name: backend
      properties:
        image: reposcope/backend:latest
        ports:
          - port: 8000
        resources:
          requests:
            cpu: 1
            memoryInGb: 1
    - name: frontend
      properties:
        image: reposcope/frontend:latest
        ports:
          - port: 3000
        resources:
          requests:
            cpu: 1
            memoryInGb: 1
  osType: Linux
  ipAddress:
    type: Public
    ports:
      - protocol: tcp
        port: 80
      - protocol: tcp
        port: 8000
```

## 🚀 Production Deployment

### Environment Configuration

#### Backend Environment

```bash
# .env.production
ENVIRONMENT=production
LOG_LEVEL=info
MAX_REPOSITORY_SIZE_MB=50
ANALYSIS_TIMEOUT_SECONDS=120
CACHE_TTL_HOURS=24
REDIS_URL=redis://localhost:6379
```

#### Frontend Environment

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.reposcope.com
NEXT_PUBLIC_APP_NAME=RepoScope
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ANALYTICS_ID=GA-XXXXXXXXX
```

### Production Checklist

#### Security

- [ ] HTTPS enabled with valid SSL certificate
- [ ] Environment variables secured
- [ ] API rate limiting configured
- [ ] Input validation implemented
- [ ] CORS properly configured

#### Performance

- [ ] CDN configured for static assets
- [ ] Database connection pooling
- [ ] Caching strategy implemented
- [ ] Load balancing configured
- [ ] Monitoring and alerting setup

#### Monitoring

- [ ] Application logs centralized
- [ ] Error tracking (Sentry, etc.)
- [ ] Performance monitoring
- [ ] Health checks configured
- [ ] Backup strategy implemented

## 🔧 Configuration Management

### Environment Variables

#### Backend Configuration

```python
# config.py
import os
from typing import Optional

class Settings:
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "info")
    max_repository_size_mb: int = int(os.getenv("MAX_REPOSITORY_SIZE_MB", "50"))
    analysis_timeout_seconds: int = int(os.getenv("ANALYSIS_TIMEOUT_SECONDS", "120"))
    cache_ttl_hours: int = int(os.getenv("CACHE_TTL_HOURS", "24"))
    redis_url: Optional[str] = os.getenv("REDIS_URL")

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./reposcope.db")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key")
    cors_origins: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

settings = Settings()
```

#### Frontend Configuration

```typescript
// config.ts
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  appName: process.env.NEXT_PUBLIC_APP_NAME || 'RepoScope',
  appVersion: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  analyticsId: process.env.NEXT_PUBLIC_ANALYTICS_ID,
  environment: process.env.NODE_ENV || 'development',
};
```

## 📊 Monitoring and Logging

### Application Monitoring

```python
# monitoring.py
import logging
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logging.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"{func.__name__} failed after {duration:.2f}s: {str(e)}")
            raise
    return wrapper
```

### Health Checks

```python
# health.py
from fastapi import APIRouter, HTTPException
import psutil
import time

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        # Check application health
        uptime = time.time() - start_time

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "uptime": uptime,
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

## 🔒 Security Considerations

### SSL/TLS Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
```

### API Security

```python
# security.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## 📈 Scaling Considerations

### Horizontal Scaling

- **Load Balancer**: Distribute requests across multiple instances
- **Database**: Use read replicas for query distribution
- **Caching**: Redis cluster for distributed caching
- **CDN**: CloudFront or CloudFlare for static assets

### Vertical Scaling

- **CPU**: Increase instance size for compute-intensive analysis
- **Memory**: Add RAM for large repository processing
- **Storage**: SSD storage for faster I/O operations
- **Network**: High-bandwidth connections for data transfer

## 🚨 Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump -h localhost -U username -d reposcope > backup.sql

# Restore
psql -h localhost -U username -d reposcope < backup.sql
```

### Application Backup

```bash
# Backup application files
tar -czf reposcope-backup-$(date +%Y%m%d).tar.gz /opt/reposcope/

# Backup configuration
cp -r /etc/reposcope/ /backup/config/
```

### Disaster Recovery

1. **RTO**: Recovery Time Objective < 4 hours
2. **RPO**: Recovery Point Objective < 1 hour
3. **Backup Frequency**: Daily automated backups
4. **Testing**: Monthly disaster recovery drills

## 👨‍💻 Author

**Artur Kud** - kudzik@outlook.com

---

For more information, see the main [README.md](README.md) file or contact Artur Kud at kudzik@outlook.com.
