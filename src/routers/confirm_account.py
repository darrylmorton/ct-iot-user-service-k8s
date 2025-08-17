from http import HTTPStatus

import requests
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
from database.user_crud import UserCrud
from decorators.metrics import observability
from logger import log


router = APIRouter()

ROUTE_PATH = "/confirm-account/"


@router.get(ROUTE_PATH, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method="GET")
async def confirm_account(
    request: Request, token: str = Query(default=None)
) -> JSONResponse:
    try:
        if not token:
            log.debug("Token is missing")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token is missing"
            )

        response = requests.get(
            f"{config.AUTH_SERVICE_URL}/jwt/confirm-account",
            headers={"confirm-account-token": token},
        )

        if response.status_code != HTTPStatus.OK:
            log.error(
                f"Failed to confirm account - auth service returned HTTP error {response.status_code}: {response.text}")

            raise HTTPException(status_code=response.status_code, detail=response.text)

        else:
            response_json = response.json()

            username = response_json["username"]

            user_exists = await UserCrud().find_user_by_username_and_confirmed(username)

            if user_exists:
                log.debug("Confirm Account - user exists")

                await UserCrud().update_confirmed(_username=username, _confirmed=True)

                return JSONResponse(
                    status_code=HTTPStatus.OK, content={"message": "Account confirmed"}
                )

            return JSONResponse(status_code=HTTPStatus.OK, content="")
    except HTTPException as error:
        log.error(f"Confirm Account - http error {error}")

        return JSONResponse(status_code=error.status_code, content=error.detail)
    except Exception as error:
        log.error(f"Confirm Account error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Confirm Account error"},
        )
