import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.environ.get("AWS_REGION")
SES_SOURCE = os.environ.get("SES_SOURCE")

SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT") or "local"
SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE"))
SENTRY_SAMPLE_RATE = int(os.environ.get("SENTRY_SAMPLE_RATE"))

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8001

QUEUE_WAIT_SECONDS = int(os.environ.get("QUEUE_WAIT_SECONDS"))
SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE = "ACCOUNT_VERIFICATION"
SQS_EMAIL_QUEUE_NAME = os.environ.get("SQS_EMAIL_QUEUE_NAME")
SQS_EMAIL_DLQ_NAME = os.environ.get("SQS_EMAIL_DLQ_NAME")

AUTH_SERVICE_ENDPOINT = os.environ.get("AUTH_SERVICE_URL")
AUTH_SERVICE_URL = f"{AUTH_SERVICE_ENDPOINT}/api"

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

HTTP_STATUS_CODE_EXPIRED_TOKEN = 498
JWT_SECRET_VERIFY_ACCOUNT = os.environ.get("JWT_SECRET_VERIFY_ACCOUNT")
JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT = int(os.environ.get("JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT"))
ALB_URL = os.environ.get("ALB_URL")

JWT_EXCLUDED_ENDPOINTS = [
    "/favicon.ico",
    "/openapi.json",
    "/docs",
    "/healthz",
    "/api/signup",
    "/api/login",
    "/api/account-confirmation",
]

UUID_PATH_PARAMS_ROUTES = ["/api/users/", "/api/user-details/"]
