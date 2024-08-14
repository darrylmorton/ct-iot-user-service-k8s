import requests

from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import schemas
from crud import Crud

logger = config.get_logger()

router = APIRouter()


@router.post("/login", response_model=schemas.User, status_code=200)
async def login(req: Request) -> JSONResponse:
    request_payload = await req.json()

    try:
        schemas.LoginRequest.model_validate(request_payload)

        username = request_payload["username"]
        password = request_payload["password"]

        authorised_user = await Crud().authorise(
            _usernavme=username, _password=password
        )

        if not authorised_user.enabled:
            logger.error("Account not enabled")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Account suspended"
            )
        elif authorised_user.enabled:
            response = requests.post(f"{config.AUTH_SERVICE_URL}/jwt", username)

            if response.status_code == HTTPStatus.CREATED:
                return JSONResponse(status_code=HTTPStatus.OK, content=response.json())
            else:
                logger.error("Cannot login")

                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Invalid username or password",
                )
    except SQLAlchemyError as error:
        logger.error(f"Cannot login {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Cannot login"
        ) from error
