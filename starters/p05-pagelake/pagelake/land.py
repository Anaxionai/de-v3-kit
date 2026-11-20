"""Land the raw hourly files in the bronze layer, unchanged.

    uv run --env-file .env python -m pagelake.land data/raw

The command line is set-up and is complete; the two functions are yours.
"""

import argparse
from pathlib import Path

from pagelake import lake


def bronze_key(name: str) -> str:
    """The bronze key of one dump file, keeping the file's name.

    pageviews-20261102-010000.gz -> bronze/pageviews/2026/2026-11/pageviews-20261102-010000.gz

    The year and the month come from the date in the name. tests/test_land.py
    checks it, with the week's last file pageviews-20261109-000000.gz too.
    """
    raise NotImplementedError("TODO(task 8): write bronze_key()")


def land(raw_dir: Path, bucket: str) -> int:
    """Upload every .gz file of raw_dir that is not in bronze yet, and return
    how many were uploaded.

    - First list the keys under bronze/pageviews/ with the list_objects_v2
      paginator of lake.s3_client(): one answer holds at most 1,000 keys.
    - Then upload_file only the files whose bronze_key() is missing.
    A second run on the same folder uploads 0.
    """
    raise NotImplementedError("TODO(task 8): write land()")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python -m pagelake.land", description="Land raw files in bronze."
    )
    parser.add_argument(
        "raw_dir", help="the folder of downloaded .gz files, such as data/raw"
    )
    args = parser.parse_args(argv)
    uploaded = land(Path(args.raw_dir), lake.bucket())
    print(f"uploaded {uploaded} files")


if __name__ == "__main__":
    main()
