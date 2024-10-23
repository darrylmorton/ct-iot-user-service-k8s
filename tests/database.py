from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from tests.config import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, autoflush=True)
Base = declarative_base()
