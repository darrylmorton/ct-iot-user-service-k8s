import requests

from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Body
from pydantic import ValidationError

from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from logger import log

router = APIRouter()


@router.post("/login", response_model=schemas.User, status_code=HTTPStatus.OK)
async def login(payload: schemas.LoginRequest = Body(embed=False)) -> JSONResponse:
    try:
        authorised_user = await UserCrud().authorise(
            _username=payload.username, _password=payload.password
        )

        if not authorised_user.enabled:
            log.error("Account not enabled")

            # raise HTTPException(
            #     status_code=HTTPStatus.FORBIDDEN, detail="Account suspended"
            # )
            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN,
                content={"message": "Account suspended"},
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
    except ValidationError as error:
        log.debug(f"**** login - validation error HELLO {error}")
        log.debug(f"login - validation error {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )
    except SQLAlchemyError as error:
        log.error(f"Cannot login {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Cannot login"
        ) from error
