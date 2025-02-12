import time
from functools import wraps
from prometheus_client import Gauge, Counter, Histogram

from logger import log

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


def observability(status_code=200):
    def outer_wrapper(func):
        @wraps(func)
        async def inner_wrapper(*args, **kwargs):
            start_time = time.time()
            request = kwargs.get("request")
            method = request["method"]
            path = request["path"]

            REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()
            REQUEST_COUNT.labels(method=method, status=status_code, path=path).inc()
            REQUEST_LATENCY.labels(
                method=method, status=status_code, path=path
            ).observe(time.time() - start_time)
            REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

            return await func(*args, **kwargs)

        log.debug("inner wrapper completed")

        return inner_wrapper

    log.debug("outer wrapper completed")

    return outer_wrapper
