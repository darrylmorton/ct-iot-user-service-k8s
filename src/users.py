from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .db import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/users", response_model=list[schemas.User])
async def users(db: Session = Depends(get_db)) -> Any:
    result = crud.get_users(db)

    return result


@router.get("/user-details", response_model=list[schemas.UserDetails])
async def user_details(db: Session = Depends(get_db)) -> Any:
    result = crud.get_user_details(db)

    return result
