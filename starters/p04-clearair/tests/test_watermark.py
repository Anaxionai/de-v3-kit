"""Tests for window_start() and next_watermark(). Task 11 asks you to write these four.

Both functions are pure, so the tests need no database. Use timezone-aware
datetimes, such as datetime(2026, 11, 12, 6, tzinfo=timezone.utc).
"""

import pytest

from clearair.watermark import next_watermark, window_start  # noqa: F401  (your tests will use them)


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_window_start_without_a_watermark():
    """No watermark: the window starts start_days days before until."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_window_start_with_a_watermark():
    """A watermark: the window starts lookback_hours hours before it."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_next_watermark_with_rows():
    """The newest of the times, whatever their order."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_next_watermark_with_no_rows():
    """An empty list keeps the old watermark."""
    raise NotImplementedError("TODO(task 11): write this test")
