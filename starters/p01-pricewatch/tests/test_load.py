"""Tests for the loader in pricewatch/load.py. Task 22 asks you to write them.

Add `from pricewatch.load import read_prices` at the top when you write the tests. Every
file a test reads is written into tmp_path, never read from data/. Write each test,
remove its skip line, and run `uv run pytest -q`.
"""

import pytest


@pytest.fixture
def bad_file(tmp_path):
    """Write a price file into tmp_path and return its path.

    The file has the 11-column header, two good rows and five bad rows, each with a
    different fault: an empty price, a price of abc, the date 31/02/2026, an empty market,
    and a line cut short. Write it with
    path.write_text("\\n".join(lines) + "\\n", encoding="utf-8").
    """
    raise NotImplementedError("TODO(task 22): write the bad_file fixture")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_five_bad_rows(bad_file):
    """read_prices gives two records and five bad rows. Check the five line numbers, and
    one word of each reason (for example assert "date" in reason), not whole sentences."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_missing_column(tmp_path):
    """A file whose header lacks Modal_Price makes read_prices raise ValueError."""
    raise NotImplementedError("TODO(task 22): write this test")
