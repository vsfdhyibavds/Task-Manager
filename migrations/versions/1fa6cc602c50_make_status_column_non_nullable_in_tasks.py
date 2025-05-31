"""Make status column non-nullable in tasks

Revision ID: 1fa6cc602c50
Revises: 4f759a0ee549
Create Date: 2025-05-30 20:13:20.338133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fa6cc602c50'
down_revision: Union[str, None] = '4f759a0ee549'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
