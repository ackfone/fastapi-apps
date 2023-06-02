"""create users table

Revision ID: 949afbee80a8
Revises: f3a39b55aa1e
Create Date: 2023-06-01 14:42:40.278105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '949afbee80a8'
down_revision = 'f3a39b55aa1e'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass

def downgrade():
    op.drop_table('users')
    pass