"""empty message

Revision ID: 4ee341e08717
Revises: 47ae2611efbc
Create Date: 2021-01-10 15:29:08.533681

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4ee341e08717'
down_revision = '47ae2611efbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('post_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='posts_author_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='posts_pkey')
    )
    # ### end Alembic commands ###
