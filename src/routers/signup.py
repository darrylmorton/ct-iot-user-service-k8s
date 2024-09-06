from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import config
import schemas
from database.user_crud import UserCrud
from database.user_details_crud import UserDetailsCrud

logger = config.get_logger()

router = APIRouter()


@router.post(
    "/signup", response_model=schemas.SignupResponse, status_code=HTTPStatus.CREATED
)
async def signup(
    signup_request: Annotated[schemas.SignupRequest, Body(embed=False)],
) -> JSONResponse | schemas.SignupResponse:
    validation_status_code = HTTPStatus.UNAUTHORIZED
    validation_message = "Invalid username or password"

    try:
        username_exists = await UserCrud().find_user_by_username(
            signup_request.username
        )

        if username_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Username exists"
            )

        user = await UserCrud().add_user(
            _username=signup_request.username, _password=signup_request.password
        )

        validation_status_code = HTTPStatus.BAD_REQUEST
        validation_message = "Invalid first or last name"

        user_details = await UserDetailsCrud().add_user_details(
            _user_id=user.id,
            _first_name=signup_request.first_name,
            _last_name=signup_request.last_name,
        )

        return schemas.SignupResponse(
            username=user.username,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
        )
    except ValidationError as error:
        logger.debug("signup validation error")

        raise HTTPException(
            status_code=validation_status_code, detail=validation_message
        ) from error
    except SQLAlchemyError as error:
        logger.error(f"Cannot signup {error}")

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Cannot signup"
        ) from error
