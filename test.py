
import unittest
import requests
import threading
from key_server import run_server
import time

class TestKeyServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 1123
        cls.max_size = 1024
        cls.metrics_port = 8000
        
        # Create a readiness event
        cls.server_ready = threading.Event()
        
        # Start server in a thread
        cls.server_thread = threading.Thread(
            target=run_server,
            args=(cls.port, cls.max_size, cls.metrics_port, cls.server_ready),
            daemon=True
        )
        cls.server_thread.start()
        
        # Wait for server to be ready (max 20 seconds)
        if not cls.server_ready.wait(timeout=10):
            raise TimeoutError("Server failed to start within 20 seconds")

    def test_positive_request(self):
        """Test valid key request"""
        response = requests.get(f'http://localhost:{self.port}/key/10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 10)

    def test_negative_request(self):
        """Test oversized key request"""
        response = requests.get(f'http://localhost:{self.port}/key/2000')
        self.assertEqual(response.status_code, 413)
        self.assertIn("exceeds maximum size", response.text)

    def test_health_check(self):
        """Test health endpoint"""
        response = requests.get(f'http://localhost:{self.port}/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'OK')

    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        # Generate some traffic
        requests.get(f'http://localhost:{self.port}/key/10')
        requests.get(f'http://localhost:{self.port}/key/2000')
        
        response = requests.get(f'http://localhost:{self.metrics_port}/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertIn('http_responses_total', response.text)
        self.assertIn('key_length_bytes', response.text)

if __name__ == '__main__':
    unittest.main()