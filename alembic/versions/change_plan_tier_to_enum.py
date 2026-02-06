"""Change plan tier from integer to enum.

Revision ID: change_plan_tier_to_enum
Revises: add_service_subcategories
Create Date: 2026-02-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from src.domain.plan.entities.plan_tier import PlanTier

# revision identifiers, used by Alembic.
revision = 'change_plan_tier_to_enum'
down_revision = 'add_service_subcategories'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema - convert tier column to enum."""
    # Create the enum type
    plan_tier_enum = postgresql.ENUM(
        'Lifestyle', 'Traveller', 'Elite',
        name='plan_tier',
        create_type=True
    )
    plan_tier_enum.create(op.get_bind(), checkfirst=True)
    
    # Alter the column to use the enum type
    # First, we need to cast the integer values to text and then to enum
    op.execute("""
        ALTER TABLE plans 
        ALTER COLUMN tier TYPE plan_tier 
        USING CASE 
            WHEN tier >= 24999 THEN 'Elite'::plan_tier
            WHEN tier >= 4999 THEN 'Traveller'::plan_tier
            ELSE 'Lifestyle'::plan_tier
        END
    """)


def downgrade() -> None:
    """Downgrade database schema - revert enum back to integer."""
    # Convert enum back to integer
    op.execute("""
        ALTER TABLE plans 
        ALTER COLUMN tier TYPE integer 
        USING CASE 
            WHEN tier = 'Lifestyle'::plan_tier THEN 4999
            WHEN tier = 'Traveller'::plan_tier THEN 24999
            WHEN tier = 'Elite'::plan_tier THEN 100000
            ELSE 0
        END
    """)
    
    # Drop the enum type
    op.execute("DROP TYPE plan_tier")
