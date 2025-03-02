"""Update appid to steambases

Revision ID: 8005d2faa76d
Revises: 7fb9eeb420ac
Create Date: 2025-03-02 11:05:55.137493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8005d2faa76d'
down_revision: Union[str, None] = '7fb9eeb420ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('steambase','appid',type_=sa.Integer,postgresql_using="appid::integer")


def downgrade() -> None:
    op.alter_column('steambase', 'appid',
                    type_=sa.String(),  # Змініть на попередній тип
                    postgresql_using='appid::text')