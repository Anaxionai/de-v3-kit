"""Turn raw Kafka messages into clean rows of Wikipedia edits (task 10).

Runs in the Spark container, from the editstream/ folder:

    docker compose exec spark spark-submit stream/parse.py
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F  # noqa: F401  (your code uses F.from_json and more)

BOOTSTRAP = "kafka:19092"  # Kafka from inside the Spark container, not localhost:9092

# TODO(task 10): the schema of one event, as a StructType: meta (a struct with the
# strings id and domain), the strings type, title and user, the boolean bot, and
# timestamp as a long (Unix seconds, the time of the edit). Compare it with the
# example event in the kit's data/edits/README.md.
EVENT_SCHEMA = None


def parse_events(raw: DataFrame) -> DataFrame:
    """Parse Kafka rows into one row per Wikipedia edit.

    `raw` has Kafka's `value` column (bytes). Return the columns event_id
    (meta.id), event_time (a timestamp made from `timestamp`), domain, title,
    user, bot and language (the domain up to its first dot, such as "en").

    Keep only rows whose type is "edit", whose domain ends with
    ".wikipedia.org" and whose event_id is not null. Broken JSON parses to
    nulls, so it is dropped too.
    """
    raise NotImplementedError("TODO(task 10): parse the JSON and keep only Wikipedia edits")


def read_topic(spark: SparkSession, topic: str, replay: bool = False) -> DataFrame:
    """Return the topic as a streaming DataFrame, read from the earliest offset.

    Use spark.readStream.format("kafka") with kafka.bootstrap.servers BOOTSTRAP.
    """
    # TODO(task 12): when replay is true, also set maxOffsetsPerTrigger to 25, so
    # Spark reads the topic in small batches, as if it arrived live.
    raise NotImplementedError("TODO(task 10): read the topic as a stream")


def main() -> None:
    """Print parsed edits from wiki-edits to the console until Ctrl+C.

    Build a SparkSession with spark.sql.shuffle.partitions 4, write
    parse_events(read_topic(spark, "wiki-edits")) to the console sink, and call
    awaitTermination().
    """
    raise NotImplementedError("TODO(task 10): run the parsed stream to the console")


if __name__ == "__main__":
    main()
