import logging
from fastapi import APIRouter
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.schemas import User, UserRequest
from src.crud import get_users, post_user, get_user_by_username

router = APIRouter()


@router.get("/users", response_model=list[User])
async def users() -> list[User] | JSONResponse:
    try:
        return await get_users()
    except DatabaseError as e:
        logging.error(f"get users error {e}")

        return JSONResponse(status_code=500, content=None)


@router.get("/users/{username}", response_model=list[User])
async def user(username: str) -> User | JSONResponse:
    try:
        return await get_user_by_username(username)
    except DatabaseError as e:
        logging.error(f"get users error {e}")

        return JSONResponse(status_code=500, content=None)


@router.post("/users", response_model=User, status_code=201)
async def user(req: Request) -> JSONResponse:
    request_payload = await req.json()

    username = UserRequest.model_validate_json(request_payload).username
    password = UserRequest.model_validate_json(request_payload).password

    user_request = UserRequest(
        username=username,
        password=password,
    )

    try:
        return await post_user(user_request)
    except DatabaseError as e:
        logging.error(f"post users error {e}")

        return JSONResponse(status_code=500, content=None)
