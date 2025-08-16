import uuid
from http import HTTPStatus

from email_validator import validate_email, EmailSyntaxError
from fastapi import HTTPException

from decorators.metrics import REQUEST_COUNT
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
    def validate_id(v: str):
        if not ValidatorUtil.validate_uuid4(v):
            log.debug(f"Invalid id: {v}")

            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.BAD_REQUEST,
                path="/signup",
            ).inc()

            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid id")

        return v

    @staticmethod
    def validate_user_id(v: str):
        if not ValidatorUtil.validate_uuid4(v):
            log.debug(f"Invalid user id: {v}")

            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.BAD_REQUEST,
                path="/signup",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid user id"
            )

        return v

    @staticmethod
    def validate_username(v: str, status_code: int, path: str, message: str):
        try:
            validate_email(v, check_deliverability=False)

        except EmailSyntaxError:
            log.debug(f"Invalid username: {v}")

            REQUEST_COUNT.labels(
                method="POST",
                status=status_code,
                path=path,
            ).inc()

            raise HTTPException(
                status_code=status_code,
                detail=message,
            )

        return v

    @staticmethod
    def validate_password(v: str, status_code, path: str, message: str):
        if not isinstance(v, str) or len(v) < 8 or len(v) > 16:
            log.debug("Invalid password")

            REQUEST_COUNT.labels(
                method="POST",
                status=status_code,
                path=path,
            ).inc()

            raise HTTPException(
                status_code=status_code,
                detail=message,
            )

        return v

    @staticmethod
    def validate_first_name(v: str):
        if not isinstance(v, str) or len(v) < 2 or len(v) > 30:
            log.debug(f"Invalid first name: {v}")

            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.BAD_REQUEST,
                path="/signup",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid first_name"
            )

        return v

    @staticmethod
    def validate_last_name(v: str):
        if not isinstance(v, str) or len(v) < 2 or len(v) > 30:
            log.debug(f"Invalid last name: {v}")

            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.BAD_REQUEST,
                path="/signup",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid last_name"
            )

        return v
