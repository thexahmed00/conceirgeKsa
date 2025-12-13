-- Migration: Add is_admin column to users table
-- Run this script to add admin support

-- Add is_admin column with default value false
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN NOT NULL DEFAULT FALSE;

-- Create index for faster admin lookups
CREATE INDEX IF NOT EXISTS idx_users_is_admin ON users(is_admin);

-- Optional: Create a default admin user (change email and password as needed)
-- Note: The password hash below is for 'admin123' - CHANGE THIS IN PRODUCTION!
-- To generate a new hash, use: python -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('your_password'))"

-- Uncomment to create admin user:
-- INSERT INTO users (email, hashed_password, first_name, last_name, tier, is_active, is_admin, created_at, updated_at)
-- VALUES ('admin@ajla.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiLXCJc.z.Vy', 'Admin', 'User', 100000, true, true, NOW(), NOW())
-- ON CONFLICT (email) DO UPDATE SET is_admin = true;
