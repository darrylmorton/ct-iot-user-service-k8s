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

login_examples = [schemas.LoginRequest(username="foo@bar.com", password="barbarba")]


@router.post("/login", response_model=schemas.User, status_code=HTTPStatus.OK)
async def login(
    payload: schemas.LoginRequest = Body(embed=False, examples=login_examples),
) -> JSONResponse:
    try:
        authorised_user = await UserCrud().authorise(
            _username=payload.username, _password=payload.password
        )

        if not authorised_user.id:
            log.error("Invalid login")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Invalid login credentials"
            )
        elif not authorised_user.enabled:
            log.error("Account not enabled")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Account not enabled"
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
