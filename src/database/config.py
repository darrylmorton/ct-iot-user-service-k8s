from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from utils.app_util import AppUtil


db_url = AppUtil.get_sqlalchemy_db_url()

async_engine = create_async_engine(db_url, future=True, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, autoflush=True)
Base = declarative_base()
