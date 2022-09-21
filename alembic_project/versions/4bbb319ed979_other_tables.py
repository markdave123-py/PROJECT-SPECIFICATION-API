"""other tables

Revision ID: 4bbb319ed979
Revises: 3b9b96bd5357
Create Date: 2022-09-19 00:37:29.837745

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4bbb319ed979'
down_revision = '3b9b96bd5357'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.add_column('users', sa.Column('user_name', sa.String(), nullable=False))
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'user_name')
    op.drop_table('tasks')
    op.drop_table('projects')
    # ### end Alembic commands ###