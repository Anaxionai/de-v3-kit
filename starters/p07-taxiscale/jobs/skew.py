"""Find the skewed key: which pickup zones hold the most trips, and how uneven
the partitions are when the trips are split by zone.

Run it in the Spark container, from taxiscale/:
    docker compose exec spark spark-submit jobs/skew.py

It reads the clean trips from data/out/clean/. The code runs inside the kit's Spark
image (Python 3.10), not on your laptop's Python.
"""


def top_keys(df, key, n):
    """The n most common values of the column key, with their row count and
    their share of all rows, most common first."""
    raise NotImplementedError("TODO(task 13): write top_keys()")


def partition_sizes(df, cols, parts):
    """Split df with repartition(parts, *cols), count the rows of each
    partition with F.spark_partition_id(), and print the largest, the median
    and the largest divided by the median."""
    raise NotImplementedError("TODO(task 13): write partition_sizes()")


def main() -> None:
    """Print the top 5 pickup zones, the partition sizes for pu_zone_id, and
    (after salting) the partition sizes for pu_zone_id and salt together."""
    raise NotImplementedError("TODO(task 13): write main()")


if __name__ == "__main__":
    main()
