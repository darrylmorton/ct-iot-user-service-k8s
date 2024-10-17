from typing import Annotated

import requests

from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Body

from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from logger import log

router = APIRouter()


@router.post("/login", response_model=schemas.User, status_code=200)
async def login(
    login_request: Annotated[schemas.LoginRequest, Body(embed=False)],
) -> JSONResponse:
    try:
        schemas.LoginRequest.model_validate(login_request)

        username = login_request.username
        password = login_request.password

        authorised_user = await UserCrud().authorise(
            _username=username, _password=password
        )
        log.info(f"{authorised_user=}")

        if not authorised_user.enabled:
            log.error("Account not enabled")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Account suspended"
            )
        else:
            log.info(f"AUTH URL: {config.AUTH_SERVICE_URL}/jwt")
            log.info(f"AUTH ID: {str(authorised_user.id)=}")
            log.info(f"AUTH ADMIN: {authorised_user.is_admin=}")

            response = requests.post(
                f"{config.AUTH_SERVICE_URL}/jwt",
                json={
                    "id": str(authorised_user.id),
                    "is_admin": authorised_user.is_admin,
                },
            )
            # log.info(f"{response.text}")
            log.info(f"AUTH RESPONSE STATUS: {response.status_code=}")

            if response.status_code == HTTPStatus.CREATED:
                return JSONResponse(status_code=HTTPStatus.OK, content=response.json())
            else:
                log.error("Cannot login")

                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Invalid username or password",
                )
    except SQLAlchemyError as error:
        log.error(f"Cannot login {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Cannot login"
        ) from error
