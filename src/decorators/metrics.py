import time
from functools import wraps

from prometheus_client import Gauge, Counter, Histogram

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
CPU_USAGE = Gauge("process_cpu_usage", "Current CPU usage in percent")
MEMORY_USAGE = Gauge("process_memory_usage_bytes", "Current memory usage in bytes")


def observability(method: str, path: str, status_code=200):
    def outer_wrapper(func):
        @wraps(func)
        async def inner_wrapper(*args, **kwargs):
            start_time = time.time()

            REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()

            # returns JSONResponse with status_code and content
            response = await func(*args, **kwargs)

            REQUEST_COUNT.labels(
                method=method, status=response.status_code, path=path
            ).inc()

            REQUEST_LATENCY.labels(
                method=method, status=response.status_code, path=path
            ).observe(time.time() - start_time)
            REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

            return response

        return inner_wrapper

    return outer_wrapper
