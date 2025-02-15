from http import HTTPStatus
from typing import List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import JSONResponse

import schemas
from database.admin_crud import AdminCrud
from decorators.metrics import observability
from logger import log


router = APIRouter()

ROUTE_PATH = "/admin/users"


@router.get(ROUTE_PATH)
@observability(path=ROUTE_PATH, method="GET")
async def get_users(request: Request) -> JSONResponse:
    offset = request.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        result = await AdminCrud().find_users(offset)

        users_adapter = TypeAdapter(List[schemas.User])
        result_json = users_adapter.validate_python(result)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=jsonable_encoder(result_json),
        )
    except Exception as error:
        log.error(f"get_users {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Cannot get users"},
        )
