"""Tests for the step functions, without Airflow and without the bucket (task 9).

Each test makes its own files in pytest's tmp_path folder. Write each test,
remove its skip and run `uv run pytest -q`.
"""

import pytest

from pagelake import steps  # noqa: F401  (your tests call it)


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_missing_hours_names_the_end_of_day_file(tmp_path):
    """Create the 24 files of 2026-11-06 as empty files in tmp_path, delete
    pageviews-20261107-000000.gz, and check that missing_hours returns only
    that name."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_check_language_counts_a_clean_file(tmp_path):
    """Write a 3-row Parquet file in tmp_path with duckdb.sql("COPY (...) TO ...")
    (columns lang, mobile, title, views, hour), and check the rows and views
    check_language returns for one language."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_check_language_refuses_a_repeated_row(tmp_path):
    """The same file with one row written twice: check_language raises
    ValueError (use pytest.raises)."""
    raise NotImplementedError("TODO(task 9): write this test")
