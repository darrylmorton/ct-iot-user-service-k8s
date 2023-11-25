from sqlalchemy import delete, select, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import db_host, db_name, db_port, db_username, db_password


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def cleanup(db: AsyncSession):
    # db = AsyncSessionLocal()
    # result = await db.execute(select(User))
    # await db.delete(result)
    await db.execute(delete(User))
    await db.commit()
    # await db.close()
