"""The silver layer: typed Parquet, one file per hour, in one folder per day.

    uv run --env-file .env python -m pagelake.silver 2026-11-02 --days 7
    uv run --env-file .env python -m pagelake.silver load-day 2026-11-04

Layout: silver/pageviews/day=<YYYY-MM-DD>/hour-<HH>.parquet with the columns
lang, mobile, title, views and hour. The day comes from the folder name, so the
files do not hold it.

The command line is set-up and is complete; the functions are yours.
"""

import argparse
import sys
from datetime import date, timedelta

from pagelake import lake


def hour_files(day: date) -> list[str]:
    """The bronze keys of the 24 files that hold one UTC day, in hour order.

    A file is named after the END of its hour: 00:00 to 01:00 on 2 November is
    pageviews-20261102-010000.gz, and 23:00 to 24:00 is the next day's
    pageviews-20261103-000000.gz. Build each key with land.bronze_key().
    """
    raise NotImplementedError("TODO(task 9): write hour_files()")


def write_hour(con, bucket: str, day: date, hour: int) -> int:
    """Write the silver file of one hour and return its row count.

    - Read hour_files(day)[hour] from bronze with read_csv(..., delim = ' ',
      header = false, quote = '', escape = '') and name the four columns.
    - Keep lang (the code before the first dot), mobile (true when the code ends
      in .m), title, views and hour (0 to 23, the hour the row covers).
    - COPY the result to silver/pageviews/day=<YYYY-MM-DD>/hour-<HH>.parquet
      (FORMAT parquet).
    con is a connection from lake.connect().
    """
    raise NotImplementedError("TODO(task 9): write write_hour()")


def load_day(day: date) -> int:
    """Load one day so that running it twice changes nothing, and return its rows.

    - Delete every object under silver/pageviews/day=<YYYY-MM-DD>/: list them
      with the paginator, remove them with delete_objects (at most 1,000 keys
      per call). The prefix ends with the slash.
    - Then write its 24 hours with write_hour() and compact them with
      compact.compact_day().
    """
    raise NotImplementedError("TODO(task 13): write load_day()")


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "load-day":
        parser = argparse.ArgumentParser(prog="python -m pagelake.silver load-day")
        parser.add_argument(
            "day", type=date.fromisoformat, help="a UTC day, such as 2026-11-04"
        )
        args = parser.parse_args(argv[1:])
        print(f"{args.day}: {load_day(args.day)} rows")
        return

    parser = argparse.ArgumentParser(
        prog="python -m pagelake.silver", description="Write silver from bronze."
    )
    parser.add_argument(
        "start", type=date.fromisoformat, help="the first UTC day, such as 2026-11-02"
    )
    parser.add_argument("--days", type=int, default=1, help="how many days (default 1)")
    args = parser.parse_args(argv)
    con = lake.connect()
    bucket = lake.bucket()
    for number in range(args.days):
        day = args.start + timedelta(days=number)
        for hour in range(24):
            rows = write_hour(con, bucket, day, hour)
            print(f"{day} hour {hour:02d}: {rows} rows")


if __name__ == "__main__":
    main()
