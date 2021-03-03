"""empty message

Revision ID: 402c4b6e91e7
Revises: 888acd024b5b
Create Date: 2021-03-02 21:30:16.004581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '402c4b6e91e7'
down_revision = '888acd024b5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('cost_in_credits', sa.String(length=250), nullable=False),
    sa.Column('max_atmosphering_speed', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    # ### end Alembic commands ###
