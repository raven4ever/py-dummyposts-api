"""finalize posts

Revision ID: 35125df1f872
Revises: 2a428f4dfe1c
Create Date: 2021-11-04 17:13:34.159186

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '35125df1f872'
down_revision = '2a428f4dfe1c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean,
                                     nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text('now()'))
                  )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
