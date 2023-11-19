from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from . import config


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
