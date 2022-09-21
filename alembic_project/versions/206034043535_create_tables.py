"""create tables

Revision ID: 206034043535
Revises: 09621163a733
Create Date: 2022-09-19 00:56:55.082747

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '206034043535'
down_revision = '09621163a733'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('admins', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('participants', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('project_status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('projectID', sa.Integer(), nullable=False),
    sa.Column('assignedTo', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('deadline', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['projectID'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table("users",sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                            sa.Column('first_name', sa.String(), nullable = False),
                            sa.Column('last_name', sa.String(), nullable = False),
                            sa.Column('password', sa.String(), nullable = False),
                            sa.Column('user_name', sa.String(), nullable = False),
                            sa.Column('email', sa.String(), nullable = False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                            server_default = sa.text('now()'),nullable = False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
    )
    
    pass


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('projects')
    pass
