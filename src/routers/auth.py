import json
import logging
from http import HTTPStatus

import jwt
from fastapi import APIRouter, HTTPException
from jwt import ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..utils.date_util import create_token_expiry
from ..config import SERVICE_NAME, JWT_SECRET
from ..schemas import User, UserRequest
from ..crud import add_user, find_by_username, authorise

router = APIRouter()

LOGGER = logging.getLogger(SERVICE_NAME)


# TODO UserDetails also required as part of successful signup
@router.post("/signup", response_model=User, status_code=201)
async def signup(req: Request) -> User | JSONResponse:
    request_payload = await req.json()

    try:
        username = UserRequest.model_validate_json(request_payload).username
        password = UserRequest.model_validate_json(request_payload).password

        username_exists = await find_by_username(username)

        if username_exists:
            return JSONResponse(status_code=409, content="Username exists")

        return await add_user(username, password)
    except ValidationError as error:
        LOGGER.debug("signup validation error")

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid username or password"
        ) from error
    except DatabaseError as error:
        LOGGER.error(f"signup database error {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database error"
        ) from error


@router.post("/login", response_model=User, status_code=200)
async def login(req: Request) -> JSONResponse:
    request_payload = await req.json()
    LOGGER.info(f"*** route login request_payload: {request_payload}")

    try:
        username = UserRequest.model_validate_json(request_payload).username
        password = UserRequest.model_validate_json(request_payload).password
        authorised_user = await authorise(username, password)
        LOGGER.info(f"*** route login authorised_user: {authorised_user}")

        if authorised_user:
            expiry = create_token_expiry()
            LOGGER.info(f"route login expiry: {expiry}")

            token = {
                "token": jwt.encode(
                    {"username": username, "exp": expiry},
                    JWT_SECRET,
                    algorithm="HS256",
                )
            }
            LOGGER.info(f"route login token: {token}")

            return JSONResponse(status_code=200, content=token)

        return JSONResponse(status_code=401, content="Invalid username or password")
    except ValidationError as error:
        LOGGER.debug("login validation error")

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid username or password"
        ) from error
    except ExpiredSignatureError as error:
        LOGGER.debug(f"login expired signature error {error}")

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
        ) from error
    except DatabaseError as error:
        LOGGER.error(f"login database error {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database error"
        ) from error
