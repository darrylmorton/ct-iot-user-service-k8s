import logging

from fastapi import APIRouter, Depends
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.database import get_db
from src.schemas import User, UserRequest
from src.crud import get_users, post_user, get_user_by_username

router = APIRouter()


@router.get("/users", response_model=list[User])
async def users(db: AsyncSession = Depends(get_db)) -> list[User] | JSONResponse:
    try:
        result = await get_users(db)

        return result.fetchall()
    except DatabaseError as e:
        logging.error(f"get users error {e}")

        return JSONResponse(status_code=500, content=None)


@router.get("/users/:username", response_model=User)
async def users(request: Request, db: AsyncSession = Depends(get_db)) -> User | JSONResponse:
    username = request["path"]

    try:
        result = await get_user_by_username(db, username)

        return result.fetchone()
    except DatabaseError as e:
        logging.error(f"get users error {e}")

        return JSONResponse(status_code=500, content=None)


@router.post("/users")
async def users(request: Request, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    request_payload = await request.json()
    logging.info(f"*** route users request_payload {request_payload}")

    username = UserRequest.model_validate_json(request_payload).username
    password = UserRequest.model_validate_json(request_payload).password

    user_request = UserRequest(
        username=username,
        password=password,
    )

    try:
        await post_user(db, user_request)

        return JSONResponse(status_code=201, content=None)
    except DatabaseError as e:
        logging.error(f"post users error {e}")

        return JSONResponse(status_code=500, content=None)
