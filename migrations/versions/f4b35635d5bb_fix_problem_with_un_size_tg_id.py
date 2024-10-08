"""fix problem with un-size tg id

Revision ID: f4b35635d5bb
Revises: 0be70e591bed
Create Date: 2024-07-25 04:36:56.256932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4b35635d5bb'
down_revision: Union[str, None] = '0be70e591bed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admins', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('chats', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('operators', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('operators', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('chats', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('admins', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
