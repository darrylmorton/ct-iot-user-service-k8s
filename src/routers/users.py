import logging
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas import User, UserDetails
from src.crud import get_users, get_user_details

router = APIRouter()


@router.get("/users", response_model=list[User])
async def users(db: AsyncSession = Depends(get_db)) -> Any:
    result = await get_users(db)
    logging.info(f'users {result}')

    return result.fetchall()


@router.get("/user-details", response_model=list[UserDetails])
async def user_details(db: AsyncSession = Depends(get_db)) -> Any:
    result = await get_user_details(db)
    logging.info(f'user details {result}')

    return result.fetchall()
