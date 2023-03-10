"""empty message

Revision ID: 033f4b1fe668
Revises: 
Create Date: 2023-02-15 14:08:54.854093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '033f4b1fe668'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('merch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.String(length=15), nullable=False),
    sa.Column('img', sa.BLOB(), nullable=False),
    sa.Column('mimetype', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('img')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('items', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('fuffiled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=100), nullable=False),
    sa.Column('time', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_table('user')
    op.drop_table('shows')
    op.drop_table('orders')
    op.drop_table('merch')
    # ### end Alembic commands ###
