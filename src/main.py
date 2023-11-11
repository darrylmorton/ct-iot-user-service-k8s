import logging
from fastapi import FastAPI

from src.routers import health
from . import users, database, config

logging.basicConfig(level=config.log_level)
logging.info(f"Environment {config.environment}")
logging.info(f"Service name {config.service_name}")
logging.info(f"Log level {config.log_level}")

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(health.router)
app.include_router(users.router)
