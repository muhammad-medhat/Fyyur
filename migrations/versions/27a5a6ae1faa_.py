"""empty message

Revision ID: 27a5a6ae1faa
Revises: 
Create Date: 2021-03-18 00:31:28.836147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27a5a6ae1faa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('artists', sa.Column('seeking_talent', sa.String(), nullable=True))
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('artists', 'seeking_talent')
    op.drop_column('artists', 'address')
    # ### end Alembic commands ###