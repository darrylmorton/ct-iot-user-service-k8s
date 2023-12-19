import json
import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body
from jose import jwt

from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..utils.date_util import create_token_expiry
from ..config import JWT_SECRET, SERVICE_NAME
from ..schemas import (
    User,
    UserRequest,
    SignupResponse,
    SignupRequest,
)
from ..crud import add_user, find_user_by_username, authorise, add_user_details

logger = logging.getLogger(SERVICE_NAME)

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=201)
async def signup(
    signup_request: Annotated[SignupRequest, Body(embed=False)],
) -> JSONResponse | SignupResponse:
    print(f"signup route called...")

    # request_payload = req
    print(f"signup_request: {signup_request}")
    validation_message = "Invalid username or password"

    try:
        # username = UserRequest.model_validate_json(request_payload).username
        # print(f"0 request_payload: {request_payload}")
        #
        # password = UserRequest.model_validate_json(request_payload).password
        # print(f"1 request_payload: {request_payload}")
        #
        username_exists = await find_user_by_username(signup_request.username)
        print(f"username_exists: {username_exists}")

        if username_exists:
            return JSONResponse(status_code=409, content="Username exists")

        # print(f"2 request_payload first_name: {request_payload['first_name']}")

        # first_name = UserDetailsRequest.model_validate_json(request_payload).first_name
        # print(f"2 request_payload: {request_payload}")
        #
        # last_name = UserDetailsRequest.model_validate_json(request_payload).last_name
        # print(f"3 request_payload: {request_payload}")

        user = await add_user(
            _username=signup_request.username, _password=signup_request.password
        )
        print(f"user: {user}")

        validation_message = "Invalid first or last name"

        user_details = await add_user_details(
            _user_id=user.id,
            _first_name=signup_request.first_name,
            _last_name=signup_request.last_name,
        )
        print(f"user_details: {user_details}")

        # user.user_details = user_details

        return SignupResponse(
            username=user.username,
            first_name=user_details.first_name,
            last_name=user_details.last_name
        )
    except ValidationError as error:
        logger.debug("signup validation error")

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=validation_message
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
        username = UserRequest.model_validate_json(request_payload).username
        password = UserRequest.model_validate_json(request_payload).password

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

        return JSONResponse(status_code=401, content="Invalid username or password")
    except ValidationError as error:
        logger.debug("login validation error")

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid username or password"
        ) from error
    except DatabaseError as error:
        logger.error(f"login database error {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database error"
        ) from error
