"""empty message

Revision ID: f6dfac78b414
Revises: 
Create Date: 2020-07-22 22:10:55.149152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6dfac78b414'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('idade', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('permission', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('price', sa.String(length=10), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('postagens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('caption', sa.String(length=200), nullable=False),
    sa.Column('img_url', sa.String(length=200), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('postagem_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['postagem_id'], ['postagens.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('postagens')
    op.drop_table('products')
    op.drop_table('users')
    # ### end Alembic commands ###