"""Tests for find_deleted(). Task 22 asks you to write these three.

find_deleted() is pure, so the tests need no database: pass lists of ids.
"""

import pytest

from clearair.stationdb import find_deleted  # noqa: F401  (your tests will use it)


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_three_stations_gone():
    """Three ids are in the target but not in the source: exactly those three come back."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_nothing_gone():
    """The same ids on both sides: nothing comes back."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_empty_source_raises():
    """An empty source raises ValueError instead of marking every station."""
    raise NotImplementedError("TODO(task 22): write this test")
