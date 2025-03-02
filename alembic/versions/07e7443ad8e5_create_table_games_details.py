"""Create Table Games_details

Revision ID: 07e7443ad8e5
Revises: ff8c5a62761d
Create Date: 2025-03-01 14:51:56.047874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07e7443ad8e5'
down_revision: Union[str, None] = 'ff8c5a62761d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
