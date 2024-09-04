"""create users table

Revision ID: c4c2eafae6e5
Revises: 
Create Date: 2023-12-23 08:30:45.611852

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4c2eafae6e5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(64), nullable=False),
        sa.Column("enabled", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime, default=datetime.now()),
        sa.Column("updated_at", sa.DateTime, default=datetime.now()),
        sa.Index("idx_users_username", "username"),
    )


def downgrade() -> None:
    op.drop_table("users")
