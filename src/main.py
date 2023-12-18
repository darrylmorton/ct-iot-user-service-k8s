import json
import logging
from typing import Annotated

import jose
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, JOSEError, JWSError, ExpiredSignatureError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from .schemas import TokenData
from .config import SERVICE_NAME, JWT_EXCLUDED_ENDPOINTS, JWT_SECRET
from .routers import healthz, auth, users

logger = logging.getLogger(SERVICE_NAME)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False
server = FastAPI(title="FastAPI server")


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         # token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     # user = get_user(fake_users_db, username=token_data.username)
#     # if user is None:
#     #     raise credentials_exception
#     # return user
#     return None


@server.middleware("http")
async def authenticate(request: Request, call_next):
    request_path = request["path"]
    print(f"middleware - request_path {request_path}")

    if request_path not in JWT_EXCLUDED_ENDPOINTS:
        try:
            logger.debug(f"login - unauthorized request: {request}")
            print(f"middleware - unauthorized request {request_path}")

            auth_token = request.headers["Authorization"]
            print(f"middleware - auth_token: {auth_token}")

            # token = json.dumps({"token": auth_token})

            payload = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
            print(f"middleware - payload: {payload}")

            username = payload.get("username")
            print(f"middleware - username: {username}")
        except KeyError as error:
            logger.debug(f"login - invalid key error {error}")

            return JSONResponse(status_code=401, content="Invalid key error")
        except ExpiredSignatureError as error:
            logger.debug(f"login - expired signature error {error}")

            return JSONResponse(status_code=401, content="Expired jwt")
        except JWTError as error:
            logger.debug(f"login - invalid jwt error {error}")

            return JSONResponse(status_code=401, content="Invalid jwt")
    # except InvalidTokenError as error:
    #     logger.debug(f"login - invalid token error {error}")
    #
    #     raise HTTPException(status_code=401, detail="Invalid token") from error

    return await call_next(request)


server.include_router(healthz.router, include_in_schema=False)

server.include_router(auth.router, prefix="/api", tags=["auth"])
server.include_router(users.router, prefix="/api", tags=["users"])
