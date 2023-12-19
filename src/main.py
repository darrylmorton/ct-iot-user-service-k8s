import logging
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import SERVICE_NAME, JWT_EXCLUDED_ENDPOINTS, JWT_SECRET
from .routers import healthz, auth, users, user_details

logger = logging.getLogger(SERVICE_NAME)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False
server = FastAPI(title="FastAPI server")


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

            return JSONResponse(status_code=401, content="Expired jwt")
        except JWTError as error:
            logger.debug(f"login - invalid jwt error {error}")

            return JSONResponse(status_code=401, content="Invalid jwt")

    return await call_next(request)


server.include_router(healthz.router, include_in_schema=False)

server.include_router(auth.router, prefix="/api", tags=["auth"])
server.include_router(users.router, prefix="/api", tags=["users"])
server.include_router(user_details.router, prefix="/api", tags=["user-details"])
