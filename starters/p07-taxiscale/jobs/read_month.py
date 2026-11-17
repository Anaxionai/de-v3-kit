"""TaxiScale's first job: read one month of trips and check it.

Run it in the Spark container, from taxiscale/:
    docker compose exec spark spark-submit jobs/read_month.py

The code runs inside the kit's Spark image (Python 3.10), not on your laptop's Python.
"""


def main() -> None:
    """Read data/yellow/yellow_tripdata_2024-01.parquet and print what is in it.

    - Build a SparkSession (SparkSession.builder.appName(...).getOrCreate()).
    - Read the file with spark.read.parquet() and call printSchema().
    - Print count(). The January 2024 file has 2,964,624 rows.
    - Print the earliest and the latest tpep_pickup_datetime with
      agg(F.min(...), F.max(...)). TLC files hold some trips from outside their month.
    - Stop the session at the end.
    """
    raise NotImplementedError("TODO(task 8): write main()")


if __name__ == "__main__":
    main()
