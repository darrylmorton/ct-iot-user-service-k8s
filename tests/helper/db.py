from sqlalchemy import delete

from src.models import User
from src.database import AsyncSessionLocal


async def cleanup():
    db = AsyncSessionLocal()
    await db.execute(delete(User))
    await db.commit()
