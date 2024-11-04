from http import HTTPStatus
from fastapi import APIRouter
from starlette.responses import JSONResponse

from database.user_crud import UserCrud
from logger import log
from unit.utils.token_util import TokenUtil

router = APIRouter()


@router.get("/verify-account/{token}", status_code=HTTPStatus.OK)
async def verify_account(token: str) -> JSONResponse:
    try:
        payload = TokenUtil.decode_token(token)
        username = payload["username"]

        user_exists = await UserCrud().find_user_by_username_and_confirmed(username)

        if user_exists:
            log.debug("Verify Account - user exists")

            await UserCrud().update_confirmed(_username=username, _confirmed=True)

            return JSONResponse(status_code=HTTPStatus.OK, content="Account confirmed")

        return JSONResponse(status_code=HTTPStatus.OK, content="")
    except Exception as error:
        log.error(f"Verify Account error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content="Verify Account error"
        )
