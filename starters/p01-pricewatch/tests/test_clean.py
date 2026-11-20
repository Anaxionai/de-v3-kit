"""Tests for the name rules in pricewatch/clean.py. Task 22 asks you to write them.

These tests wait for task 22. Your package pricewatch/pricewatch/ only exists from
task 12, so this file imports nothing yet: add `from pricewatch.clean import ...` at the
top when you write the tests. Write each test, remove its skip line, and run
`uv run pytest -q`. No test reads data/: every input is written in the test.
"""

import pytest


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_clean_market():
    """clean_market with @pytest.mark.parametrize and six (name, expected) pairs:
    extra spaces, lower case, no space before a bracket, a space before a comma, a name
    from MARKET_ALIASES, and a name that is already clean."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_clean_commodity_in_table():
    """A commodity name from your COMMODITY_NAMES table comes out with your spelling."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_clean_commodity_not_in_table():
    """A commodity name that is not in COMMODITY_NAMES comes out tidy and otherwise unchanged."""
    raise NotImplementedError("TODO(task 22): write this test")
