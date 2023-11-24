"""create_courses_table

Revision ID: 1588f5637079
Revises: 0a65a101e4ba
Create Date: 2023-11-24 07:50:26.903192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1588f5637079'
down_revision: Union[str, None] = '0a65a101e4ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('image', sa.Text(), nullable=True)
    )

    op.create_table(
        'classes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('link', sa.String(255), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('classes')
    op.drop_table('courses')
