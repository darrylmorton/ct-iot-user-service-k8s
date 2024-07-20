from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import config
import crud
import schemas

logger = config.get_logger()

router = APIRouter()


@router.get("/users/{username}", response_model=schemas.User)
async def get_user_by_username(username: str) -> schemas.User | JSONResponse:
    try:
        return await crud.find_user_by_username(username=username)
    except SQLAlchemyError as error:
        logger.error(f"get_user_by_username {error}")

        return JSONResponse(status_code=500, content="Cannot get users by username")
