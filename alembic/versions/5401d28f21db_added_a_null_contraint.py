"""added a null contraint

Revision ID: 5401d28f21db
Revises: d7a75ddfc4a5
Create Date: 2024-12-09 00:46:09.476847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5401d28f21db'
down_revision: Union[str, None] = 'd7a75ddfc4a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'file_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'file_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
