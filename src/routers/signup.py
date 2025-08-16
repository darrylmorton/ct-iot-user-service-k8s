from http import HTTPStatus
from fastapi import APIRouter, Body
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from database.user_details_crud import UserDetailsCrud
from logger import log
from kafka.email_producer import EmailProducer
from decorators.metrics import observability


router = APIRouter()

ROUTE_PATH = "/signup"


@router.post(ROUTE_PATH, status_code=HTTPStatus.CREATED)
@observability(path=ROUTE_PATH, method="POST", status_code=HTTPStatus.CREATED)
async def signup(
    request: Request,
    payload: schemas.SignupRequest = Body(embed=False),
) -> JSONResponse:
    try:
        username_exists = await UserCrud().find_user_by_username(payload.username)

        if username_exists:
            log.debug("Signup - username exists")

            return JSONResponse(
                status_code=HTTPStatus.CONFLICT, content={"message": "Username exists"}
            )

        user = await UserCrud().add_user(
            _username=payload.username, _password=payload.password
        )

        user_details = await UserDetailsCrud().add_user_details(
            _user_id=user.id,
            _first_name=payload.first_name,
            _last_name=payload.last_name,
        )

        EmailProducer().produce(
            email_type=config.CONFIRM_ACCOUNT_VERIFICATION_TYPE,
            username=user.username,
        )

        # TODO query should return this via join and aliases
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content={
                "username": user.username,
                "first_name": user_details.first_name,
                "last_name": user_details.last_name,
            },
        )
    except Exception as error:
        log.error(f"Signup error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Signup error"},
        )
