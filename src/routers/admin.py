from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import schemas
from crud import Crud

logger = config.get_logger()

router = APIRouter()


@router.get("/admin/users", response_model=list[schemas.User])
async def get_users(req: Request) -> list[schemas.User] | JSONResponse:
    offset = req.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        return await Crud().find_users(offset)
    except SQLAlchemyError as error:
        logger.error(f"get_users {error}")

        return JSONResponse(status_code=500, content="Cannot get users")
