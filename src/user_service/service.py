import contextlib

import sentry_sdk
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from logger import log
from config import SERVICE_NAME
from routers import health, users, user_details, signup

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

    sentry_sdk.init(
        dsn="https://08d7c1a4c2f9ae2533fadbda6a688817@o4506877226909696.ingest.us.sentry.io/4506877230186496",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

    await run_migrations()

    log.info(f"{SERVICE_NAME} is ready")

    yield
    log.info(f"{SERVICE_NAME} is shutting down...")


server = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


@server.middleware("http")
async def authenticate(request: Request, call_next):
    # request_path = request["path"]
    #
    # if request_path not in JWT_EXCLUDED_ENDPOINTS:
    #     try:
    #         auth_token = request.headers["Authorization"]
    #         payload = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
    #
    #         username = payload.get("username")
    #         request.state.username = username
    #     except KeyError as error:
    #         log.debug(f"login - invalid key error {error}")
    #
    #         return JSONResponse(status_code=401, content="Invalid key error")
    #     except ExpiredSignatureError as error:
    #         log.debug(f"login - expired signature error {error}")
    #
    #         return JSONResponse(status_code=401, content="Expired token error")
    #     except JWTError as error:
    #         log.debug(f"login - invalid token error {error}")
    #
    #         return JSONResponse(status_code=401, content="Invalid token error")

    return await call_next(request)


server.include_router(health.router, include_in_schema=False)

server.include_router(signup.router, prefix="/api", tags=["signup"])
server.include_router(users.router, prefix="/api", tags=["users"])
server.include_router(user_details.router, prefix="/api", tags=["user-details"])
