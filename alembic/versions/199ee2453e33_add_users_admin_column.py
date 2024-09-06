"""add users admin column

Revision ID: 199ee2453e33
Revises: 5f91ec0558e6
Create Date: 2024-09-04 10:42:17.638159

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "199ee2453e33"
down_revision: Union[str, None] = "5f91ec0558e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), default=False))


def downgrade() -> None:
    op.drop_column("users", "is_admin")
