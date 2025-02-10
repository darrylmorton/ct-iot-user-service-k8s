from http import HTTPStatus

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from decorators.metrics import observability_metrics
from utils.app_util import AppUtil

router = APIRouter()


@router.get("/healthz")
@observability_metrics
async def health(request: Request) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": AppUtil.get_app_version()},
    )
