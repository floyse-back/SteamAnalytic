"""Create users table

Revision ID: ff8c5a62761d
Revises: f9ed83ee9ba0
Create Date: 2025-03-01 12:59:40.088566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff8c5a62761d'
down_revision: Union[str, None] = 'f9ed83ee9ba0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True,autoincrement=True),
                    sa.Column('username',sa.String(200),nullable=False),
                    sa.Column('hashed_password',sa.String(200),nullable=False),
                    sa.Column('email',sa.String(200),nullable = False),
                    sa.Column('steam_id',sa.String(200),nullable=False),
                    sa.Column('is_active',sa.Boolean,nullable=False,default=True),
                    sa.Column('role',sa.String(200),nullable=False,default='user'),
                    sa.Column("steam_img_url",sa.String(200),nullable=False,default='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg'),
                    sa.Column('created_at',sa.DateTime,nullable=False,default=sa.func.current_timestamp())
                    )


def downgrade() -> None:
    op.drop_table('users')
