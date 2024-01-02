from fastapi import APIRouter
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..config import get_logger
from ..schemas import User
from ..crud import find_users, find_user_by_username

logger = get_logger()

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
        logger.error(f"get_users database error {e}")

        return JSONResponse(status_code=500, content="Database error")


@router.get("/users/{username}", response_model=User)
async def get_user_by_username(username: str) -> User | JSONResponse:
    try:
        return await find_user_by_username(username)
    except DatabaseError as error:
        logger.error(f"get_user_by_username database error {error}")

        return JSONResponse(status_code=500, content="Database error")
