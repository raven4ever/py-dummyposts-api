"""add content column to posts

Revision ID: e0f8bb98f70f
Revises: 113d84b6395f
Create Date: 2021-11-04 16:55:38.781625

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e0f8bb98f70f'
down_revision = '113d84b6395f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
