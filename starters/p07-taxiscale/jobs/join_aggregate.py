"""TaxiScale's main table: trips, fares and distance per pickup zone per day.

Run it in the Spark container, from taxiscale/ (a --conf goes BEFORE the script name):
    docker compose exec spark spark-submit jobs/join_aggregate.py
    docker compose exec spark spark-submit --conf spark.sql.autoBroadcastJoinThreshold=-1 jobs/join_aggregate.py --join sortmerge

It reads the clean trips of task 9 from data/out/clean/ and the zone lookup from
data/zones/taxi_zone_lookup.csv, and writes data/out/daily_zone/. The code runs inside
the kit's Spark image (Python 3.10), not on your laptop's Python.
"""


def read_zones(spark, path):
    """Read the zone lookup CSV (LocationID, Borough, Zone, service_zone) with
    header=True and inferSchema=True. 265 rows."""
    raise NotImplementedError("TODO(task 10): write read_zones()")


def join_zones(trips, zones):
    """Left-join the clean trips to the zones on pu_zone_id = LocationID, adding
    borough and zone. A left join keeps trips whose zone is unknown.

    Task 12 adds a way to choose the join: wrap the zones in F.broadcast() for
    --join broadcast, and leave them as they are for --join sortmerge.
    """
    # TODO(task 12): choose the join: F.broadcast(zones) only for --join broadcast.
    raise NotImplementedError("TODO(task 10): write join_zones()")


def daily_zone_totals(df):
    """Group by pickup_date, pu_zone_id, borough and zone, with
    trips (a count), total_fare (the sum of fare_amount) and avg_miles."""
    raise NotImplementedError("TODO(task 10): write daily_zone_totals()")


def salted_join(trips, zones, salts=8):
    """The join with a salt, for a skewed pickup zone (task 13).

    - Add salt to the trips: (F.rand(42) * salts).cast("int").
    - Copy each zone once per salt value:
      zones.crossJoin(spark.range(salts).withColumnRenamed("id", "salt")),
      where spark is trips.sparkSession.
    - Join on the zone id and salt, then drop salt.
    The row count and the sum of trips must equal the broadcast join's.
    """
    raise NotImplementedError("TODO(task 13): write salted_join()")


def main() -> None:
    """The daily-zone job.

    - task 10: read data/out/clean/ and the zones; build the table with
      daily_zone_totals(join_zones(...)) and with sql/daily_zone.sql over the
      temporary views trips and zones; print "same rows: True" when
      assertDataFrameEqual (with its tolerance for doubles) finds the two
      tables equal; write the DataFrame result to
      data/out/daily_zone/ as Parquet; print its row count, the 5 busiest
      zone-days, the seconds taken, the sum of trips and the clean row count.
      exceptAll compares total_fare and avg_miles (doubles) exactly, so it says
      True only while both versions add the numbers in the same order. When a
      later --conf or --join gives them different plans, the last digits differ
      and it says False with the same table; assertDataFrameEqual (task 9's
      card) compares doubles within a small tolerance.
    - task 11: print the result's plan with explain("formatted") before the write.
    - task 12: an option --join with the values sortmerge and broadcast.
    - task 13: a third value, salted, that uses salted_join().
    """
    # TODO(task 11): call explain("formatted") on the result before you write it.
    # TODO(task 12): add the option --join sortmerge|broadcast and pass it to join_zones().
    # TODO(task 13): add --join salted, which uses salted_join().
    raise NotImplementedError("TODO(task 10): write main()")


if __name__ == "__main__":
    main()
