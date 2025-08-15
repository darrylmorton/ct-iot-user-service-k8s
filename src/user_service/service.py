import asyncio
import contextlib
from http import HTTPStatus

import psutil
import requests
import sentry_sdk
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from prometheus_client import make_asgi_app

import config
from database.user_crud import UserCrud
from decorators.metrics import CPU_USAGE, MEMORY_USAGE

from logger import log
from routers import health, users, user_details, signup, login, admin, verify_account
from utils.app_util import AppUtil
from utils.auth_util import AuthUtil
from utils.validator_util import ValidatorUtil


async def run_migrations():
    log.info("Running migrations...")

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        log.info("Migrations completed successfully")
    except Exception:
        log.error("Database migration error on startup")
        raise Exception("Database migration error on startup")


async def update_process_metrics(interval: float = 5.0):
    """
    Periodically update Prometheus metrics for CPU and memory usage.
    This asynchronous background task runs indefinitely, updating the
    CPU_USAGE and MEMORY_USAGE Prometheus metrics at a fixed interval.
    Args:
        interval (float): The time in seconds to wait between metric updates.
            Defaults to 5.0 seconds.
    """
    log.info("Starting update_process_metrics() task...")

    process = psutil.Process()

    while True:
        try:
            CPU_USAGE.set(psutil.cpu_percent())
            MEMORY_USAGE.set(process.memory_info().rss)

        except Exception as e:
            log.error(f"Error updating process metrics: {e}")

        await asyncio.sleep(interval)


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {config.SERVICE_NAME}...{app.host}")
    log.info(f"Sentry {config.SENTRY_ENVIRONMENT} environment")
    log.info(f"Application {config.ENVIRONMENT} environment")

    asyncio.create_task(update_process_metrics())

    if config.SENTRY_ENVIRONMENT != "local":
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for tracing.
            traces_sample_rate=config.SENTRY_TRACES_SAMPLE_RATE,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=config.SENTRY_PROFILES_SAMPLE_RATE,
            sample_rate=config.SENTRY_SAMPLE_RATE,
            environment=config.ENVIRONMENT,
            server_name=config.SERVICE_NAME,
            integrations=[
                StarletteIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes=[403, range(500, 599)],
                ),
                FastApiIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes=[403, range(500, 599)],
                ),
            ],
        )

    await run_migrations()

    log.info(f"{config.SERVICE_NAME} is ready")

    yield
    log.info(f"{config.SERVICE_NAME} is shutting down...")


app = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)

http_bearer_security = HTTPBearer()


@app.middleware("http")
async def authenticate(request: Request, call_next):
    log.debug("middleware - authentication")

    request_path = request["path"]

    if not AppUtil.is_excluded_endpoint(request_path):
        try:
            auth_token = request.headers["authorization"]

            if not auth_token:
                log.debug("authenticate - missing auth token")

                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
                )

            auth_token = auth_token.replace("Bearer ", "")

            response = requests.get(
                f"{config.AUTH_SERVICE_URL}/jwt/authentication",
                headers={"auth-token": auth_token},
            )

            if response.status_code != HTTPStatus.OK:
                log.debug("authenticate - invalid token")

                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
                )

            response_json = response.json()

            _id = response_json["id"]
            _admin = response_json["is_admin"]

            # token user id must be a valid uuid
            if not ValidatorUtil.validate_uuid4(_id):
                log.debug("authenticate - invalid uuid")

                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
                )

            user = await UserCrud().find_user_by_id(_id=_id)

            if not user:
                log.debug("authenticate - user not found")

                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
                )

            # user must be valid:
            AuthUtil.is_user_valid(
                _confirmed=user.confirmed,
                _enabled=user.enabled,
            )

            # admin status must be valid
            AuthUtil.is_admin_valid(
                _id=str(user.id),
                _is_admin=user.is_admin,
                _admin=_admin,
                _request_path=request_path,
            )

        except KeyError as err:
            log.error(f"authenticate - missing token {err}")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Unauthorised error"},
            )
        except HTTPException as error:
            log.error(f"authenticate - http error {error}")

            return JSONResponse(status_code=error.status_code, content=error.detail)
        except Exception as err:
            log.error(f"authenticate - server error {err}")

            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": "Server error"},
            )

    return await call_next(request)


# prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics/", metrics_app)

app.include_router(health.router, include_in_schema=False)

app.include_router(signup.router, prefix="/api", tags=["signup"])
app.include_router(login.router, prefix="/api", tags=["login"])
app.include_router(verify_account.router, prefix="/api", tags=["verify-account"])

app.include_router(
    users.router,
    prefix="/api",
    tags=["users"],
    dependencies=[Depends(http_bearer_security)],
)
app.include_router(
    user_details.router,
    prefix="/api",
    tags=["user-details"],
    dependencies=[Depends(http_bearer_security)],
)
app.include_router(
    admin.router,
    prefix="/api",
    tags=["admin"],
    dependencies=[Depends(http_bearer_security)],
)

app = AppUtil.set_openapi_info(app=app)
