import logging
from fastapi.logger import logger as fastapi_logger
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")

DATABASE_URL = "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
    DB_USERNAME=os.environ.get("DB_USERNAME"),
    DB_PASSWORD=os.environ.get("DB_PASSWORD"),
    DB_HOST=os.environ.get("DB_HOST"),
    DB_PORT=os.environ.get("DB_PORT"),
    DB_NAME=os.environ.get("DB_NAME"),
)

JWT_SECRET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
JWT_TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 7

# LOGGER = logging.getLogger("gunicorn.info")
# fastapi_logger.handlers = LOGGER.handlers
# fastapi_logger.setLevel(LOGGER.level)

# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
