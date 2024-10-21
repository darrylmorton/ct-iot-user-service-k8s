from fastapi import APIRouter, Header
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import config
import schemas
from database.user_details_crud import UserDetailsCrud

logger = config.get_logger()

router = APIRouter()


@router.get("/user-details/{user_id}", response_model=schemas.UserDetails)
async def get_user_details_by_user_id(
    user_id: int,
) -> schemas.UserDetails | JSONResponse:
    try:
        return await UserDetailsCrud().find_user_details_by_user_id(user_id)
    except SQLAlchemyError as error:
        logger.error(f"get_user_details_by_user_id {error}")

        return JSONResponse(
            status_code=500, content="Cannot get user details by user id"
        )
