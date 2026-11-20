"""PageLake's freshness check: is the newest complete day within the promise? (task 14)

Run it from the pagelake/ folder, with the S3 emulator running:

    uv run --env-file .env python -m pagelake.freshness --today 2026-11-09
    uv run --env-file .env python -m pagelake.freshness

The command line's --today option is set-up and complete; status() and the
rest of main() are yours.
"""

import argparse
from datetime import date

PROMISE_DAYS = 1  # the newest complete day is at most this many days old


def status(newest_day: date | None, today: date, max_days: int = PROMISE_DAYS) -> str:
    """Return "FRESH" or "LATE".

    - "FRESH" when newest_day is at most max_days days before today.
    - "LATE" when it is older, and when newest_day is None (no complete day).
    """
    raise NotImplementedError("TODO(task 14): compare the newest day with the promise")


def main(argv: list[str] | None = None) -> int:
    """Run sql/freshness.sql, print the result and return the exit code."""
    parser = argparse.ArgumentParser(
        prog="python -m pagelake.freshness", description="Check PageLake's freshness."
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=None,
        help="the day to check against, such as 2026-11-09 (default: the real date)",
    )
    args = parser.parse_args(argv)
    # TODO(task 14): the rest of main().
    # - today: args.today if given, else the real date (date's today method).
    # - Read sql/freshness.sql, fill {silver} as query.py does (query.fill), and
    #   run it on lake.connect(): it gives the newest day with all 24 hours.
    # - Work out its age from today, and the status from status().
    # - Print "<status>: newest complete day <day>, <n> days old (promise: 1)".
    # - Return 0 when FRESH and 1 when LATE.
    raise NotImplementedError(f"TODO(task 14): check freshness (--today {args.today})")


if __name__ == "__main__":
    raise SystemExit(main())
