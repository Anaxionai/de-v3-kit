-- q1: the 10 most-viewed titles on 2026-11-05, over every language.
-- Run from pagelake/: uv run --env-file .env python -m pagelake.query sql/q1_one_day.sql [--layout <layout>] [--explain]
-- {silver} becomes read_parquet(...) over the layout you choose.

-- TODO(task 9): SELECT the top 10 titles and their views FROM {silver} for the day 2026-11-05.
