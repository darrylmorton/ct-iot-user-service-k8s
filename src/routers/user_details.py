import uuid
from http import HTTPStatus

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

import schemas
from database.user_details_crud import UserDetailsCrud
from decorators.metrics import observability_metrics
from logger import log


router = APIRouter()


@router.get("/user-details/{user_id}", response_model=schemas.UserDetails)
@observability_metrics
async def get_user_details_by_user_id(
    request: Request, user_id: uuid.UUID,
) -> schemas.UserDetails | JSONResponse:
    try:
        return await UserDetailsCrud().find_user_details_by_user_id(user_id)
    except Exception as error:
        log.error(f"get_user_details_by_user_id {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content="Cannot get user details by user id",
        )
