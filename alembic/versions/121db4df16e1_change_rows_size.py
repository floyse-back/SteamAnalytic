"""Change rows size

Revision ID: 121db4df16e1
Revises: 
Create Date: 2025-02-27 17:27:47.378974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '121db4df16e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('steambase', 'name', type_=sa.String(400))
    op.alter_column('steambase', 'developer', type_=sa.String(400))
    op.alter_column('steambase', 'publisher', type_=sa.String(400))
    op.alter_column('steambase', 'score_rank', type_=sa.String(200))

def downgrade() -> None:
    op.alter_column('steambase', 'name', type_=sa.String(200))
    op.alter_column('steambase', 'developer', type_=sa.String(200))
    op.alter_column('steambase', 'publisher', type_=sa.String(200))
    op.alter_column('steambase', 'score_rank', type_=sa.String(200))