import contextlib

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import JWT_EXCLUDED_ENDPOINTS, JWT_SECRET, get_logger, SERVICE_NAME
from .routers import healthz, auth, users, user_details

logger = get_logger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


async def run_migrations():
    logger.info("Running migrations...")

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        logger.info("Migrations completed successfully")
    except Exception as error:
        logger.error(f"Database migration error on startup: {error}")


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    logger.info(f"Starting {SERVICE_NAME}...{app.host}")

    await run_migrations()

    logger.info(f"{SERVICE_NAME} is ready")

    yield
    logger.info(f"{SERVICE_NAME} is shutting down...")

    logger.info(f"{SERVICE_NAME} has shut down")


server = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


# @server.on_event("startup")
# async def startup():
#     logger.info(f"Starting {SERVICE_NAME}...")
#
#     await run_migrations()
#
#     logger.info(f"{SERVICE_NAME} is ready")


@server.middleware("http")
async def authenticate(request: Request, call_next):
    request_path = request["path"]

    if request_path not in JWT_EXCLUDED_ENDPOINTS:
        try:
            auth_token = request.headers["Authorization"]
            payload = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])

            username = payload.get("username")
            request.state.username = username
        except KeyError as error:
            logger.debug(f"login - invalid key error {error}")

            return JSONResponse(status_code=401, content="Invalid key error")
        except ExpiredSignatureError as error:
            logger.debug(f"login - expired signature error {error}")

            return JSONResponse(status_code=401, content="Expired token error")
        except JWTError as error:
            logger.debug(f"login - invalid token error {error}")

            return JSONResponse(status_code=401, content="Invalid token error")

    return await call_next(request)


server.include_router(healthz.router, include_in_schema=False)

server.include_router(auth.router, prefix="/api", tags=["auth"])
server.include_router(users.router, prefix="/api", tags=["users"])
server.include_router(user_details.router, prefix="/api", tags=["user-details"])
