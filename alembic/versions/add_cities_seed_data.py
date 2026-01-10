"""Add seed data for cities

Revision ID: add_cities_seed_data
Revises: add_vendor_city
Create Date: 2026-01-10 21:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'add_cities_seed_data'
down_revision = 'add_vendor_city'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add initial cities data."""
    cities_table = sa.table(
        'cities',
        sa.column('name', sa.String(100)),
        sa.column('name_ar', sa.String(100)),
        sa.column('country', sa.String(100)),
        sa.column('display_order', sa.Integer),
        sa.column('is_active', sa.Boolean),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )
    
    now = datetime.utcnow()
    
    cities_data = [
        {
            'name': 'Riyadh',
            'name_ar': 'الرياض',
            'country': 'Saudi Arabia',
            'display_order': 1,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Jeddah',
            'name_ar': 'جدة',
            'country': 'Saudi Arabia',
            'display_order': 2,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Dammam',
            'name_ar': 'الدمام',
            'country': 'Saudi Arabia',
            'display_order': 3,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Medina',
            'name_ar': 'المدينة المنورة',
            'country': 'Saudi Arabia',
            'display_order': 4,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Mecca',
            'name_ar': 'مكة المكرمة',
            'country': 'Saudi Arabia',
            'display_order': 5,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Khobar',
            'name_ar': 'الخبر',
            'country': 'Saudi Arabia',
            'display_order': 6,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Dhahran',
            'name_ar': 'الظهران',
            'country': 'Saudi Arabia',
            'display_order': 7,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Abha',
            'name_ar': 'أبها',
            'country': 'Saudi Arabia',
            'display_order': 8,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Taif',
            'name_ar': 'الطائف',
            'country': 'Saudi Arabia',
            'display_order': 9,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
        {
            'name': 'Tabuk',
            'name_ar': 'تبوك',
            'country': 'Saudi Arabia',
            'display_order': 10,
            'is_active': True,
            'created_at': now,
            'updated_at': now,
        },
    ]
    
    op.bulk_insert(cities_table, cities_data)


def downgrade() -> None:
    """Remove cities seed data."""
    op.execute("DELETE FROM cities WHERE country = 'Saudi Arabia'")
