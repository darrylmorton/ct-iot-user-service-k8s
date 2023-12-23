"""create user details table

Revision ID: 5f91ec0558e6
Revises: c4c2eafae6e5
Create Date: 2023-12-23 11:13:14.265145

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f91ec0558e6"
down_revision: Union[str, None] = "c4c2eafae6e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user-details",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.now()),
        sa.Column("updated_at", sa.DateTime, default=datetime.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade() -> None:
    op.drop_table("user-details")
