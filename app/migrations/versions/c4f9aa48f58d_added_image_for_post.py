"""Added image for post

Revision ID: c4f9aa48f58d
Revises: 2fffcbcd676d
Create Date: 2021-01-17 16:34:11.474364

"""
from alembic import op
import sqlalchemy as sa
from flask_image_alchemy.fields import StdImageField

# revision identifiers, used by Alembic.
revision = 'c4f9aa48f58d'
down_revision = '2fffcbcd676d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('image', StdImageField(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'image')
    # ### end Alembic commands ###
