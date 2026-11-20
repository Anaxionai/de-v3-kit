-- ClearAir's tables in the clearair database.
-- load.ensure_schema() runs this file on every run, so every statement uses IF NOT EXISTS.

-- TODO(task 10): readings, one row per sensor and hour: sensor_id, period_end (TIMESTAMPTZ),
--   location_id, parameter, units, value, loaded_at, and PRIMARY KEY (sensor_id, period_end).

-- TODO(task 11): load_state, one watermark per load: name (TEXT, the primary key, such as
--   'sensor:<sensor-id>' or 'stations'), watermark (TIMESTAMPTZ) and updated_at.

-- TODO(task 21): stations: the nine source columns the kit's data/airquality/README.md lists
--   (station_id is the primary key), plus loaded_at and deleted_at (NULL while current).
