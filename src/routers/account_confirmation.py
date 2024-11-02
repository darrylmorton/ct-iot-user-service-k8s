from http import HTTPStatus
from fastapi import APIRouter
from starlette.responses import JSONResponse

from database.user_crud import UserCrud
from logger import log


router = APIRouter()


@router.get("/verify-account/{id}", status_code=HTTPStatus.CREATED)
async def verify_account(id: str) -> JSONResponse:
    try:
        user_exists = await UserCrud().find_user_by_id(id)

        if user_exists:
            log.debug("Verify Account - user exists")

            await UserCrud().update_confirmed(_id=user_exists.id, _confirmed=True)

            return JSONResponse(status_code=HTTPStatus.OK, content="Account confirmed")

        return JSONResponse(status_code=HTTPStatus.OK, content="Account confirmed")
    except Exception as error:
        log.error(f"Account confirmation error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content="Signup error"
        )
