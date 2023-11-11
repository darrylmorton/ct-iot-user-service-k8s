import datetime

from sqlalchemy import (
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    MappedColumn,
    Mapped,
)

from . import database


class User(database.Base):
    __tablename__ = "users"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    username: Mapped[str] = MappedColumn(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = MappedColumn(nullable=False)
    salt: Mapped[str] = MappedColumn(nullable=False)
    enabled: Mapped[bool] = MappedColumn(default=False)
    updated_at: Mapped[datetime.date] = MappedColumn(nullable=False, default=func.now)
    created_at: Mapped[datetime.date] = MappedColumn(nullable=False, default=func.now)


class UserDetails(database.Base):
    __tablename__ = "user_details"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    first_name: Mapped[str] = MappedColumn(nullable=False)
    last_name: Mapped[str] = MappedColumn(nullable=False)
    updated_at: Mapped[datetime.date] = MappedColumn(nullable=False, default=func.now())
    created_at: Mapped[datetime.date] = MappedColumn(nullable=False, default=func.now())

    user_id: Mapped[int] = MappedColumn(ForeignKey("users.id"))


database.Base.metadata.create_all(database.engine)
