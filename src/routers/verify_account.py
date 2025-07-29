from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from starlette.responses import JSONResponse

from database.user_crud import UserCrud
from decorators.metrics import observability, REQUEST_COUNT
from logger import log
from utils.token_util import TokenUtil

router = APIRouter()

ROUTE_PATH = "/verify-account/"
ROUTE_METHOD = "GET"


@router.get(ROUTE_PATH, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method=ROUTE_METHOD)
async def verify_account(token: str = Query(default=None)) -> JSONResponse:
    try:
        if not token:
            log.debug("Token is missing")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token is missing"
            )

        payload = TokenUtil.decode_token(token)
        username = payload["username"]

        user_exists = await UserCrud().find_user_by_username_and_confirmed(username)

        if user_exists:
            log.debug("Verify Account - user exists")

            await UserCrud().update_confirmed(_username=username, _confirmed=True)

            return JSONResponse(
                status_code=HTTPStatus.OK, content={"message": "Account confirmed"}
            )

        return JSONResponse(status_code=HTTPStatus.OK, content="")
    except HTTPException as error:
        log.error(f"Verify Account - http error {error}")

        REQUEST_COUNT.labels(
            method=ROUTE_METHOD, status=error.status_code, path=ROUTE_PATH
        ).inc()

        return JSONResponse(status_code=error.status_code, content=error.detail)
    except Exception as error:
        log.error(f"Verify Account error {error}")

        REQUEST_COUNT.labels(
            method=ROUTE_METHOD,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            path=ROUTE_PATH,
        ).inc()

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Verify Account error"},
        )
