"""user confirmed

Revision ID: 5e4d6b8dab17
Revises: 199ee2453e33
Create Date: 2024-10-28 10:43:03.761489

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pygments.lexer import default

# revision identifiers, used by Alembic.
revision: str = "5e4d6b8dab17"
down_revision: Union[str, None] = "199ee2453e33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "enabled", default=True)
    op.add_column("users", sa.Column("confirmed", sa.Boolean(), default=False))


def downgrade() -> None:
    op.alter_column("users", "enabled", default=False)
    op.drop_column("users", "confirmed")
