from fastapi import APIRouter
from starlette.responses import JSONResponse

import config

router = APIRouter()


@router.get("/healthz")
async def health() -> JSONResponse:
    return JSONResponse(
        status_code=200, content={"message": "ok", "version": config.APP_VERSION}
    )
