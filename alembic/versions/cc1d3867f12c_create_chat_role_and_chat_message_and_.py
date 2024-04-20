"""Create chat_role and chat_message and chat session table

Revision ID: cc1d3867f12c
Revises: 72fe738cfe31
Create Date: 2024-04-19 17:30:57.166927

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc1d3867f12c'
down_revision: Union[str, None] = '72fe738cfe31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'chat_role',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('update_at', sa.DateTime(), nullable=True),
        sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('role'),
    )
    op.create_table(
        'chat_session',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('update_at', sa.DateTime(), nullable=True),
        sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'chat_message',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.String(length=36), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('update_at', sa.DateTime(), nullable=True),
        sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['role_id'],
            ['chat_role.id'],
        ),
        sa.ForeignKeyConstraint(
            ['session_id'],
            ['chat_session.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_message')
    op.drop_table('chat_session')
    op.drop_table('chat_role')
    # ### end Alembic commands ###
