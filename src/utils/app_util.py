import uuid
from pathlib import Path

import toml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import config


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
