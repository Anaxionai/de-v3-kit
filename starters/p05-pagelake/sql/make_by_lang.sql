-- A second silver layout for the measurement: the same rows, partitioned by language.
-- Run from pagelake/: uv run --env-file .env python -m pagelake.query sql/make_by_lang.sql
-- <bucket> becomes your bucket's name. Delete silver/pageviews_by_lang/ again at the end of task 9.

-- TODO(task 9): COPY every row FROM {silver} to 's3://<bucket>/silver/pageviews_by_lang' as Parquet, partitioned by lang.
--   Step 10 of the brief gives the statement.
