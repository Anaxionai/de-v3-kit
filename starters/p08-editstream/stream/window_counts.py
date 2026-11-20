"""Count Wikipedia edits per language in one-minute event-time windows (tasks 11 to 13).

Runs in the Spark container, from the editstream/ folder:

    docker compose exec spark spark-submit stream/window_counts.py
    docker compose exec spark spark-submit stream/window_counts.py --output-mode append
    docker compose exec spark spark-submit stream/window_counts.py --topic wiki-edits-test --replay
    docker compose exec spark spark-submit stream/window_counts.py --sink delta
"""

from pyspark.sql import DataFrame

from stream.parse import parse_events, read_topic  # noqa: F401  (main() uses them)

QUERY_NAME = "counts"                          # the memory sink's table in --replay
DELTA_PATH = "data/delta/edit_counts"          # relative to editstream/
CHECKPOINT = "data/checkpoints/edit_counts"    # relative to editstream/


def count_per_language(edits: DataFrame, delay: str = "2 minutes") -> DataFrame:
    """Count edits per one-minute window of event_time and per language.

    `edits` has at least event_id, event_time and language. Set a watermark of
    `delay` on event_time before you group. Return the columns window_start,
    window_end, language and edits (the count).
    """
    # TODO(task 12): after the watermark, drop repeated events by event_id within
    # it, so an edit sent twice is counted once.
    raise NotImplementedError("TODO(task 11): watermark, window and count")


def parse_args(argv: list[str] | None = None):
    """Read the command line with argparse.

    --topic (default wiki-edits) and --output-mode (default update) in task 11,
    --replay in task 12, --sink (console, the default, or delta) in task 13.
    """
    raise NotImplementedError("TODO(task 11): add --topic and --output-mode")


def main(argv: list[str] | None = None) -> None:
    """Run the counts as a streaming query.

    - Session settings: spark.sql.shuffle.partitions 4 and spark.sql.session.timeZone UTC.
    - Console sink: the chosen output mode, truncate False, numRows 50 and a
      30-second processing-time trigger, then awaitTermination().
    """
    # TODO(task 12): --replay reads the topic with replay=True and writes to the
    # memory sink named QUERY_NAME in append mode with trigger(availableNow=True).
    # When it ends, print the edits per window_start and the total of edits.
    # TODO(task 13): --sink delta writes in append mode to DELTA_PATH with the
    # checkpoint location CHECKPOINT and the same 30-second trigger.
    raise NotImplementedError("TODO(task 11): run the counts to the console")


if __name__ == "__main__":
    main()
