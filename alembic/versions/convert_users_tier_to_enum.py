"""Convert users.tier from integer to plan_tier enum.

Revision ID: convert_users_tier_to_enum
Revises: change_plan_tier_to_enum
Create Date: 2026-02-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'convert_users_tier_to_enum'
down_revision: Union[str, None] = 'change_plan_tier_to_enum'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Convert users.tier column from INTEGER to plan_tier ENUM using CASE mapping."""
    # Drop current default (numeric 5000)
    op.execute("ALTER TABLE users ALTER COLUMN tier DROP DEFAULT;")
    
    # Convert column type using CASE mapping:
    # - tier >= 24999 → 'Elite'
    # - tier >= 4999  → 'Traveller'
    # - tier < 4999   → 'Lifestyle'
    # - NULL          → NULL
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN tier TYPE plan_tier
        USING (
            CASE
                WHEN tier >= 24999 THEN 'Elite'
                WHEN tier >= 4999  THEN 'Traveller'
                WHEN tier IS NULL  THEN NULL
                ELSE 'Lifestyle'
            END
        )::plan_tier;
        """
    )
    
    # Set default to 'Lifestyle'
    op.execute("ALTER TABLE users ALTER COLUMN tier SET DEFAULT 'Lifestyle'::plan_tier;")


def downgrade() -> None:
    """Revert users.tier column back to INTEGER."""
    # Drop default
    op.execute("ALTER TABLE users ALTER COLUMN tier DROP DEFAULT;")
    
    # Convert back to integer using reverse mapping:
    # - 'Elite'      → 34999
    # - 'Traveller'  → 24999
    # - 'Lifestyle'  → 4999
    # - NULL         → NULL
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN tier TYPE INTEGER
        USING (
            CASE
                WHEN tier = 'Elite'     THEN 34999
                WHEN tier = 'Traveller' THEN 24999
                WHEN tier IS NULL       THEN NULL
                ELSE 4999
            END
        );
        """
    )
    
    # Restore numeric default
    op.execute("ALTER TABLE users ALTER COLUMN tier SET DEFAULT 5000;")
