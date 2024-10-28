import requests

from http import HTTPStatus
from fastapi import APIRouter, Body
from starlette.exceptions import HTTPException
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
        _user = await UserCrud().authorise(
            _username=payload.username, _password=payload.password
        )

        if not _user:
            log.debug("Login - invalid login")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid login"
            )
        if not _user.confirmed:
            log.debug("Login - user account unconfirmed")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="User account unconfirmed"
            )
        if not _user.enabled:
            log.debug("Login - user account suspended")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="User account suspended"
            )

        response = requests.post(
            f"{config.AUTH_SERVICE_URL}/jwt",
            json={
                "id": str(_user.id),
                "admin": _user.is_admin,
            },
        )

        if response.status_code == HTTPStatus.CREATED:
            return JSONResponse(status_code=HTTPStatus.OK, content=response.json())
        else:
            log.debug(
                f"Login - jwt generation failed: {response.status_code}, {response.text}"
            )

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Login error",
            )
    except HTTPException as error:
        log.error(f"Login error {error}")

        return JSONResponse(status_code=error.status_code, content=error.detail)
    except Exception as error:
        log.error(f"Login error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content="Login error"
        )
