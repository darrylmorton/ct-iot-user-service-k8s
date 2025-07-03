from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

from decorators.metrics import observability
from utils.app_util import AppUtil

router = APIRouter()

ROUTE_PATH = "/healthz"


@router.get(ROUTE_PATH)
@observability(path=ROUTE_PATH, method="GET")
async def health() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": AppUtil.get_app_version()},
    )
