-- Add title column to requests table
-- Migration: 002_add_title_to_requests.sql
-- Date: 2025-12-23

ALTER TABLE requests ADD COLUMN IF NOT EXISTS title VARCHAR(255);

-- Set a default value for existing records (optional)
UPDATE requests SET title = 'Request #' || id WHERE title IS NULL;

-- Make title NOT NULL after setting defaults (optional - remove if you want nullable)
-- ALTER TABLE requests ALTER COLUMN title SET NOT NULL;
