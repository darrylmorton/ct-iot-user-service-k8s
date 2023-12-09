import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")

# db_host = os.environ.get("DB_HOST")
# db_port = os.environ.get("DB_PORT")
# db_username = os.environ.get("DB_USERNAME")
# db_password = os.environ.get("DB_PASSWORD")
# db_name = os.environ.get("DB_NAME")

DATABASE_URL = (
    # f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USERNAME=os.environ.get("DB_USERNAME"),
        DB_PASSWORD=os.environ.get("DB_PASSWORD"),
        DB_HOST=os.environ.get("DB_HOST"),
        DB_PORT=os.environ.get("DB_PORT"),
        DB_NAME=os.environ.get("DB_NAME"),
    )
)

# class Config:
#     LOG_CONFIG = os.getenv(
#       "LOG_CONFIG",
#       ENVIRONMENT
#     ),
#     DB_CONFIG = os.getenv(
#         "DB_CONFIG",
#         "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
#             DB_USERNAME=os.environ.get("DB_USERNAME"),
#             DB_PASSWORD=os.environ.get("DB_PASSWORD"),
#             DB_HOST= os.environ.get("DB_HOST"),
#             DB_PORT=os.environ.get("DB_PORT"),
#             DB_NAME=os.environ.get("DB_NAME")
#         ),
#     )
#
#
# config = Config
