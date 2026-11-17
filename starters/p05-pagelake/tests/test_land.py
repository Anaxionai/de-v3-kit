"""Tests for bronze_key(). Task 8 asks you to write these two.

bronze_key() is pure: the tests need no bucket and no emulator. Write each test,
remove its skip and run `uv run pytest -q`.
"""

import pytest

from pagelake.land import bronze_key  # noqa: F401  (your tests will use it)


@pytest.mark.skip(reason="TODO(task 8): write this test, then remove the skip")
def test_first_file_of_the_week():
    """pageviews-20261102-010000.gz -> bronze/pageviews/2026/2026-11/pageviews-20261102-010000.gz"""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8): write this test, then remove the skip")
def test_last_file_of_the_week():
    """The week's last file, pageviews-20261109-000000.gz, keeps its name under 2026/2026-11/."""
    raise NotImplementedError("TODO(task 8): write this test")
