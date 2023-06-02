"""add foreinkey to posts table

Revision ID: 3324a0660f5a
Revises: 949afbee80a8
Create Date: 2023-06-01 14:51:33.136713

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3324a0660f5a'
down_revision = '949afbee80a8'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    op.add_column('posts', sa.Column('username', sa.String, sa.ForeignKey("users.username", ondelete="CASCADE"), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'user_id')
    op.drop_column('posts', 'username')
    pass
