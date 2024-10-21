import uuid
from http import HTTPStatus

from email_validator import validate_email, EmailSyntaxError
from fastapi import FastAPI, HTTPException
from pydantic_core.core_schema import ValidationInfo

import config
from logger import log
from utils.app_util import AppUtil


class ValidatorUtil:
    @staticmethod
    def validate_email(email: str) -> bool:
        try:
            validate_email(email)

            return True
        except EmailSyntaxError:
            log.debug(f"Invalid email: {email}")

            return False

    @staticmethod
    def validate_id(v: str, info: ValidationInfo):
        if info.field_name == "id" and not AppUtil.validate_uuid4(v):
            log.debug(f"Invalid id: {v}")

            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid id")

        return v

    @staticmethod
    def validate_user_id(v: str, info: ValidationInfo):
        if info.field_name == "user_id" and not AppUtil.validate_uuid4(v):
            log.debug(f"Invalid user id: {v}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid user id"
            )

        return v

    @staticmethod
    def validate_username(v: str, info: ValidationInfo, status_code, message: str):
        if info.field_name == "username" and not ValidatorUtil.validate_email(v):
            log.debug(f"Invalid username: {v}")

            raise HTTPException(
                status_code=status_code,
                detail=message,
            )

        return v

    @staticmethod
    def validate_password(v: str, info: ValidationInfo, status_code, message: str):
        if (
            info.field_name == "password"
            and not isinstance(v, str)
            or len(v) < 8
            or len(v) > 16
        ):
            log.debug(f"Invalid password: {v}")

            raise HTTPException(
                status_code=status_code,
                detail=message,
            )

        return v

    @staticmethod
    def validate_first_name(v: str, info: ValidationInfo):
        if (
            info.field_name == "first_name"
            and not isinstance(v, str)
            or len(v) < 2
            or len(v) > 30
        ):
            log.debug(f"Invalid first name: {v}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="1 Invalid first_name"
            )

        return v

    @staticmethod
    def validate_last_name(v: str, info: ValidationInfo):
        if (
            info.field_name == "last_name"
            and not isinstance(v, str)
            or len(v) < 2
            or len(v) > 30
        ):
            log.debug(f"Invalid last name: {v}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="1 Invalid last_name"
            )

        return v
