"""empty message

Revision ID: 078e0e07d0af
Revises: 96f39f75e17d
Create Date: 2023-06-23 17:29:46.309090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '078e0e07d0af'
down_revision = '96f39f75e17d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sighting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sighting', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###