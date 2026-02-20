#!/usr/bin/env python3
# app.py
from prometheus_client import Counter, Histogram, generate_latest
import falcon
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

class PrometheusMiddleware:
    def process_request(self, req, resp):
        req.start_time = time.time()
        req.method = req.method
        req.path = req.path

    def process_response(self, req, resp, resource, req_succeeded):
        latency = time.time() - req.start_time
        status = resp.status.split()[0]

        REQUEST_COUNT.labels(
            method=req.method,
            endpoint=req.path,
            status=status
        ).inc()

        REQUEST_LATENCY.labels(
            method=req.method,
            endpoint=req.path
        ).observe(latency)

class MetricsResource:
    def on_get(self, req, resp):
        # Use resp.text for string response
        resp.text = generate_latest().decode('utf-8')
        resp.content_type = 'text/plain; version=0.0.4'

class HelloResource:
    def on_get(self, req, resp):
        resp.media = {'message': 'Hello, World!'}

# Create app with middleware
app = falcon.API(middleware=[PrometheusMiddleware()])

app.add_route('/metrics', MetricsResource())
app.add_route('/hello', HelloResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
