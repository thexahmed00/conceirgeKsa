"""Add service subcategories table.

Revision ID: add_service_subcategories
Revises: add_cities_seed_data
Create Date: 2026-02-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_service_subcategories'
down_revision = 'add_cities_seed_data'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'service_subcategories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('icon_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['service_categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_subcategory_category_id', 'service_subcategories', ['category_id'])
    op.create_index('idx_subcategory_slug', 'service_subcategories', ['slug'])
    op.create_index('idx_subcategory_display_order', 'service_subcategories', ['display_order'])


def downgrade():
    op.drop_index('idx_subcategory_display_order', table_name='service_subcategories')
    op.drop_index('idx_subcategory_slug', table_name='service_subcategories')
    op.drop_index('idx_subcategory_category_id', table_name='service_subcategories')
    op.drop_table('service_subcategories')
