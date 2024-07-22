import contextlib
from http import HTTPStatus

import requests

import sentry_sdk
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import crud
from logger import log
from config import SERVICE_NAME, JWT_EXCLUDED_ENDPOINTS
from routers import health, users, user_details, signup, login

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


async def run_migrations():
    log.info("Running migrations...")

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        log.info("Migrations completed successfully")
    except Exception as error:
        log.error(f"Database migration error on startup: {error}")


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {SERVICE_NAME}...{app.host}")

    if config.ENVIRONMENT == "production":
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

    log.info(f"{SERVICE_NAME} is ready")

    yield
    log.info(f"{SERVICE_NAME} is shutting down...")


server = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


# TODO check user path param matches user in token
#  (unless roles are implemented and another user has permission to access other users)
#  Could be achieved within users/{username} route by
#  comparing path param and session user?
#  Or obtain path param from within middleware would be cleaner and more secure
@server.middleware("http")
async def authenticate(request: Request, call_next):
    request_path = request["path"]

    if request_path not in JWT_EXCLUDED_ENDPOINTS:
        auth_token = request.headers["Authorization"]

        if not auth_token:
            log.debug("authenticate - missing auth token")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

        response = requests.get(
            f"{config.AUTH_SERVICE_URL}/jwt", headers={"Authorization": auth_token}
        )

        if response.status_code != HTTPStatus.OK:
            log.debug("authenticate - invalid token")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

        response_json = response.json()

        username = response_json["username"]

        user = await crud.find_user_by_username_and_enabled(username=username)

        if not user or user.username != username:
            log.debug("authenticate - username not found")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

    return await call_next(request)


server.include_router(health.router, include_in_schema=False)

server.include_router(signup.router, prefix="/api", tags=["signup"])
server.include_router(login.router, prefix="/api", tags=["login"])
server.include_router(users.router, prefix="/api", tags=["users"])
server.include_router(user_details.router, prefix="/api", tags=["user-details"])
# roles need to be implemented to restrict access
# server.include_router(users.router, prefix="/api", tags=["admin"])
