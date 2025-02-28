"""Delete Row score rank

Revision ID: c48e8bdda273
Revises: 121db4df16e1
Create Date: 2025-02-27 17:49:55.190657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c48e8bdda273'
down_revision: Union[str, None] = '121db4df16e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('steambase','score_rank')


def downgrade() -> None:
    op.add_column('steambase',sa.Column('score_rank',sa.String(200)))
