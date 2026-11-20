"""Watermarks: where each load stopped, kept in the load_state table.

A row of load_state is named "sensor:<sensor-id>" for a sensor's readings
(task 11) and "stations" for the station table (task 21). All times are
timezone-aware datetimes in UTC.
"""

from datetime import datetime


def read_watermark(conn, name: str) -> datetime | None:
    """Return the watermark stored in load_state under name, or None when there
    is no row for it yet (a first run)."""
    raise NotImplementedError("TODO(task 11): write read_watermark()")


def write_watermark(conn, name: str, value: datetime) -> None:
    """Store value as the watermark of name: an upsert on load_state that also
    sets updated_at. It runs inside the caller's transaction, so the rows and
    their watermark are committed together or not at all."""
    raise NotImplementedError("TODO(task 11): write write_watermark()")


def window_start(
    watermark: datetime | None, until: datetime, start_days: int, lookback_hours: int
) -> datetime:
    """Return the start of the next request's window (its datetime_from).

    - No watermark yet: until minus start_days days.
    - Otherwise: the watermark minus lookback_hours hours, so that late data in
      the last hours is read again.
    """
    raise NotImplementedError("TODO(task 11): write window_start()")


def next_watermark(times: list[datetime], old: datetime | None) -> datetime | None:
    """Return the new watermark: the newest of times (the values just loaded),
    or old when times is empty. Never the clock."""
    raise NotImplementedError("TODO(task 11): write next_watermark()")
