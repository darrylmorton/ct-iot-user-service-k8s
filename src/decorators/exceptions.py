import functools
from http import HTTPStatus


from decorators.metrics import REQUEST_COUNT
from exceptions.exceptions import MetricsCatcherException
from logger import log


def metrics_catcher(f):
    log.debug("metrics_catcher")

    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        log.debug(f"metrics_catcher {request['path']=}")
        # log.debug(f"metrics_catcher {args=}")
        # log.debug(f"metrics_catcher {kwargs=}")

        # def inner(*args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        # except KeyError as error:
        #     log.error(f"metrics_catcher - missing token {error}")
        #
        #     REQUEST_COUNT.labels(
        #         method=error.method, status=error.status_code, path=error.path
        #     ).inc()
        #
        #     return JSONResponse(
        #         status_code=HTTPStatus.UNAUTHORIZED,
        #         content={"message": "Unauthorised error"},
        #     )
        except MetricsCatcherException as error:
            log.info(f"** metrics_catcher {error}")

            REQUEST_COUNT.labels(
                method=error.method, status=error.status_code, path=error.path
            ).inc()

            return f(*args, **kwargs)
            # raise error
            # return JSONResponse(status_code=error.status_code, content=error.detail)
            # return HTTPException(
            #     status_code=error.status_code, detail=error.detail)
        except Exception as err:
            log.error(f"*** metrics_catcher - server error {err}")

            REQUEST_COUNT.labels(
                method="", status=HTTPStatus.INTERNAL_SERVER_ERROR, path=""
            ).inc()

            # return f(*args, **kwargs)
            # return JSONResponse(
            #     status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            #     content={"message": "Server error"},
            # )
            # return HTTPException(
            #     status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Server error")
        finally:
            log.info("**** metrics_catcher")

            # return f(*args, **kwargs)
            # CPU_USAGE.set(psutil.cpu_percent())
            # MEMORY_USAGE.set(psutil.Process().memory_info().rss)

        # return inner()

    return wrapper
