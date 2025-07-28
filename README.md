# TA-takehomeproj
Key Generation Service
# Key Generation Service

A lightweight HTTP service that generates cryptographically secure random keys of specified lengths, with built-in Prometheus metrics for monitoring.

## Features

- Generates random byte sequences on demand
- Configurable maximum key size
- Prometheus metrics integration
- Health checks for container orchestration
- Helm chart for Kubernetes deployment

## Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
```bash
git clone https://github.com/your-repo/key-service.git
cd key-service
Running the Service
bash
python key_server.py --srv-port 8080 --max-size 2048
Test the Service
bash
curl http://localhost:8080/key/32 | hexdump -C
curl http://localhost:8080/health
API Endpoints
Endpoint	Method	Description
/key/<length>	GET	Generate random bytes of specified length
/health	GET	Health check endpoint
/metrics	GET	Prometheus metrics
Configuration Options
Parameter	Default	Description
--srv-port	1123	HTTP server port
--max-size	1024	Maximum allowed key size
--metrics-port	8000	Prometheus metrics port
--host	0.0.0.0	Network interface to bind to
Prometheus Metrics
The service exposes these metrics at :8000/metrics:

key_length_bytes: Histogram of requested key lengths

http_responses_total: Counter of HTTP responses by status code

request_latency_seconds: Request processing latency

Sample query:

promql
# Average key size over 5m
rate(key_length_bytes_sum[5m]) / rate(key_length_bytes_count[5m])
Docker Deployment
bash
docker build -t key-service .
docker run -p 1123:1123 -p 8000:8000 key-service
Kubernetes Deployment
Install Helm: https://helm.sh/docs/intro/install/

Deploy the chart:

bash
helm install key-service ./helm-chart \
  --set server.port=1123 \
  --set server.maxSize=2048
Testing
Unit Tests
bash
python -m unittest discover
Test Cases
Valid key generation requests

Oversized key requests

Invalid length parameters

Health check validation

Metrics endpoint verification

Monitoring and Alerting
Recommended Prometheus alerts:

yaml
- alert: HighErrorRate
  expr: sum(rate(http_responses_total{status_code=~"5.."}[5m])) / sum(rate(http_responses_total[5m])) > 0.05
  for: 5m

- alert: ServiceDown
  expr: up{job="key-service"} == 0
  for: 2m