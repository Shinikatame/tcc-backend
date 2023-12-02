"""phone_responsible column

Revision ID: 95f1ed16a9cf
Revises: 9b3c77e8cfab
Create Date: 2023-12-02 12:23:15.700570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95f1ed16a9cf'
down_revision: Union[str, None] = '9b3c77e8cfab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_responsible', sa.String(length=255), nullable=True))



def downgrade() -> None:
    op.drop_column('phone_responsible', 'email')
