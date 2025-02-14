import uuid
from http import HTTPStatus

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse

from database.user_details_crud import UserDetailsCrud
from decorators.metrics import observability
from logger import log


router = APIRouter()

ROUTE_PATH = "/user-details/{user_id}"


@router.get(ROUTE_PATH)
@observability(path=ROUTE_PATH, method="GET")
async def get_user_details_by_user_id(
    request: Request,
    user_id: uuid.UUID,
) -> JSONResponse:
    try:
        result = await UserDetailsCrud().find_user_details_by_user_id(user_id)

        return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))
    except Exception as error:
        log.error(f"get_user_details_by_user_id {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content="Cannot get user details by user id",
        )
