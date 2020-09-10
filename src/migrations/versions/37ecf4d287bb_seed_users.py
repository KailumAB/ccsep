"""seed users

Revision ID: 37ecf4d287bb
Revises: 56a7b72748e3
Create Date: 2020-09-10 11:20:46.847702

"""
from alembic import op
import sqlalchemy as sa
from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, DateTime


# revision identifiers, used by Alembic.
revision = '37ecf4d287bb'
down_revision = '56a7b72748e3'
branch_labels = None
depends_on = None




def upgrade():
    # Create an ad-hoc table to use for the insert statement.
    users = table('user',
        column('id', Integer),
        column('username', String),
        column('email', String),
        column('password', String),
        column('dob', DateTime),
        column('postcode', Integer),
    )
    op.bulk_insert(users,
        [
            {'id':1, 'username':'John Smith', 'email': 'john@test.com', 'password': 'johnpw', 'dob': date(1998, 5, 27), 'postcode': 6031},

            {'id':2, 'username':'Ed Williams', 'email': 'ed@test.com', 'password': 'edpw', 'dob': date(2000, 5, 27), 'postcode': 123123},

            {'id':3, 'username':'Wendy Jones', 'email': 'wendy@test.com', 'password': 'wendypw', 'dob': date(2008, 8, 15), 'postcode': 4567},
        ]
    )



def downgrade():
    pass
