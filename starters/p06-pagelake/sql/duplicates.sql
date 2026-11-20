-- Repeated rows: rows of silver that share day, lang, mobile, title and hour. Good output has no rows.
-- Run from pagelake/: uv run --env-file .env python -m pagelake.query sql/duplicates.sql

-- TODO(task 11): FROM {silver}, the day, lang, mobile, title and hour that appear more than once, with how often.
