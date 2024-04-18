from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body
from jose import jwt

from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from utils.auth_util import create_token_expiry
from config import JWT_SECRET, get_logger
from schemas import (
    User,
    SignupResponse,
    SignupRequest,
    LoginRequest,
)
from crud import add_user, find_user_by_username, authorise, add_user_details

logger = get_logger()

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=201)
async def signup(
    signup_request: Annotated[SignupRequest, Body(embed=False)],
) -> JSONResponse | SignupResponse:
    validation_status_code = HTTPStatus.UNAUTHORIZED
    validation_message = "Invalid username or password"

    try:
        username_exists = await find_user_by_username(signup_request.username)

        if username_exists:
            return JSONResponse(status_code=409, content="Username exists")

        user = await add_user(
            _username=signup_request.username, _password=signup_request.password
        )

        validation_status_code = HTTPStatus.BAD_REQUEST
        validation_message = "Invalid first or last name"

        user_details = await add_user_details(
            _user_id=user.id,
            _first_name=signup_request.first_name,
            _last_name=signup_request.last_name,
        )

        return SignupResponse(
            username=user.username,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
        )
    except ValidationError as error:
        logger.debug("signup validation error")

        raise HTTPException(
            status_code=validation_status_code, detail=validation_message
        ) from error
    except DatabaseError as error:
        logger.error(f"signup database error {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database error"
        ) from error


@router.post("/login", response_model=User, status_code=200)
async def login(req: Request) -> JSONResponse:
    request_payload = await req.json()

    try:
        LoginRequest.model_validate(request_payload)

        username = request_payload["username"]
        password = request_payload["password"]

        authorised_user = await authorise(_username=username, _password=password)

        if not authorised_user.enabled:
            return JSONResponse(status_code=403, content="Account not enabled")
        elif authorised_user.enabled:
            expiry = create_token_expiry()

            token = {
                "token": jwt.encode(
                    {"username": username, "exp": expiry},
                    JWT_SECRET,
                    algorithm="HS256",
                )
            }

            return JSONResponse(status_code=200, content=token)
    except ValueError as error:
        logger.debug("login validation error")

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid username or password"
        ) from error
    except DatabaseError as error:
        logger.error(f"login database error {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database error"
        ) from error
