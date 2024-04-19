"""Create embedding_file table

Revision ID: 72fe738cfe31
Revises:
Create Date: 2024-04-18 21:36:57.593957

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72fe738cfe31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'embedding_file',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('raw_filename', sa.String(length=20), nullable=False),
        sa.Column('azure_blob_url', sa.Text(), nullable=False),
        sa.Column('update_at', sa.DateTime(), nullable=True),
        sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('embedding_file')
    # ### end Alembic commands ###