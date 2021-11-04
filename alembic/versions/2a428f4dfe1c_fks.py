"""fks

Revision ID: 2a428f4dfe1c
Revises: e9c1e411c167
Create Date: 2021-11-04 17:08:58.297264

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2a428f4dfe1c'
down_revision = 'e9c1e411c167'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts',
                          referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
