"""empty message

Revision ID: 8f3454933a7d
Revises: 050417f9443d
Create Date: 2020-07-20 23:48:23.586320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3454933a7d'
down_revision = '050417f9443d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('premium_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('coin_price', sa.Integer(), nullable=True),
    sa.Column('experience_price', sa.Integer(), nullable=True),
    sa.Column('num_available', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('progression_premium_item',
    sa.Column('progression_id', sa.Integer(), nullable=True),
    sa.Column('premium_item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['premium_item_id'], ['premium_item.id'], ),
    sa.ForeignKeyConstraint(['progression_id'], ['verifier_progression.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('progression_premium_item')
    op.drop_table('premium_item')
    # ### end Alembic commands ###