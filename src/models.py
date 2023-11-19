import asyncio

from datetime import datetime
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import MappedColumn, Mapped, declarative_base

from . import database

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    username: Mapped[str] = MappedColumn(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = MappedColumn(nullable=False)
    salt: Mapped[str] = MappedColumn(nullable=False)
    enabled: Mapped[bool] = MappedColumn(default=False)
    updated_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())
    created_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())


class UserDetails(Base):
    __tablename__ = "user_details"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    first_name: Mapped[str] = MappedColumn(nullable=False)
    last_name: Mapped[str] = MappedColumn(nullable=False)
    updated_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())
    created_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())

    user_id: Mapped[int] = MappedColumn(ForeignKey("users.id"))


# conn = database.engine.begin()
# conn.run_sync(Base.meta.create_all)
# database.engine.dispose()

# database.engine.begin().run_sync(Base.meta.create_all)

# asyncio.run(Base.metadata.create_all(database.engine))
