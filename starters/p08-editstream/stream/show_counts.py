"""Show what the Delta sink wrote: rows, repeated windows and the table history (task 13).

Runs in the Spark container, from the editstream/ folder:

    docker compose exec spark spark-submit stream/show_counts.py
"""

from stream.window_counts import DELTA_PATH  # noqa: F401  (main() reads it)


def main() -> None:
    """Read DELTA_PATH with spark.read.format("delta") and print three things.

    - The number of rows.
    - How many (window_start, language) pairs appear more than once (expect 0).
    - DESCRIBE HISTORY of the table, with version, operation and
      operationParameters. Use the absolute path: os.path.abspath(DELTA_PATH).
    """
    raise NotImplementedError("TODO(task 13): print rows, repeated pairs and history")


if __name__ == "__main__":
    main()
