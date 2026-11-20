"""PageLake's Iceberg table lake.pageviews: the silver layer with snapshots.

    uv run --env-file .env python -m pagelake.iceberg_table create
    uv run --env-file .env python -m pagelake.iceberg_table append 2026-11-02 --days 7
    uv run --env-file .env python -m pagelake.iceberg_table snapshots
    uv run --env-file .env python -m pagelake.iceberg_table add-column
    uv run --env-file .env python -m pagelake.iceberg_table time-travel
    uv run --env-file .env python -m pagelake.iceberg_table count-day 2026-11-04
    uv run --env-file .env python -m pagelake.iceberg_table replace-day 2026-11-04

Task 11 starts with `uv add "pyiceberg[pyarrow,sql-sqlite]"`. Until then this file
imports nothing from PyIceberg. You will need:
    from pyiceberg.catalog import load_catalog
    from pyiceberg.expressions import EqualTo
    from pyiceberg.types import TimestampType

The command line is set-up and is complete; the functions are yours.
"""

import argparse
from datetime import date, timedelta

TABLE = "lake.pageviews"


def get_catalog():
    """The PyIceberg SQL catalogue of PageLake:
    load_catalog("pagelake", type="sql", uri=..., warehouse=f"s3://{bucket}/iceberg", **s3)

    - uri: a SQLite file in your home folder, so every task folder finds the same
      table: "sqlite:///" + (Path.home() / f"{bucket}-catalog.db").as_posix()
    - s3: "s3.endpoint", "s3.access-key-id", "s3.secret-access-key" and
      "s3.region", from the same settings as lake.py.
    """
    raise NotImplementedError("TODO(task 11): write get_catalog()")


def day_arrow(day: date):
    """One day of silver as a PyArrow table: read it with lake.connect() and
    return .to_arrow_table()."""
    raise NotImplementedError("TODO(task 11): write day_arrow()")


def create_table():
    """Create the namespace lake if it is missing, then the table lake.pageviews
    with the schema of one day's Arrow table, partitioned by day
    (update_spec() with add_identity("day")). Return the table."""
    raise NotImplementedError("TODO(task 11): write create_table()")


def append_day(day: date) -> None:
    """Append one day of silver to lake.pageviews: table.append(day_arrow(day)).
    Each call makes one snapshot."""
    raise NotImplementedError("TODO(task 11): write append_day()")


def snapshots() -> None:
    """Print table.inspect.snapshots(): each snapshot's id, time and operation."""
    raise NotImplementedError("TODO(task 11): write the snapshots command")


def add_column() -> None:
    """Add the column loaded_at (TimestampType()) with update_schema(), and print
    the number of data files (len(table.inspect.files())) before and after, and
    the new schema."""
    raise NotImplementedError("TODO(task 11): write the add-column command")


def time_travel() -> None:
    """Print the row count at the first snapshot,
    table.scan(snapshot_id=<its id>).count(), and now, table.scan().count()."""
    raise NotImplementedError("TODO(task 11): write the time-travel command")


def count_day(day: date) -> int:
    """The rows of one day in the table: table.scan(row_filter="day = '<day>'").count()."""
    raise NotImplementedError("TODO(task 13): write count_day()")


def replace_day(day: date) -> None:
    """Replace one day of the table in one commit.

    Read the day with `localtimestamp AS loaded_at` added, then call
    table.overwrite(arrow, overwrite_filter=EqualTo("day", <the day>)). Each
    call makes a delete and an append snapshot; running it twice changes no row.
    """
    raise NotImplementedError("TODO(task 13): write replace_day()")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python -m pagelake.iceberg_table", description="The Iceberg table."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("create", help="create lake.pageviews (task 11)")
    append = commands.add_parser("append", help="append days of silver (task 11)")
    append.add_argument("start", type=date.fromisoformat)
    append.add_argument("--days", type=int, default=1)
    commands.add_parser("snapshots", help="list the snapshots (task 11)")
    commands.add_parser("add-column", help="add loaded_at (task 11)")
    commands.add_parser("time-travel", help="row counts then and now (task 11)")
    count = commands.add_parser("count-day", help="rows of one day (task 13)")
    count.add_argument("day", type=date.fromisoformat)
    replace = commands.add_parser("replace-day", help="replace one day (task 13)")
    replace.add_argument("day", type=date.fromisoformat)
    args = parser.parse_args(argv)

    if args.command == "create":
        create_table()
        print(f"created {TABLE}")
    elif args.command == "append":
        for number in range(args.days):
            day = args.start + timedelta(days=number)
            append_day(day)
            print(f"appended {day}")
    elif args.command == "snapshots":
        snapshots()
    elif args.command == "add-column":
        add_column()
    elif args.command == "time-travel":
        time_travel()
    elif args.command == "count-day":
        print(count_day(args.day))
    elif args.command == "replace-day":
        replace_day(args.day)
        print(f"replaced {args.day}")


if __name__ == "__main__":
    main()
