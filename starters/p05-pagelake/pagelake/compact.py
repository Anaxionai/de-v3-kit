"""Compaction: one day's 24 small silver files rewritten as one sorted file.

    uv run --env-file .env python -m pagelake.compact 2026-11-05

The command line is set-up and is complete; compact_day() is yours.
"""

import argparse
from datetime import date


def compact_day(day: date) -> tuple[int, int]:
    """Rewrite one day's hour-*.parquet files as one file, and return (rows, views).

    1. Count the rows and sum the views of silver/pageviews/day=<day>/hour-*.parquet.
    2. COPY the same five columns (lang, mobile, title, views, hour; the folder
       gives the day) ORDER BY lang, title to day=<day>/compact-0.parquet. Add
       mobile and hour at the end of the ORDER BY to break ties: then a second
       run writes the same file, byte for byte (task 13 compares the listings).
    3. Task 12 step 4: wait with input("Press Enter to delete the hourly files"),
       and remove that line again in step 9.
    4. Compare the new file's rows and views with step 1. When they match, delete
       the 24 hour-* objects with one delete_objects call. When they do not,
       delete the new file and raise an error.
    """
    raise NotImplementedError("TODO(task 12): write compact_day()")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python -m pagelake.compact", description="Compact one day of silver."
    )
    parser.add_argument(
        "day", type=date.fromisoformat, help="a UTC day, such as 2026-11-05"
    )
    args = parser.parse_args(argv)
    rows, views = compact_day(args.day)
    print(f"{args.day}: {rows} rows, {views} views in compact-0.parquet")


if __name__ == "__main__":
    main()
