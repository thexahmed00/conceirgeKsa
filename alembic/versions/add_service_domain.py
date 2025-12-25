"""Add service domain tables

Revision ID: add_service_domain
Revises: 1309b445fbb3
Create Date: 2025-12-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_service_domain'
down_revision: Union[str, None] = '1309b445fbb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create service_categories table
    op.create_table(
        'service_categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('idx_category_slug', 'service_categories', ['slug'])
    op.create_index('idx_category_display_order', 'service_categories', ['display_order'])
    
    # Create service_vendors table
    op.create_table(
        'service_vendors',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('whatsapp', sa.String(length=50), nullable=True),
        sa.Column('rating', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('vendor_metadata', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['category_id'], ['service_categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_vendor_category_id', 'service_vendors', ['category_id'])
    op.create_index('idx_vendor_is_active', 'service_vendors', ['is_active'])
    op.create_index('idx_vendor_rating', 'service_vendors', ['rating'])
    op.create_index('idx_vendor_created_at', 'service_vendors', ['created_at'])
    
    # Create vendor_images table
    op.create_table(
        'vendor_images',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('vendor_id', sa.Integer(), nullable=False),
        sa.Column('image_type', sa.String(length=20), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('thumbnail_url', sa.String(length=500), nullable=True),
        sa.Column('caption', sa.String(length=255), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['vendor_id'], ['service_vendors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_image_vendor_id', 'vendor_images', ['vendor_id'])
    op.create_index('idx_image_type', 'vendor_images', ['image_type'])
    op.create_index('idx_image_vendor_type', 'vendor_images', ['vendor_id', 'image_type'])
    op.create_index('idx_image_display_order', 'vendor_images', ['display_order'])
    
    # Add vendor_id column to requests table
    op.add_column('requests', sa.Column('vendor_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_requests_vendor_id',
        'requests',
        'service_vendors',
        ['vendor_id'],
        ['id'],
        ondelete='SET NULL'
    )
    op.create_index('idx_requests_vendor_id', 'requests', ['vendor_id'])
    
    # Seed initial categories
    op.execute("""
        INSERT INTO service_categories (slug, name, display_order) VALUES
        ('restaurant', 'Restaurant', 1),
        ('private_jet', 'Private Jet', 2),
        ('flight', 'Flight', 3),
        ('car', 'Car', 4),
        ('hotel', 'Hotel', 5),
        ('car_driver', 'Car & Driver', 6),
        ('events', 'Events', 7),
        ('shopping', 'Shopping', 8)
    """)


def downgrade() -> None:
    # Remove vendor_id from requests
    op.drop_index('idx_requests_vendor_id', 'requests')
    op.drop_constraint('fk_requests_vendor_id', 'requests', type_='foreignkey')
    op.drop_column('requests', 'vendor_id')
    
    # Drop vendor_images table
    op.drop_index('idx_image_display_order', 'vendor_images')
    op.drop_index('idx_image_vendor_type', 'vendor_images')
    op.drop_index('idx_image_type', 'vendor_images')
    op.drop_index('idx_image_vendor_id', 'vendor_images')
    op.drop_table('vendor_images')
    
    # Drop service_vendors table
    op.drop_index('idx_vendor_created_at', 'service_vendors')
    op.drop_index('idx_vendor_rating', 'service_vendors')
    op.drop_index('idx_vendor_is_active', 'service_vendors')
    op.drop_index('idx_vendor_category_id', 'service_vendors')
    op.drop_table('service_vendors')
    
    # Drop service_categories table
    op.drop_index('idx_category_display_order', 'service_categories')
    op.drop_index('idx_category_slug', 'service_categories')
    op.drop_table('service_categories')
