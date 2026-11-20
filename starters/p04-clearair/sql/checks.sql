-- ClearAir's checks on the readings table. Run them from clearair/:
--   docker exec -i datalab-postgres-1 psql -U de -d clearair < sql/checks.sql

-- TODO(task 13): 1. the number of rows, and the number of distinct (sensor_id, period_end) keys.

-- TODO(task 13): 2. the keys found more than once (HAVING COUNT(*) > 1). It must return 0 rows.

-- TODO(task 13): 3. each sensor's newest period_end, beside its watermark in load_state.
