"""empty message

Revision ID: 96f80341a428
Revises: a94ad7a25f05
Create Date: 2019-01-30 22:14:40.823144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96f80341a428'
down_revision = 'a94ad7a25f05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('middle_name', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_employees_first_name'), 'employees', ['first_name'], unique=False)
    op.create_index(op.f('ix_employees_last_name'), 'employees', ['last_name'], unique=False)
    op.create_index(op.f('ix_employees_middle_name'), 'employees', ['middle_name'], unique=False)
    op.drop_index('ix_employees_name', table_name='employees')
    op.drop_column('employees', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('name', sa.VARCHAR(length=100), nullable=True))
    op.create_index('ix_employees_name', 'employees', ['name'], unique=False)
    op.drop_index(op.f('ix_employees_middle_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_last_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_first_name'), table_name='employees')
    op.drop_column('employees', 'middle_name')
    op.drop_column('employees', 'last_name')
    op.drop_column('employees', 'first_name')
    # ### end Alembic commands ###
