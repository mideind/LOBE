"""empty message

Revision ID: 302e9ce12252
Revises: 1a78b320642f
Create Date: 2020-07-16 15:29:52.346519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '302e9ce12252'
down_revision = '1a78b320642f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Mos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('num_samples', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['Collection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MosInstance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mos_id', sa.Integer(), nullable=True),
    sa.Column('recording_id', sa.Integer(), nullable=True),
    sa.Column('synthesized_audio_path', sa.String(), nullable=True),
    sa.Column('mos_instance_type', sa.String(), nullable=True),
    sa.Column('mos_selected', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['mos_id'], ['Mos.id'], ),
    sa.ForeignKeyConstraint(['recording_id'], ['Recording.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MosRating',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('MosInastance_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['MosInastance_id'], ['MosInstance.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('progression_lootbox')
    op.drop_table('verifier_lootbox')
    op.drop_table('mos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('collection_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('num_samples', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['Collection.id'], name='mos_collection_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='mos_pkey')
    )
    op.create_table('verifier_lootbox',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('verifier_lootbox_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rarity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='verifier_lootbox_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('progression_lootbox',
    sa.Column('progression_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lootbox_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['lootbox_id'], ['verifier_lootbox.id'], name='progression_lootbox_lootbox_id_fkey'),
    sa.ForeignKeyConstraint(['progression_id'], ['verifier_progression.id'], name='progression_lootbox_progression_id_fkey')
    )
    op.drop_table('MosRating')
    op.drop_table('MosInstance')
    op.drop_table('Mos')
    # ### end Alembic commands ###
