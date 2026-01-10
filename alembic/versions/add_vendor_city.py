"""Add city column to service_vendors table

Revision ID: add_vendor_city
Revises: add_category_icon_url
Create Date: 2025-01-10 10:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_vendor_city'
down_revision: Union[str, None] = 'add_category_icon_url'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add city column to service_vendors table."""
    op.add_column('service_vendors', sa.Column('city', sa.String(length=100), nullable=True))
    op.create_index('idx_vendor_city', 'service_vendors', ['city'])


def downgrade() -> None:
    """Remove city column from service_vendors table."""
    op.drop_index('idx_vendor_city', table_name='service_vendors')
    op.drop_column('service_vendors', 'city')
