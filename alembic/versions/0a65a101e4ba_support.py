"""support

Revision ID: 0a65a101e4ba
Revises: 06cdd8eea987
Create Date: 2023-10-17 20:37:28.220056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0a65a101e4ba'
down_revision: Union[str, None] = '06cdd8eea987'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'support',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name_student', sa.String(length=255), nullable=False),
        sa.Column('name_responsible', sa.String(length=255), nullable=False),
        sa.Column('email_responsible', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.CheckConstraint("status IN ('aberto', 'resolvido', 'aguardando')"),
        sa.Column('date', sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('support')