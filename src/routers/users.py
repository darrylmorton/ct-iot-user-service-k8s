import uuid
from http import HTTPStatus

from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter
from starlette.responses import JSONResponse

import schemas
from database.user_crud import UserCrud
from decorators.metrics import observability, REQUEST_COUNT
from logger import log

router = APIRouter()

ROUTE_PATH = "/users/{id}"
ROUTE_METHOD = "GET"


@router.get(ROUTE_PATH)
@observability(path=ROUTE_PATH, method=ROUTE_METHOD)
async def get_user_by_id(id: uuid.UUID) -> JSONResponse:
    log.debug(f"get_user_by_id called with {id=}")

    try:
        result = await UserCrud().find_user_by_id(_id=str(id))

        result_json = schemas.User.model_validate(result)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=jsonable_encoder(result_json),
        )
    except Exception as error:
        log.error(f"get_user_by_id {error}")

        REQUEST_COUNT.labels(
            method=ROUTE_METHOD,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            path=ROUTE_PATH,
        ).inc()

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Cannot get user by id"},
        )
