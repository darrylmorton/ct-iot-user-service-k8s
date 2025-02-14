import uuid
from http import HTTPStatus

from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

import schemas
from database.user_crud import UserCrud
from decorators.metrics import observability
from logger import log


router = APIRouter()

ROUTE_PATH = "/users/{id}"


@router.get(ROUTE_PATH)
@observability(path=ROUTE_PATH, method="GET")
async def get_user_by_id(request: Request, id: uuid.UUID) -> JSONResponse:
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

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content="Cannot get user by id",
        )
