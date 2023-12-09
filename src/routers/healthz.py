from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/healthz")
async def healthz() -> JSONResponse:
    return JSONResponse(status_code=200, content={"message": "ok"})
