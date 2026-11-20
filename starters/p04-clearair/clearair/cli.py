"""ClearAir's command line. Run it from the clearair/ folder:

    uv run --env-file .env python -m clearair.cli load-api
    uv run --env-file .env python -m clearair.cli load-api --until 2026-11-12T06:00:00Z
    uv run --env-file .env python -m clearair.cli load-api --raw data/raw/20261112T0800Z
    uv run --env-file .env python -m clearair.cli load-stations [--full]

The command-line parsing below is set-up and is complete. The two commands are
yours to write.
"""

import argparse
import logging


def load_api(args: argparse.Namespace) -> None:
    """The load-api command: OpenAQ readings into the readings table.

    What each task adds:
    - task 8: load the settings; take the run start (UTC, rounded down to the
      hour) and its run id; find_sensors(); for each sensor, one /hours page with
      datetime_from 7 days before the run start and datetime_to the run start
      (UTC, ending in Z), saved under data/raw/<run-id>/. Log each call and
      each file saved.
    - task 9: every page with fetch_pages(), the window end fixed once per run,
      and summarise_pages() logged for each sensor.
    - task 10: ensure_schema(), then each sensor's rows upserted in one
      transaction. With --raw, load a saved run folder without calling the API.
    - task 11: datetime_from from window_start() and the sensor's watermark,
      the window end from --until, and the new watermark written in the same
      transaction as the rows.
    - task 12: every get_json() call wrapped in call_with_retries().

    Open the database with psycopg.connect(DATABASE_URL, autocommit=True). Then
    each `with conn.transaction():` block commits when it ends. Without
    autocommit, psycopg keeps one transaction open for the whole run, and a run
    that fails halfway (task 12) rolls back the sensors it had finished too.
    """
    # TODO(task 9): read every page with fetch_pages() and log summarise_pages() for each sensor.
    # TODO(task 10): ensure_schema(), one transaction per sensor with upsert_readings(), and --raw.
    # TODO(task 11): the window from the watermark and --until; write the watermark with the rows.
    # TODO(task 12): wrap every get_json() call in call_with_retries().
    raise NotImplementedError("TODO(task 8): write the load-api command")


def load_stations(args: argparse.Namespace) -> None:
    """The load-stations command: the station database into the stations table.

    - task 21: open the source (STATIONDB_URL) and the target (DATABASE_URL),
      both with autocommit=True as in load_api, and run ensure_schema() on the
      target. --full runs full_load(); without it,
      incremental_load() runs, or full_load() when there is no "stations"
      watermark yet. Log the rows read.
    - task 22: then call mark_deleted() and log the ids it marked.
    """
    # TODO(task 22): call mark_deleted() at the end and log the ids it marked.
    raise NotImplementedError("TODO(task 21): write the load-stations command")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clearair",
        description="ClearAir: air-quality readings and stations, loaded into PostgreSQL.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    api = commands.add_parser(
        "load-api", help="load hourly readings from the OpenAQ API"
    )
    api.add_argument(
        "--until",
        help="end of the window, a UTC time such as 2026-11-12T06:00:00Z (task 11); "
        "without it, the run start rounded down to the hour",
    )
    api.add_argument(
        "--raw",
        help="load the saved pages of a run folder such as data/raw/20261112T0800Z, "
        "without calling the API (task 10)",
    )
    api.set_defaults(func=load_api)

    stations = commands.add_parser(
        "load-stations", help="load the stations table from the station database"
    )
    stations.add_argument(
        "--full",
        action="store_true",
        help="read every row, not only the changed ones (task 21)",
    )
    stations.set_defaults(func=load_stations)
    return parser


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
