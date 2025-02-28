"""Change validation Steam

Revision ID: 3b5a3d6a64ff
Revises: c64dad613c3e
Create Date: 2025-02-28 10:49:06.293819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b5a3d6a64ff'
down_revision: Union[str, None] = 'c64dad613c3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('steambase', 'average_forever', type_=sa.Integer, existing_type=sa.String, postgresql_using='average_forever::integer')
    op.alter_column('steambase', 'average_2weeks', type_=sa.Integer, existing_type=sa.String, postgresql_using='average_2weeks::integer')
    op.alter_column('steambase', 'median_2weeks', type_=sa.Integer, existing_type=sa.String, postgresql_using='median_2weeks::integer')
    op.alter_column('steambase', 'median_forever', type_=sa.Integer, existing_type=sa.String, postgresql_using='median_forever::integer')
    op.alter_column('steambase', 'discount', type_=sa.Integer, existing_type=sa.String, postgresql_using='discount::integer')

def downgrade() -> None:
    op.alter_column('steambase', 'average_forever', type_=sa.String, existing_type=sa.Integer, postgresql_using='average_forever::text')
    op.alter_column('steambase', 'average_2weeks', type_=sa.String, existing_type=sa.Integer, postgresql_using='average_2weeks::text')
    op.alter_column('steambase', 'median_2weeks', type_=sa.String, existing_type=sa.Integer, postgresql_using='median_2weeks::text')
    op.alter_column('steambase', 'median_forever', type_=sa.String, existing_type=sa.Integer, postgresql_using='median_forever::text')
    op.alter_column('steambase', 'discount', type_=sa.String, existing_type=sa.Integer, postgresql_using='discount::text')
