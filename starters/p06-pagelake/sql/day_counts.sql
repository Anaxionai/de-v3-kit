-- Day counts: one row per day of silver, to prove a re-run changes nothing.
-- Columns: day, rows, views, hours. A complete day has 24 hours.
-- Run from pagelake/: uv run --env-file .env python -m pagelake.query sql/day_counts.sql

-- TODO(task 11): FROM {silver}, per day: the rows, sum(views) and count(DISTINCT hour) AS hours, in day order.
