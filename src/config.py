import logging
import os
from dotenv import load_dotenv

from utils import app_util

load_dotenv()

APP_VERSION = app_util.get_app_version()
SENTRY_DSN = os.getenv("SENTRY_DSN")
AWS_REGION = os.environ.get("AWS_REGION")

ENVIRONMENT = os.environ.get("ENVIRONMENT") or "DEVELOPMENT"
LOG_LEVEL = os.environ.get("LOG_LEVEL") or "INFO"
SERVICE_NAME = os.environ.get("SERVICE_NAME") or "user-service"
APP_PORT = os.environ.get("APP_PORT") or 8001

DATABASE_URL_PREFIX = "postgresql+asyncpg"
DATABASE_URL_SUFFIX = (
    "{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USERNAME=os.environ.get("DB_USERNAME"),
        DB_PASSWORD=os.environ.get("DB_PASSWORD"),
        DB_HOST=os.environ.get("DB_HOST"),
        DB_PORT=os.environ.get("DB_PORT"),
        DB_NAME=os.environ.get("DB_NAME"),
    )
)
DATABASE_URL = f"{DATABASE_URL_PREFIX}://{DATABASE_URL_SUFFIX}"

JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/signup", "/api/login"]


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.getLevelName(LOG_LEVEL))

    return logger
