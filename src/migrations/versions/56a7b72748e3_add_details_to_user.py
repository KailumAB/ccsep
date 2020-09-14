"""Add details to user

Revision ID: 5d4231b8b67a
Revises: 508d8dfd7e99
Create Date: 2020-09-10 09:35:45.152471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56a7b72748e3'
down_revision = '5d4231b8b67a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('dob', sa.DateTime))
    op.add_column('user', sa.Column('postcode', sa.Integer()))

def downgrade():
    pass
