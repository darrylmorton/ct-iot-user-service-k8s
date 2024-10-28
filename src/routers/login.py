import requests

from http import HTTPStatus
from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from logger import log
from utils.app_util import AppUtil
from utils.auth_util import AuthUtil

router = APIRouter()


@router.post("/login", response_model=schemas.User, status_code=HTTPStatus.OK)
async def login(
    payload: schemas.LoginRequest = Body(embed=False),
) -> JSONResponse:
    try:
        authorised_user = await UserCrud().authorise(
            _username=payload.username, _password=payload.password
        )

        valid_user = AppUtil.is_user_valid(
            _user=authorised_user, _status_code=HTTPStatus.FORBIDDEN
        )
        log.debug(f"{valid_user=}")

        if valid_user:
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
