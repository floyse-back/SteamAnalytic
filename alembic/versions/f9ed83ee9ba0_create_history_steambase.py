"""Create history steambase

Revision ID: f9ed83ee9ba0
Revises: 3b5a3d6a64ff
Create Date: 2025-03-01 10:40:02.371033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9ed83ee9ba0'
down_revision: Union[str, None] = '3b5a3d6a64ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('historysteambase',
                    sa.Column('id', sa.Integer, primary_key=True,autoincrement=True),
                    sa.Column('data',sa.JSON,nullable=False),
                    sa.Column('snapshot_date',sa.Date,nullable=False,default=sa.func.current_date())
                    )


def downgrade() -> None:
    op.drop_table('historysteambase')
