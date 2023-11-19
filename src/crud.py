from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import models


async def get_users(db: AsyncSession):
    return await db.execute(select(models.User.id, models.User.username).limit(1))


async def get_user_details(db: AsyncSession):
    return await db.execute(select(models.UserDetails.id, models.UserDetails.user_id, models.UserDetails.first_name,
                                   models.UserDetails.last_name).limit(1))
