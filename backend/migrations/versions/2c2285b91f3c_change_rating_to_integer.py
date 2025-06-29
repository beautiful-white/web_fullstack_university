"""change_rating_to_integer

Revision ID: 2c2285b91f3c
Revises: 32104b404b5e
Create Date: 2025-06-30 06:29:00.738831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c2285b91f3c'
down_revision: Union[str, Sequence[str], None] = '32104b404b5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.alter_column('rating', type_=sa.Integer())


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.alter_column('rating', type_=sa.Float())
