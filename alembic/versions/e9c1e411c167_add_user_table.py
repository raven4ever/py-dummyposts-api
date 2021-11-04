"""add user table

Revision ID: e9c1e411c167
Revises: e0f8bb98f70f
Create Date: 2021-11-04 17:00:07.780235

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e9c1e411c167'
down_revision = 'e0f8bb98f70f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False,
                              primary_key=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()'))
                    )


def downgrade():
    op.drop_table('users')
