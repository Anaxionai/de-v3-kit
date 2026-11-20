-- Scorebook indexes. Task 22.
-- Run it after the load with: bash psql.sh < sql/indexes.sql
-- sql/schema.sql drops the tables and their indexes: after a reset, load again, then run this file.

-- TODO(task 22): the index deliveries_batter_idx on deliveries (batter_id), so that it can
-- run twice (IF NOT EXISTS), then ANALYZE deliveries.
