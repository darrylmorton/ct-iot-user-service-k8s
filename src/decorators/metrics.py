import json
import time
from functools import wraps

# import psutil
from prometheus_client import Gauge, Counter, Histogram

from logger import log

# CPU_USAGE = Gauge("process_cpu_usage", "Current CPU usage in percent")
# MEMORY_USAGE = Gauge("process_memory_usage_bytes", "Current memory usage in bytes")
REQUEST_COUNT = Counter(
    "http_request_total", "Total HTTP Requests", ["method", "status", "path"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "status", "path"],
)
REQUEST_IN_PROGRESS = Gauge(
    "http_requests_in_progress", "HTTP Requests in progress", ["method", "path"]
)

def observability_metrics(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # log.debug(f"observability_metrics - wrapper {args=}, {kwargs=}")

        start_time = time.time()
        request = kwargs.get("request")
        method = request["method"]
        path = request["path"]

        REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()

        response = await func(*args, **kwargs)
        status_code = response.status_code

        REQUEST_COUNT.labels(method=method, status=status_code, path=path).inc()
        REQUEST_LATENCY.labels(method=method, status=status_code, path=path).observe(
            time.time() - start_time
        )
        REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

        return response

    return wrapper
