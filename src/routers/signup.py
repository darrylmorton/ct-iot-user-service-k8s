from http import HTTPStatus
from http.client import responses

# from alembic.util import status
from fastapi import APIRouter, HTTPException, Body
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from database.user_details_crud import UserDetailsCrud
from logger import log

logger = config.get_logger()

router = APIRouter()


@router.post("/signup", status_code=HTTPStatus.CREATED)
async def signup(
    payload: schemas.SignupRequest = Body(embed=False),
) -> JSONResponse:
    # validation_status_code = HTTPStatus.BAD_REQUEST
    # validation_message = "Invalid username or password"

    try:
        username_exists = await UserCrud().find_user_by_username(payload.username)

        if username_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Username exists"
            )

        user = await UserCrud().add_user(
            _username=payload.username, _password=payload.password
        )

        # validation_status_code = HTTPStatus.BAD_REQUEST
        # validation_message = "Invalid first or last name"

        user_details = await UserDetailsCrud().add_user_details(
            _user_id=str(user.id),
            _first_name=payload.first_name,
            _last_name=payload.last_name,
        )

        # result = schemas.SignupResponse(
        #     username=user.username,
        #     first_name=user_details.first_name,
        #     last_name=user_details.last_name,
        # )
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            # content=result
            content={
                "username": user.username,
                "first_name": user_details.first_name,
                "last_name": user_details.last_name,
            },
        )
    # except ValidationError as error:
    #     logger.debug("signup validation error")
    #
    #     raise HTTPException(
    #         status_code=HTTPStatus.BAD_REQUEST, detail="Invalid first or last name"
    #     ) from error
    except SQLAlchemyError as error:
        logger.error(f"Cannot signup {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Cannot signup"
        ) from error
