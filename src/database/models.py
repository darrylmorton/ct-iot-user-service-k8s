import uuid

from datetime import datetime
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import MappedColumn, Mapped

from database.config import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = MappedColumn(primary_key=True, default=uuid.uuid4())
    username: Mapped[str] = MappedColumn(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = MappedColumn(nullable=False)
    confirmed: Mapped[bool] = MappedColumn(default=False)
    enabled: Mapped[bool] = MappedColumn(default=True)
    is_admin: Mapped[bool] = MappedColumn(default=False)
    updated_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())
    created_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())


class UserDetailsModel(Base):
    __tablename__ = "user_details"

    id: Mapped[uuid.UUID] = MappedColumn(primary_key=True, default=uuid.uuid4())
    first_name: Mapped[str] = MappedColumn(nullable=False)
    last_name: Mapped[str] = MappedColumn(nullable=False)
    updated_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())
    created_at: Mapped[datetime] = MappedColumn(nullable=False, default=datetime.now())

    user_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("users.id"))
