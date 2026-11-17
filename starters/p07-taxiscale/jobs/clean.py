"""The cleaning stage: impossible trips out, clear column names in.

Run it in the Spark container, from taxiscale/:
    docker compose exec spark spark-submit jobs/clean.py --month 2024-01

tests/test_clean.py tests clean_trips() on small hand-made DataFrames. The code runs
inside the kit's Spark image (Python 3.10), not on your laptop's Python.
"""


def clean_trips(df, months):
    """Return the clean trips of a DataFrame of TLC yellow-taxi rows.

    months is a list of 'yyyy-MM' texts, such as ["2024-01"].

    Renames:  tpep_pickup_datetime -> pickup_at, tpep_dropoff_datetime -> dropoff_at,
              PULocationID -> pu_zone_id, DOLocationID -> do_zone_id,
              trip_distance -> trip_miles.
    Kept as they are: passenger_count, payment_type, fare_amount, total_amount.
    New columns (withColumn):
        pickup_date   the pickup's date
        pickup_month  the pickup's month as text, such as '2024-01'
        duration_min  minutes from pickup to drop-off
    Rows kept: pickup_month in months; duration_min above 0 and under 360;
               trip_miles above 0 and under 100; fare_amount 0 or more.

    The result has these columns, in this order: pickup_at, dropoff_at, pickup_date,
    pickup_month, duration_min, pu_zone_id, do_zone_id, trip_miles,
    passenger_count, payment_type, fare_amount, total_amount.
    """
    raise NotImplementedError("TODO(task 9): write clean_trips()")


def main() -> None:
    """The clean job, with the option --month yyyy-MM.

    Read data/yellow/yellow_tripdata_<month>.parquet, print the rows in and the
    rows out, and write the clean trips to data/out/clean/ as Parquet with
    mode("overwrite").
    """
    raise NotImplementedError("TODO(task 9): write main()")


if __name__ == "__main__":
    main()
