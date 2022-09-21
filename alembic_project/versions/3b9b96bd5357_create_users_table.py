"""create users table

Revision ID: 3b9b96bd5357
Revises: 
Create Date: 2022-09-19 00:06:37.951842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b9b96bd5357'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                            sa.Column('first_name', sa.String, nullable = False),
                            sa.Column('last_name', sa.String, nullable = False),
                            sa.Column('password', sa.String, nullable = False),
                            sa.Column('email', sa.String,nullable = False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                            server_default = sa.text('now()'),nullable = False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
