-- The daily zone table in Spark SQL. join_aggregate.py registers the clean trips as the temporary view
-- trips and the zone lookup as zones, runs this file with spark.sql(), and compares its rows with the
-- DataFrame version. Keywords in upper case.

-- TODO(task 10): the same left join and grouping as join_zones() and daily_zone_totals():
--   pickup_date, pu_zone_id, borough, zone, trips, total_fare and avg_miles, FROM trips LEFT JOIN zones.
