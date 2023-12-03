"""course actived

Revision ID: 7df5bdc0af22
Revises: 95f1ed16a9cf
Create Date: 2023-12-03 08:40:46.340313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7df5bdc0af22'
down_revision: Union[str, None] = '95f1ed16a9cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('courses', sa.Column('actived', sa.Boolean(), server_default='1'))


def downgrade() -> None:
    op.drop_column('courses', 'actived')
    
