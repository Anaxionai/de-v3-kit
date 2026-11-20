"""Load raw /hours pages into the readings table of the clearair database.

Each function takes an open psycopg connection (`conn`) from its caller, so the
pure function rows_from_page() can be tested without a database.
"""


def ensure_schema(conn) -> None:
    """Run sql/schema.sql on conn.

    Every statement in that file uses IF NOT EXISTS, so this is safe on every run.
    Find the file next to the package, as
    Path(__file__).parent.parent / "sql" / "schema.sql", so that it is found from
    any folder and inside the Docker image (task 23).
    """
    raise NotImplementedError("TODO(task 10): write ensure_schema()")


def rows_from_page(page: dict, location_id: int, sensor_id: int) -> list[dict]:
    """Turn one /hours page into rows for readings: one dict per result.

    Keys, named like the columns: sensor_id, period_end, location_id, parameter,
    units, value.
    - period_end comes from result["period"]["datetimeTo"]["utc"], parsed into a
      datetime that keeps its UTC zone (the text ends in "Z").
    - parameter and units come from result["parameter"]["name"] and ["units"].

    Which edge cases tests/test_load.py checks is yours to decide in task 10.
    """
    raise NotImplementedError("TODO(task 10): write rows_from_page()")


def upsert_readings(conn, rows: list[dict]) -> int:
    """Insert rows into readings and return how many were sent.

    A row whose key (sensor_id, period_end) is already there updates it instead:
    INSERT ... ON CONFLICT (sensor_id, period_end) DO UPDATE, setting value and
    loaded_at = now(). Use %s query parameters, never f-strings or joined strings.
    The caller runs it inside one transaction per sensor (with conn.transaction():).
    """
    raise NotImplementedError("TODO(task 10): write upsert_readings()")
