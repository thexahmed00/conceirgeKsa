#!/usr/bin/env python
"""Fix alembic version history."""

from sqlalchemy import create_engine, text
from src.config import settings

engine = create_engine(settings.database_url)

with engine.begin() as conn:
    # Clear the table
    conn.execute(text("DELETE FROM alembic_version"))
    # Re-insert only the linear chain
    versions = [
        '1309b445fbb3',
        'add_service_domain',
        'add_category_icon_url',
        'add_vendor_city',
        'add_cities_seed_data',
        'add_service_subcategories',
    ]
    for version in versions:
        conn.execute(text(f"INSERT INTO alembic_version (version_num) VALUES ('{version}')"))
    
    # Show current versions
    result = conn.execute(text("SELECT version_num FROM alembic_version ORDER BY version_num"))
    print("✓ Migrations marked as applied (in order):")
    for (version,) in result:
        print(f"    {version}")
