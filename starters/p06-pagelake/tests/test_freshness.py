"""Tests for status() on both sides of the 1-day promise (task 14). No bucket needed."""

import pytest

from pagelake import freshness  # noqa: F401  (your tests call it)


@pytest.mark.skip(reason="TODO(task 14): write this test, then remove the skip")
def test_one_day_old_is_fresh():
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14): write this test, then remove the skip")
def test_two_days_old_is_late():
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14): write this test, then remove the skip")
def test_no_complete_day_is_late():
    """newest_day None (no day with all 24 hours) is LATE."""
    raise NotImplementedError("TODO(task 14): write this test")
