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
from database.user_crud import UserCrud
from logger import log
from config import SERVICE_NAME, JWT_EXCLUDED_ENDPOINTS
from routers import health, users, user_details, signup, login, admin
from utils.app_util import AppUtil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


async def run_migrations():
    log.info("Running migrations...")

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        log.info("Migrations completed successfully")
    except Exception:
        log.error("Database migration error on startup")
        raise Exception("Database migration error on startup")


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {SERVICE_NAME}...{app.host}")
    log.info(f"Sentry {config.SENTRY_ENVIRONMENT} environment")
    log.info(f"Application {config.ENVIRONMENT} environment")

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

    log.info(f"{SERVICE_NAME} is ready")

    yield
    log.info(f"{SERVICE_NAME} is shutting down...")


app = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


@app.middleware("http")
async def authenticate(request: Request, call_next):
    request_path = request["path"]

    try:
        if request_path not in JWT_EXCLUDED_ENDPOINTS:
            log.debug("authenticate - included request_path")

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

            _id = response_json["id"]
            _admin = response_json["admin"]

            # token user id must be a valid uuid
            if not AppUtil.validate_uuid4(_id):
                log.debug("authenticate - invalid uuid")

                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
                )

            user = await UserCrud().find_user_by_id_and_enabled(_id=_id)

            # user must exist
            if not user:
                log.debug("authenticate - user not found")

                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
                )

            # admin status must match user status
            if _admin != user.is_admin:
                log.debug("authenticate - invalid user")

                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
                )

            # only admins can access admin paths
            if not user.is_admin and request_path.startswith("/api/admin"):
                log.debug("authenticate - only admins can access admin paths")

                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN, content="Forbidden error"
                )

            # only a user can access their own user record by id
            if not user.is_admin and not AppUtil.validate_uuid_path_param(
                request_path, str(user.id)
            ):
                log.debug("authenticate - user cannot access another user record")

                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN, content="Forbidden error"
                )
    except KeyError as err:
        log.debug(f"authenticate - missing token {err}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )

    return await call_next(request)


app.include_router(health.router, include_in_schema=False)

app.include_router(signup.router, prefix="/api", tags=["signup"])
app.include_router(login.router, prefix="/api", tags=["login"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(user_details.router, prefix="/api", tags=["user-details"])
app.include_router(admin.router, prefix="/api", tags=["admin"])

app = AppUtil.set_openapi_info(app=app)
