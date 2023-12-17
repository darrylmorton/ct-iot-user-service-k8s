import logging

from fastapi import APIRouter
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..config import SERVICE_NAME
from ..schemas import User, UserRequest
from ..crud import find_users, add_user, find_by_username

LOGGER = logging.getLogger(SERVICE_NAME)

router = APIRouter()


@router.get("/users", response_model=list[User])
async def get_users(req: Request) -> list[User] | JSONResponse:
    offset = req.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        return await find_users(offset)
    except DatabaseError as e:
        LOGGER.error(f"get_users database error {e}")

        return JSONResponse(status_code=500, content="Database error")


@router.get("/users/{username}", response_model=User)
async def get_user_by_username(username: str) -> User | JSONResponse:
    try:
        return await find_by_username(username)
    except DatabaseError as error:
        LOGGER.error(f"get_user_by_username database error {error}")

        return JSONResponse(status_code=500, content="Database error")


@router.post("/users", response_model=User, status_code=201)
async def post_user(req: Request) -> User | JSONResponse:
    request_payload = await req.json()

    try:
        username = UserRequest.model_validate_json(request_payload).username
        password = UserRequest.model_validate_json(request_payload).password

        username_exists = await find_by_username(username)

        if username_exists:
            LOGGER.debug("post_user username exists")

            return JSONResponse(status_code=409, content="Username exists")

        return await add_user(username, password)
    except ValidationError:
        LOGGER.debug("post_user validation error")

        return JSONResponse(status_code=400, content="Invalid username or password")
    except DatabaseError as error:
        LOGGER.error(f"post_user database error {error}")

        return JSONResponse(status_code=500, content="Database error")
