import logging
import structlog


class ServiceLogger:
    def __init__(self):
        structlog.configure(
            processors=[
                # structlog.contextvars.merge_contextvars,
                # structlog.processors.add_log_level,
                # structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=True),
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False,
        )

        self.log = structlog.get_logger()

    def warning(self, message: str):
        self.log.warning(message)

    def debug(self, message: str):
        self.log.debug(message)

    def info(self, message: str):
        self.log.info(message)

    def error(self, message: str):
        self.log.error(message)

    def critical(self, message: str):
        self.log.critical(message)


log = ServiceLogger()
