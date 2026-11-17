"""Tests for aws/lambda/ingest.py. pyproject.toml puts aws/lambda/ on pytest's path."""

import pytest
from ingest import select_new


def station(station_id: str, last_reported: int) -> dict:
    """A small hand-made station_status record: select_new reads only last_reported."""
    return {
        "station_id": station_id,
        "num_bikes_available": 3,
        "last_reported": last_reported,
    }


@pytest.mark.skip(reason="TODO(task 9): remove this line once select_new is written")
def test_select_new_keeps_only_newer_stations():
    stations = [station("a", 100), station("b", 200), station("c", 300)]
    new, watermark = select_new(stations, 150)
    assert [s["station_id"] for s in new] == ["b", "c"]
    assert watermark == 300


# TODO(task 9): a second test: a station exactly at the watermark is not new, and when no
#   station is new the watermark stays where it was.
