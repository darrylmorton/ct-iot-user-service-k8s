from fastapi import FastAPI

from src.routers import users, health

app = FastAPI()

app.include_router(health.router)
app.include_router(users.router)
