"""create posts table

Revision ID: f3a39b55aa1e
Revises: 
Create Date: 2023-06-01 14:06:50.966968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a39b55aa1e'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default='TRUE'),
        sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass