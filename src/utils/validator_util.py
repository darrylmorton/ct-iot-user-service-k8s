import uuid
from http import HTTPStatus

from email_validator import validate_email, EmailSyntaxError
from fastapi import HTTPException
from pydantic_core.core_schema import ValidationInfo

import config
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
    def validate_uuid_path_param(request_path: str, _id: str) -> bool:
        for path_prefix in config.UUID_PATH_PARAMS_ROUTES:
            if path_prefix in request_path:
                path_params = request_path.split("/")

                return (
                    len(path_params) == 4
                    and ValidatorUtil.validate_uuid4(path_params[3])
                    and _id == path_params[3]
                )

        return False

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

    @staticmethod
    def is_user_valid(_confirmed: bool, _enabled: bool):
        if not _confirmed:
            log.debug("authenticate - user account unconfirmed")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Account unconfirmed"
            )
        if not _enabled:
            log.debug("authenticate - user account suspended")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Account suspended"
            )

    @staticmethod
    def is_admin_valid(_id: str, _is_admin: bool, _admin: bool, _request_path: str):
        if _admin != _is_admin:
            log.debug("authenticate - invalid admin status")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
            )
        if not _admin and _request_path.startswith("/api/admin"):
            log.debug("authenticate - only admins can access admin paths")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Forbidden error"
            )
        if not _admin and not ValidatorUtil.validate_uuid_path_param(
            _request_path, _id
        ):
            log.debug("authenticate - user cannot access another user record")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Forbidden error"
            )

    @staticmethod
    def is_admin_access_valid(_admin: bool, _request_path: str):
        if not _admin and _request_path.startswith("/api/admin"):
            log.debug("authenticate - only admins can access admin paths")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Forbidden error"
            )

    @staticmethod
    def is_user_access_valid(_id: str, _admin: bool, _request_path: str):
        if not _admin and not ValidatorUtil.validate_uuid_path_param(
            _request_path, str(_id)
        ):
            log.debug("authenticate - user cannot access another user record")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Forbidden error"
            )
