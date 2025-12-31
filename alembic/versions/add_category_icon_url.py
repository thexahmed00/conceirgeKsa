"""Add icon_url to service_categories

Revision ID: add_category_icon_url
Revises: add_service_domain
Create Date: 2025-12-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_category_icon_url'
down_revision: Union[str, None] = 'add_service_domain'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add `icon_url` column and index to `service_categories` table."""
    # Add column
    op.add_column('service_categories', sa.Column('icon_url', sa.String(length=500), nullable=True))
    # Create index for quick lookups
    op.create_index('idx_category_icon_url', 'service_categories', ['icon_url'])


def downgrade() -> None:
    """Remove `icon_url` column and index from `service_categories` table."""
    op.drop_index('idx_category_icon_url', 'service_categories')
    op.drop_column('service_categories', 'icon_url')
