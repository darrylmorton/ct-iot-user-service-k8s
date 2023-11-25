from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas import UserDetails
from src.crud import get_user_details

router = APIRouter()


@router.get("/user-details", response_model=list[UserDetails])
async def user_details(db: AsyncSession = Depends(get_db)) -> list[UserDetails]:
    result = await get_user_details(db)

    return result.fetchall()
