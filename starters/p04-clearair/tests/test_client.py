"""Tests for fetch_pages(). Task 9 asks you to write these four.

Write a fake get_page(page_no) that serves N made-up rows in pages of `limit`
and counts its calls. Write each test, remove its skip and run `uv run pytest -q`.
No test calls the real API.
"""

import pytest

from clearair.client import fetch_pages  # noqa: F401  (your tests will use it)


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_250_rows_in_pages_of_100():
    """250 rows: fetch_pages makes 3 calls and returns 250 rows in all."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_exactly_200_rows():
    """Exactly 200 rows: 3 calls, and the last page is empty."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_no_rows():
    """0 rows: 1 call, and no rows."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_source_that_never_ends():
    """A fake that always returns a full page: an error after max_pages calls."""
    raise NotImplementedError("TODO(task 9): write this test")
