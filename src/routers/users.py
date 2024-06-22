from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import crud
import schemas

logger = config.get_logger()

router = APIRouter()


@router.get("/users", response_model=list[schemas.User])
async def get_users(req: Request) -> list[schemas.User] | JSONResponse:
    offset = req.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        return await crud.find_users(offset)
    except SQLAlchemyError as error:
        logger.error(f"get_users {error}")

        return JSONResponse(status_code=500, content="Cannot get users")


@router.get("/users/{username}", response_model=schemas.User)
async def get_user_by_username(username: str) -> schemas.User | JSONResponse:
    try:
        return await crud.find_user_by_username(username)
    except SQLAlchemyError as error:
        logger.error(f"get_user_by_username {error}")

        return JSONResponse(status_code=500, content="Cannot get users by username")
