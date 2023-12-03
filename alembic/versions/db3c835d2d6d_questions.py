"""questions

Revision ID: db3c835d2d6d
Revises: 7df5bdc0af22
Create Date: 2023-12-03 09:03:28.433155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db3c835d2d6d'
down_revision: Union[str, None] = '7df5bdc0af22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, nullable=False),
        sa.Column('statement', sa.String(255), nullable=False),
    )

    op.create_table(
        'questions_answers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('question_id', sa.Integer, nullable=False),
        sa.Column('option', sa.String(255), nullable=False),
        sa.Column('correct', sa.Boolean(), server_default='0'),
        sa.Column('order', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('questions_answers')
    op.drop_table('questions')
