"""empty message

Revision ID: 224e95dc4fa7
Revises: 4f54d1a1e44e
Create Date: 2023-06-29 12:54:44.270344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224e95dc4fa7'
down_revision = '4f54d1a1e44e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sighting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datetime', sa.String(), nullable=True))
        batch_op.drop_column('time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sighting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('datetime')

    # ### end Alembic commands ###
