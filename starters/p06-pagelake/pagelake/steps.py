"""PageLake's daily work as plain Python functions, one named day at a time (task 9).

Every function takes the day (or the day's path) as an argument. None of them
picks the day from the clock. The DAG in dags/pagelake_daily.py calls them, and
tests/test_steps.py tests them without Airflow.

Run one whole day on your laptop, from the pagelake/ folder (task 9, step 11):

    uv run --env-file .env python -m pagelake.steps 2026-11-05

LANGS, MissingHour, data_dir() and the command line are set-up and complete;
the four functions in between are yours. Reuse P5: silver.hour_files(),
land.bronze_key() (through hour_files), lake.s3_client(), silver.load_day()
and gold.build_gold().
"""

import argparse
import os
from datetime import date
from pathlib import Path

from pagelake import gold, lake, silver

# The six Wikipedias of the course week. Task 10 makes one check task per language.
LANGS = ["simple", "id", "ko", "nl", "sv", "vi"]


class MissingHour(Exception):
    """A day cannot be landed: at least one of its 24 hourly files is missing."""


def data_dir() -> Path:
    """The data folder, from PAGELAKE_DATA_DIR (default "data").

    data/raw/ is the drop folder, where the source leaves its files. A relative
    value starts from the working folder: pagelake/ on your laptop, and the same
    folder inside Airflow (the kit's compose.yaml sets it).
    """
    return Path(os.environ.get("PAGELAKE_DATA_DIR", "data"))


def missing_hours(day: date, raw_dir: Path) -> list[str]:
    """The names of the day's 24 hourly files that are not in raw_dir, in hour order.

    Build the names from P5's silver.hour_files(day): each bronze key ends with
    the file's name. Remember the end-of-hour rule: 6 November needs
    pageviews-20261107-000000.gz. An empty list means the day is complete.
    """
    raise NotImplementedError("TODO(task 9): write missing_hours()")


def land_day(day: date, raw_dir: Path, bucket: str) -> int:
    """Upload the day's 24 hourly files to their bronze keys and return 24.

    - First check the whole day. If any file is missing, raise MissingHour with
      a message that names the day and every missing file, before anything is
      uploaded.
    - Then upload_file each of the 24 files to its bronze_key() key with
      lake.s3_client(). Uploading a file again writes the same object.
    """
    raise NotImplementedError("TODO(task 9): write land_day()")


def silver_path(bucket: str, day: date | str) -> str:
    """The files P5's load_day() writes for one day:
    s3://<bucket>/silver/pageviews/day=<YYYY-MM-DD>/*.parquet

    day may be a date or its "YYYY-MM-DD" text (the DAG passes ds): both print
    the same way in an f-string.
    """
    raise NotImplementedError("TODO(task 9): write silver_path()")


def check_language(con, path: str, lang: str) -> dict:
    """Check one language of one day of silver and return
    {"lang": lang, "rows": <rows>, "views": <total views>}.

    - Count the rows, sum the views and count the distinct (mobile, title, hour)
      of read_parquet(path) for one lang, in one query with two parameters:
      con.execute(sql, [path, lang]).fetchall().
    - Raise ValueError when the language has no rows, or when two rows share
      mobile, title and hour (a repeated row). Name the language in the message.
    con is a DuckDB connection: lake.connect() for the bucket, or duckdb.connect()
    for a local file in the tests.
    """
    raise NotImplementedError("TODO(task 9): write check_language()")


def main(argv: list[str] | None = None) -> None:
    """Run one whole day by hand: land it, rebuild its silver partition, check
    the six languages and rebuild gold, printing each result."""
    parser = argparse.ArgumentParser(
        prog="python -m pagelake.steps", description="Run one day by hand."
    )
    parser.add_argument(
        "day", type=date.fromisoformat, help="a UTC day, such as 2026-11-05"
    )
    day = parser.parse_args(argv).day
    bucket = lake.bucket()
    print(f"landed: {land_day(day, data_dir() / 'raw', bucket)} files")
    print(f"silver: {silver.load_day(day)} rows")
    path = silver_path(bucket, day)
    con = lake.connect()
    for lang in LANGS:
        print(check_language(con, path, lang))
    print(f"gold: {gold.build_gold()}")


if __name__ == "__main__":
    main()
