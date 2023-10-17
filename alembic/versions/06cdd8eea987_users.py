"""users

Revision ID: 06cdd8eea987
Revises: 
Create Date: 2023-10-09 16:04:27.440049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06cdd8eea987'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('birth', sa.INTEGER(), nullable=False),
        sa.Column('name_responsible', sa.String(length=255), nullable=False),
        sa.Column('email_responsible', sa.String(length=255), nullable=False),
        sa.Column('cpf_responsible', sa.String(length=255), nullable=False),
        sa.Column('zip_code', sa.String(length=255), nullable=False),
        sa.Column('city', sa.String(length=255)),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=False),
        sa.Column('scholarship_holder', sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

def downgrade():
    op.drop_table('users')