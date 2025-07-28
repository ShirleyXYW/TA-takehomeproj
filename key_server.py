import argparse
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from prometheus_client import start_http_server, Counter, Histogram

# Prometheus metrics
# Will be initialized later
KEY_LENGTH_HISTOGRAM = None

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency',
    ['endpoint']
)
HTTP_RESPONSES = Counter(
    'http_responses_total',
    'Total HTTP Responses',
    ['status_code']
)

class KeyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        try:
            if self.path == '/health':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
                REQUEST_LATENCY.labels('/health').observe(time.time() - start_time)
                HTTP_RESPONSES.labels('200').inc()
                return
                
            if self.path == '/metrics':
                REQUEST_LATENCY.labels('/metrics').observe(time.time() - start_time)
                HTTP_RESPONSES.labels('200').inc()
                return super().do_GET()
                
            if not self.path.startswith('/key/'):
                self.send_error(404, "Path not found")
                HTTP_RESPONSES.labels('404').inc()
                return
            
            length_str = self.path.split('/')[-1]
            try:
                length = int(length_str)
            except ValueError:
                self.send_error(400, "Invalid length: must be an integer")
                HTTP_RESPONSES.labels('400').inc()
                return
            
            if length < 1:
                self.send_error(400, "Length must be at least 1")
                HTTP_RESPONSES.labels('400').inc()
                return
            
            if length > self.server.max_size:
                self.send_error(413, f"Length exceeds maximum size of {self.server.max_size}")
                HTTP_RESPONSES.labels('413').inc()
                return
            
            # Record metrics
            if self.server.key_length_histogram:
                self.server.key_length_histogram.observe(length)
            
            random_bytes = os.urandom(length)
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(random_bytes)))
            self.end_headers()
            self.wfile.write(random_bytes)
            HTTP_RESPONSES.labels('200').inc()
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
            HTTP_RESPONSES.labels('500').inc()
        finally:
            REQUEST_LATENCY.labels(self.path).observe(time.time() - start_time)

def run_server(port, max_size, metrics_port=8000, ready_event=None):
    global KEY_LENGTH_HISTOGRAM
    
    # Create linear buckets from 0 to max_size
    bucket_step = max_size / 20
    buckets = [bucket_step * i for i in range(1, 21)]
    
    # Initialize histogram with dynamic buckets
    KEY_LENGTH_HISTOGRAM = Histogram(
        'key_length_bytes',
        'Histogram of requested key lengths',
        buckets=buckets
    )
    
    # Start metrics server
    start_http_server(metrics_port)
    
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, KeyRequestHandler)
    httpd.max_size = max_size
    httpd.key_length_histogram = KEY_LENGTH_HISTOGRAM
    if ready_event:
        ready_event.set()
    print(f"Server started on port {port} with max size {max_size}")
    print(f"Metrics available on port {metrics_port}/metrics")
    print(f"Server listening on http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', type=int, default=1024, help='maximum key size (default 1024)')
    parser.add_argument('--srv-port', type=int, default=1123, help='server listening port (default 1123)')
    parser.add_argument('--metrics-port', type=int, default=8000, help='Prometheus metrics port (default 8000)')
    args = parser.parse_args()
    
    run_server(args.srv_port, args.max_size, args.metrics_port)