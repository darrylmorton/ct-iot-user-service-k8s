import logging
from fastapi import FastAPI

from src.routers import health, users
from . import config

logging.basicConfig(level=config.log_level)
logging.info(f"Environment {config.environment}")
logging.info(f"Service name {config.service_name}")
logging.info(f"Log level {config.log_level}")

app = FastAPI()

app.include_router(health.router)
app.include_router(users.router)
