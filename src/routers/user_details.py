import logging

from fastapi import APIRouter
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..config import SERVICE_NAME
from ..schemas import UserDetails
from ..crud import find_user_details, find_user_details_by_user_id

LOGGER = logging.getLogger(SERVICE_NAME)

router = APIRouter()


@router.get("/user-details", response_model=list[UserDetails])
async def get_users(req: Request) -> list[UserDetails] | JSONResponse:
    offset = req.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        return await find_user_details(offset)
    except DatabaseError as error:
        LOGGER.error(f"get_user_details database error {error}")

        return JSONResponse(status_code=500, content="Database error")


@router.get("/user-details/{user_id}", response_model=UserDetails)
async def get_user_details_by_user_id(user_id: int) -> UserDetails | JSONResponse:
    try:
        return await find_user_details_by_user_id(user_id)
    except DatabaseError as error:
        LOGGER.error(f"get_user_details_by_user_id database error {error}")

        return JSONResponse(status_code=500, content="Database error")
