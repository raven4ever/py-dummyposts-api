"""create posts

Revision ID: 113d84b6395f
Revises:
Create Date: 2021-11-04 16:48:22.569464

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '113d84b6395f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))


def downgrade():
    op.drop_table('posts')
