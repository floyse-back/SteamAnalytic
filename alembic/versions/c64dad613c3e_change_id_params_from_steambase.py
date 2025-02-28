"""Change id params from steambase

Revision ID: c64dad613c3e
Revises: c48e8bdda273
Create Date: 2025-02-27 17:58:53.271703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c64dad613c3e'
down_revision: Union[str, None] = 'c48e8bdda273'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('steambase','id')
    op.execute('ALTER TABLE steambase ADD COLUMN id SERIAL PRIMARY KEY')

def downgrade() -> None:
    op.drop_column('steambase','id')
    op.add_column('steambase',sa.Column('id',sa.Integer))
