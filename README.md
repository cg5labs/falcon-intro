# Falcon Prometheus Metrics

A Falcon web application with Prometheus metrics collection middleware.

## Installation

```bash
pip install falcon prometheus-client
```

## Usage

```bash
python app.py
```

The server will start on `http://0.0.0.0:8000`.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/metrics` | Prometheus metrics endpoint |
| `/hello` | Example hello world endpoint |

## Metrics

The following metrics are collected:

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, endpoint, status | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | method, endpoint | HTTP request latency |

## Example

```bash
# Start the server
python app.py

# In another terminal, test the endpoints
curl http://localhost:8000/hello
# {"message": "Hello, World!"}

curl http://localhost:8000/metrics
# # HELP http_requests_total Total HTTP requests
# # TYPE http_requests_total counter
# http_requests_total{endpoint="/hello",method="GET",status="200"} 1.0
# ...
```

## Prometheus Configuration

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'falcon-app'
    static_configs:
      - targets: ['localhost:8000']
```
