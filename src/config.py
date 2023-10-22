import os

from dotenv import load_dotenv

load_dotenv()

environment = os.environ.get("ENVIRONMENT")
log_level = os.environ.get("LOG_LEVEL")
service_name = os.environ.get("SERVICE_NAME")
