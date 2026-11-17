"""Full and incremental loads from the station database into ClearAir.

`source` is a psycopg connection to the station database (STATIONDB_URL, port
5433) and `target` one to the clearair database (DATABASE_URL). The source's
stations table has nine columns, listed in the kit's data/airquality/README.md.
The target's stations table has the same nine, plus loaded_at and deleted_at
(NULL while the station is current).
"""


def upsert_stations(conn, rows: list) -> int:
    """Insert rows into the target's stations table and return how many were sent.

    INSERT ... ON CONFLICT (station_id) DO UPDATE every column, set loaded_at to
    now() and set deleted_at back to NULL, so a station that returns to the
    source is current again. Use %s query parameters.
    """
    raise NotImplementedError("TODO(task 21): write upsert_stations()")


def full_load(source, target) -> int:
    """Copy every source row and return the row count.

    Read every row with SELECT ... FROM stations, upsert them, and set the
    "stations" watermark in load_state to the newest updated_at read, in the
    same target transaction as the rows.
    """
    raise NotImplementedError("TODO(task 21): write full_load()")


def incremental_load(source, target) -> int:
    """Copy only the rows that changed since the "stations" watermark, and
    return how many were read.

    Read the rows with updated_at >= the watermark (>=, so a row that shares the
    watermark's time is read again, never missed), upsert them and move the
    watermark with watermark.next_watermark(), in one target transaction. When
    nothing changed, the watermark stays where it was.
    """
    raise NotImplementedError("TODO(task 21): write incremental_load()")


def find_deleted(source_ids, target_ids) -> list[int]:
    """Return the ids in target_ids that are not in source_ids.

    Raise ValueError when source_ids is empty: an empty or unreachable source
    must never mark every station as deleted.
    """
    raise NotImplementedError("TODO(task 22): write find_deleted()")


def mark_deleted(source, target) -> list[int]:
    """Mark the stations that are gone from the source as deleted, and return
    their ids.

    Read every source id and the target ids WHERE deleted_at IS NULL, call
    find_deleted(), then set deleted_at = now() on those rows in one UPDATE
    (WHERE station_id = ANY(%s)). Never DELETE a row: its history stays.
    """
    raise NotImplementedError("TODO(task 22): write mark_deleted()")
