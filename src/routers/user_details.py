import uuid
from http import HTTPStatus

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from database.user_details_crud import UserDetailsCrud
from decorators.metrics import observability, REQUEST_COUNT
from logger import log

router = APIRouter()

ROUTE_PATH = "/user-details/{user_id}"
ROUTE_METHOD = "GET"


@router.get(ROUTE_PATH)
@observability(path=ROUTE_PATH, method=ROUTE_METHOD)
async def get_user_details_by_user_id(
    user_id: uuid.UUID,
) -> JSONResponse:
    try:
        result = await UserDetailsCrud().find_user_details_by_user_id(user_id)

        return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))
    except Exception as error:
        log.error(f"get_user_details_by_user_id {error}")

        REQUEST_COUNT.labels(
            method=ROUTE_METHOD,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            path=ROUTE_PATH,
        ).inc()

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Cannot get user details by user id"},
        )
