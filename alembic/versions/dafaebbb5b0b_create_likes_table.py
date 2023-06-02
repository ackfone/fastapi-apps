"""create likes table

Revision ID: dafaebbb5b0b
Revises: 3324a0660f5a
Create Date: 2023-06-01 15:06:44.435576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dafaebbb5b0b'
down_revision = '3324a0660f5a'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'likes',
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column('post_id', sa.Integer, sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column('like_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass

def downgrade():
    op.drop_table('likes')
    pass
