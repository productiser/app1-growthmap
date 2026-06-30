-- Rename prospect market columns after switching from inferred market to explicit user selection.
-- Run this against existing local databases that already applied Design/DDL.sql before 2026-06-30.

ALTER TABLE prospects
    RENAME COLUMN assumed_country TO country_code;

ALTER TABLE prospects
    RENAME COLUMN assumed_language TO language_code;

ALTER TABLE prospects
    DROP COLUMN market_inference_note;

ALTER TABLE prospects
    ALTER COLUMN country_code SET NOT NULL,
    ALTER COLUMN language_code SET NOT NULL;
