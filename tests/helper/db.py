from src.models import User
from src.database import SessionLocal


async def cleanup():
    db = await SessionLocal()
    await db.query(User).delete()
    await db.commit()

