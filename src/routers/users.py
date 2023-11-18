from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import User, UserDetails
from src.crud import get_users, get_user_details

router = APIRouter()


@router.get("/users", response_model=list[User])
async def users(db: Session = Depends(get_db)) -> Any:
    result = get_users(db)

    return result


@router.get("/user-details", response_model=list[UserDetails])
async def user_details(db: Session = Depends(get_db)) -> Any:
    result = get_user_details(db)

    return result
