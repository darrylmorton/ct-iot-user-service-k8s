import logging
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")

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

JWT_SECRET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
JWT_TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 7


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.getLevelName(LOG_LEVEL))

    return logger
