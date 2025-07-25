"""add_phone_to_restaurants

Revision ID: 32104b404b5e
Revises: fb6dc2409cc3
Create Date: 2025-06-30 01:12:54.594491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32104b404b5e'
down_revision: Union[str, Sequence[str], None] = 'fb6dc2409cc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurants', sa.Column('phone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurants', 'phone')
    # ### end Alembic commands ###
