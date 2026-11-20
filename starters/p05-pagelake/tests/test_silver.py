"""Tests for hour_files(). Task 9 asks you to write these two.

hour_files() is pure: the tests need no bucket and no emulator.
"""

from datetime import date  # noqa: F401  (your tests will use it)

import pytest

from pagelake.silver import hour_files  # noqa: F401


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_a_day_has_24_files():
    """hour_files(date(2026, 11, 2)) has 24 keys, the first ending in pageviews-20261102-010000.gz."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_the_last_hour_is_the_next_days_file():
    """The last key of 2 November ends in pageviews-20261103-000000.gz (the end-of-hour rule)."""
    raise NotImplementedError("TODO(task 9): write this test")
