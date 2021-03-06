"""empty message

Revision ID: dec62594a851
Revises: 
Create Date: 2021-03-14 19:12:16.848378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dec62594a851'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category', sa.String(), nullable=True))
    op.drop_constraint('fk_Category', 'questions', type_='foreignkey')
    op.drop_column('questions', 'category_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_Category', 'questions', 'categories', ['category_id'], ['id'])
    op.drop_column('questions', 'category')
    # ### end Alembic commands ###
