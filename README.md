# Key Generation Service
🔑 Key Generation Service

A lightweight HTTP service that generates cryptographically secure random keys on demand, with built-in Prometheus metrics for monitoring and Kubernetes support for production deployments.

🚀 Quick Start
```
Requirements
Python 3.7+

pip package manager
```
## Installation
```
git clone https://github.com/ShirleyXYW/TA-takehomeproj.git
cd TA-takehomeproj
```
## Start Service
```
python key_server.py --srv-port 1123 --max-size 1024 
```
## Test Service
```
python test.py
```
## Generate 32-byte key  
```
curl http://localhost:1123/key/32
```
## Check health 
```
curl http://localhost:1123/health
```

## Access metrics  
```
curl http://localhost:8000/metrics
```
🌐 API Endpoints
### Endpoint Description
```
GET /key/<length>: Generate random bytes
GET /health: Service health check
GET /metrics: Prometheus metrics endpoint
```
⚙️ Configuration
```
Configure using command-line arguments:
python key_server.py \  
  --host 0.0.0.0 \         # Bind address (default)  
  --srv-port 1123 \         # HTTP port  
  --max-size 1024 \         # Max key size in bytes  
  --metrics-port 8000       # Prometheus port
```
📊 Prometheus Metrics
```
Access metrics at http://localhost:8000/metrics:
```
🐳 Docker Deployment
```
# Build image  
docker build -t key-service .  
```
# Run container  
```
docker run -d \  
  -p 1123:1123 \  
  -p 8000:8000 \  
  key-service \  
  --max-size 1024
```
☸️ Kubernetes Deployment
### Install Helm
```
https://helm.sh/docs/intro/install/
```
### Deploy Chart
```
helm install key-service ./helm-chart \  
  --set server.port=1123 \  
  --set server.maxSize=1024
```
### Helm Features
```
Configurable resource limits

Liveness/readiness probes

ServiceMonitor for Prometheus

Horizontal pod autoscaling
```

🧪 Testing
```
- Valid requests: Generate keys within size limits
- Size violations: Reject keys larger than max-size
- Health checks: Verify /health endpoint
```
🚨 Monitoring & Alerts
### Recommended Alerts
Ideally we would want to record the positive metrics(uptime, availability, response time, successful rate, 200 code rate..) and negative metrics(latency, error rate, non-200 code rate, downtime..) as well as some other metrics(Disk usage, CPU usage, memory usage, cache(if any) hit ratio..).
