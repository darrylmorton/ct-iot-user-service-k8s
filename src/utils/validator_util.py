import uuid
from http import HTTPStatus

from email_validator import validate_email, EmailSyntaxError
from fastapi import HTTPException
from pydantic_core.core_schema import ValidationInfo

from logger import log


class ValidatorUtil:
    @staticmethod
    def validate_uuid4(uuid_string: str) -> bool:
        """
        Validate that a UUID string is in
        fact a valid uuid4.
        Happily, the uuid module does the actual
        checking for us.
        It is vital that the 'version' kwarg be passed
        to the UUID() call, otherwise any 32-character
        hex string is considered valid.
        """

        try:
            val = uuid.UUID(uuid_string, version=4)

        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            return False

        # If the uuid_string is a valid hex code,
        # but an invalid uuid4,
        # the UUID.__init__ will convert it to a
        # valid uuid4. This is bad for validation purposes.

        return str(val) == uuid_string

    @staticmethod
    def validate_email(email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)

            return True
        except EmailSyntaxError:
            log.debug(f"Invalid email: {email}")

            return False

    @staticmethod
    def validate_id(v: str, info: ValidationInfo):
        if info.field_name == "id" and not ValidatorUtil.validate_uuid4(v):
            log.debug(f"Invalid id: {v}")

            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid id")

        return v

    @staticmethod
    def validate_user_id(v: str, info: ValidationInfo):
        if info.field_name == "user_id" and not ValidatorUtil.validate_uuid4(v):
            log.debug(f"Invalid user id: {v}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid user id"
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
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid first_name"
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
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid last_name"
            )

        return v
