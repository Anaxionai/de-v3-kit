-- bytes_report
-- Today's query jobs in your project, oldest first: when each ran, how its SQL starts,
-- the bytes it read, the bytes it was billed and whether it reused a cached result.
-- "Today" starts at midnight UTC.
-- Run it from the task folder: bq query < gitpulse/bigquery/sql/bytes_report.sql
-- The Guided starter gives this file complete, because it is a tool for checking your
-- budget, not one of the five questions. Read it before you run it (task 8, step 4),
-- and make sure you can say what each column means.
SELECT
  creation_time,
  SUBSTR(query, 1, 40) AS query_start,
  total_bytes_processed,
  total_bytes_billed,
  cache_hit
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_USER
WHERE job_type = 'QUERY'
  AND creation_time >= TIMESTAMP(CURRENT_DATE())
ORDER BY creation_time;
