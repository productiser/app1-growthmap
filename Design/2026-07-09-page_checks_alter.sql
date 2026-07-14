 ALTER TABLE page_checks
  DROP COLUMN IF EXISTS indexable,
  DROP COLUMN IF EXISTS noindex,
  DROP COLUMN IF EXISTS obvious_broken_page,
  ADD COLUMN IF NOT EXISTS description_to_content_consistency NUMERIC(8, 4);
