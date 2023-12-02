"""complementary_material

Revision ID: 9b3c77e8cfab
Revises: 1588f5637079
Create Date: 2023-12-02 11:30:53.466092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b3c77e8cfab'
down_revision: Union[str, None] = '1588f5637079'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'complementary_material',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, nullable=False),
        sa.Column('file', sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('complementary_material')
