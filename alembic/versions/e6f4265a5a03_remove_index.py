"""remove  index

Revision ID: e6f4265a5a03
Revises: 9173ff64308c
Create Date: 2024-12-13 03:18:03.823276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e6f4265a5a03'
down_revision: Union[str, None] = '9173ff64308c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_transactions_id', table_name='transactions')
    op.drop_table('transactions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='transactions_book_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='transactions_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='transactions_pkey')
    )
    op.create_index('ix_transactions_id', 'transactions', ['id'], unique=False)
    # ### end Alembic commands ###
