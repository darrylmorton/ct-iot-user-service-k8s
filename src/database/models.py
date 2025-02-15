import uuid

from datetime import datetime
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.config import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    confirmed: Mapped[bool] = mapped_column(default=False)
    enabled: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())


class UserDetailsModel(Base):
    __tablename__ = "user_details"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
