# TA-takehomeproj
Key Generation Service
🔑 Key Generation Service
A lightweight HTTP service that generates cryptographically secure random keys on demand, with built-in Prometheus metrics for monitoring and Kubernetes support for production deployments.

🚀 Quick Start
Requirements
Python 3.7+

pip package manager

Installation
bash
git clone https://github.com/your-repo/key-service.git  
cd key-service  
pip install -r requirements.txt  
Start Service
bash
python key_server.py --srv-port 8080 --max-size 2048  
Test Service
bash
# Generate 32-byte key  
curl http://localhost:8080/key/32 | hexdump -C  

# Check health  
curl http://localhost:8080/health  
# Output: OK  

# Access metrics  
curl http://localhost:8000/metrics  
🌐 API Endpoints
Endpoint	Description
GET /key/<length>	Generate random bytes (hex encoded)
GET /health	Service health check
GET /metrics	Prometheus metrics endpoint
⚙️ Configuration
Configure using command-line arguments:

bash
python key_server.py \  
  --host 0.0.0.0 \         # Bind address (default)  
  --srv-port 1123 \         # HTTP port  
  --max-size 1024 \         # Max key size in bytes  
  --metrics-port 8000       # Prometheus port  
📊 Prometheus Metrics
Access metrics at http://localhost:8000/metrics:

key_length_bytes
Histogram of requested key lengths (20 linear buckets)

http_responses_total
Counter of HTTP responses by status code

request_latency_seconds
Request processing latency distribution

Sample Queries
promql
# Average key size (5m window)  
rate(key_length_bytes_sum[5m]) / rate(key_length_bytes_count[5m])  

# Error rate  
sum(rate(http_responses_total{status_code=~"5.."}[5m]))  
/ sum(rate(http_responses_total[5m]))  
🐳 Docker Deployment
bash
# Build image  
docker build -t key-service .  

# Run container  
docker run -d \  
  -p 1123:1123 \  
  -p 8000:8000 \  
  key-service \  
  --max-size 2048  
☸️ Kubernetes Deployment
1. Install Helm
https://helm.sh/docs/intro/install/

2. Deploy Chart
bash
helm install key-service ./helm-chart \  
  --set server.port=1123 \  
  --set server.maxSize=2048  
Helm Features
Configurable resource limits

Liveness/readiness probes

ServiceMonitor for Prometheus

Horizontal pod autoscaling

🧪 Testing
Run unit tests:

bash
python -m unittest discover  
Test Cases
Test Type	Description
Valid requests	Generate keys within size limits
Size violations	Reject keys larger than max-size
Invalid parameters	Handle non-integer length values
Health checks	Verify /health endpoint
Metrics endpoint	Validate Prometheus output format
🚨 Monitoring & Alerts
Recommended Alerts
yaml
- alert: HighErrorRate  
  expr: sum(rate(http_responses_total{status_code=~"5.."}[5m])) / sum(rate(http_responses_total[5m])) > 0.05  
  labels:  
    severity: critical  
  annotations:  
    summary: "High error rate ({{ $value }})"  

- alert: ServiceDown  
  expr: up{job="key-service"} == 0  
  for: 2m  
  labels:  
    severity: critical  
Monitoring Dashboard
https://example.com/dashboard-screenshot.png
(Sample monitoring dashboard showing request rates, latency, and error percentages)

🤝 Contributing
Fork the repository

Create feature branch (git checkout -b feature/improvement)

Commit changes (git commit -am 'Add new feature')

Push to branch (git push origin feature/improvement)

Open pull request

📜 License
MIT License - See LICENSE for full text

text
Copyright 2023 Key Service Contributors  

Permission is hereby granted...  
Note: Production deployments should always:

Use HTTPS with valid certificates

Rotate API keys regularly

Set resource limits in Kubernetes

Enable Prometheus scraping

Configure alert notifications

Diagram
Code
graph LR
    A[Client] -->|HTTP GET /key/32| B(Key Server)
    B -->|Generate| C[Random Bytes]
    C -->|Return| A
    B -->|Record| D[Metrics]
    D -->|Scrape| E[Prometheus]
    E -->|Alert| F[Alertmanager]
    F -->|Notify| G[Slack/Email]
