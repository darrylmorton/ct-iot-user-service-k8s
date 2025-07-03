from starlette.exceptions import HTTPException


class MetricsCatcherException(HTTPException):
    def __init__(self, status_code, detail, path, method):
        super().__init__(status_code, detail)

        self.path = path
        self.method = method
        self.status_code = status_code
        self.detail = detail

        # log.debug(f"metrics_catcher")
