import logging
import os
from urllib.parse import quote

from dotenv import load_dotenv

from utils.app_util import AppUtil

load_dotenv()

APP_VERSION = AppUtil.get_app_version()

AWS_REGION = os.environ.get("AWS_REGION")
SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE"))
SENTRY_SAMPLE_RATE = int(os.environ.get("SENTRY_SAMPLE_RATE"))

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8001

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL")
AUTH_SERVICE_URL = f"{AUTH_SERVICE_URL}/api"

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL_PREFIX = "postgresql+asyncpg"
DATABASE_URL_SUFFIX = (
    "{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USERNAME=DB_USERNAME,
        DB_PASSWORD=quote(DB_PASSWORD).replace("%", "%%"),
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_NAME=DB_NAME,
    )
)
DATABASE_URL = f"{DATABASE_URL_PREFIX}://{DATABASE_URL_SUFFIX}"

JWT_EXCLUDED_ENDPOINTS = ["/openapi.json", "/docs", "/healthz", "/api/signup"]

UUID_PATH_PARAMS_ROUTES = ["/api/users/", "/api/user-details/"]


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.getLevelName(LOG_LEVEL))

    return logger
