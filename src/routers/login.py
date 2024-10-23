import requests

from http import HTTPStatus
from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from logger import log

router = APIRouter()


@router.post("/login", response_model=schemas.User, status_code=HTTPStatus.OK)
async def login(
    payload: schemas.LoginRequest = Body(embed=False),
) -> JSONResponse:
    try:
        authorised_user = await UserCrud().authorise(
            _username=payload.username, _password=payload.password
        )

        if not authorised_user.id:
            log.debug("Login - Invalid login")

            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN, content="Invalid login credentials"
            )
        elif not authorised_user.enabled:
            log.debug("Login - account not enabled")

            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN, content="Account not enabled"
            )
        else:
            response = requests.post(
                f"{config.AUTH_SERVICE_URL}/jwt",
                json={
                    "id": str(authorised_user.id),
                    "admin": authorised_user.is_admin,
                },
            )

            if response.status_code == HTTPStatus.CREATED:
                return JSONResponse(status_code=HTTPStatus.OK, content=response.json())
            else:
                log.debug("Login - invalid username or password")

                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content="Invalid username or password",
                )
    except Exception as error:
        log.error(f"Login error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content="Login error"
        )
