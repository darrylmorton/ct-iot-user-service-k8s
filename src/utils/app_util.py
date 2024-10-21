import uuid
from pathlib import Path

import toml
from email_validator import validate_email, EmailSyntaxError
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import config
from logger import log


class AppUtil:
    @staticmethod
    def set_openapi_info(app: FastAPI) -> FastAPI:
        app.openapi_schema = get_openapi(
            title=config.SERVICE_NAME,
            version=config.APP_VERSION,
            routes=app.routes,
        )

        return app

    @staticmethod
    def get_app_version():
        app_version = None

        pyproject_toml_file = Path(__file__).parent.parent.parent / "pyproject.toml"

        if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
            app_version = toml.load(pyproject_toml_file)["tool"]["poetry"]["version"]

        return app_version

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
                    and AppUtil.validate_uuid4(path_params[3])
                    and _id == path_params[3]
                )

        return False

    @staticmethod
    def validate_email(email: str) -> bool:
        log.info(f"******* VALIDATE CALLED {email=}")

        try:
            result = validate_email(email)
            log.info(f"******* VALIDATE RESULT {result=}")

            return True
        except EmailSyntaxError:
            log.debug(f"Invalid email: {email}")

            return False
