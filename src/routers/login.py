import requests
from http import HTTPStatus
from fastapi import APIRouter, Body
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from decorators.metrics import observability, REQUEST_COUNT
from logger import log
from utils.auth_util import AuthUtil


router = APIRouter()

ROUTE_PATH = "/login"
ROUTE_METHOD = "POST"


@router.post(ROUTE_PATH, response_model=schemas.User, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method=ROUTE_METHOD)
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

        # user must be valid:
        AuthUtil.is_user_valid(
            _confirmed=_user.confirmed,
            _enabled=_user.enabled,
        )

        response = requests.post(
            f"{config.AUTH_SERVICE_URL}/jwt",
            json={
                "id": str(_user.id),
                "is_admin": _user.is_admin,
            },
        )

        if response.status_code == HTTPStatus.OK:
            return JSONResponse(status_code=HTTPStatus.OK, content=response.json())
        else:
            log.debug(
                f"Login - jwt create failed: {response.status_code}, {response.text}"
            )

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Login error",
            )
    except HTTPException as error:
        log.error(f"Login http error {error}")

        REQUEST_COUNT.labels(
            method=ROUTE_METHOD, status=error.status_code, path=ROUTE_PATH
        ).inc()

        return JSONResponse(status_code=error.status_code, content=error.detail)
    except Exception as error:
        log.error(f"Login server error {error}")

        REQUEST_COUNT.labels(
            method=ROUTE_METHOD,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            path=ROUTE_PATH,
        ).inc()

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Login error"},
        )
