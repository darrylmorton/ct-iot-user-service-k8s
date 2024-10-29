import uuid
from http import HTTPStatus

from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

import schemas
from database.user_crud import UserCrud
from logger import log

router = APIRouter()


@router.get("/users/{id}", response_model=schemas.User)
async def get_user_by_id(id: uuid.UUID) -> schemas.User | JSONResponse:
    try:
        return await UserCrud().find_user_by_id(_id=str(id))
    except Exception as error:
        log.error(f"get_user_by_id {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content="Cannot get user by id",
        )
