from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import crud
import schemas

logger = config.get_logger()

router = APIRouter()


@router.get("/user-details", response_model=list[schemas.UserDetails])
async def get_users(req: Request) -> list[schemas.UserDetails] | JSONResponse:
    offset = req.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        return await crud.find_user_details(offset)
    except SQLAlchemyError as error:
        logger.error(f"get_user_details {error}")

        return JSONResponse(status_code=500, content="Cannot get user details")


@router.get("/user-details/{user_id}", response_model=schemas.UserDetails)
async def get_user_details_by_user_id(
    user_id: int,
) -> schemas.UserDetails | JSONResponse:
    try:
        return await crud.find_user_details_by_user_id(user_id)
    except SQLAlchemyError as error:
        logger.error(f"get_user_details_by_user_id {error}")

        return JSONResponse(
            status_code=500, content="Cannot get user details by user id"
        )
