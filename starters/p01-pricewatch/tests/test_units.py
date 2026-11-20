"""Tests for the unit rules in pricewatch/units.py. Task 22 asks you to write them.

Add `from pricewatch.units import ...` and `from pricewatch.load import BadRow` at the
top when you write the tests. Write each test, remove its skip line, and run
`uv run pytest -q`. Build each record in the test itself, as a dictionary.
"""

import pytest


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_to_rupees_per_kg():
    """to_rupees_per_kg with @pytest.mark.parametrize: one case each for quintal,
    kilogram and tonne, with the price you give and the rupees per kilogram you expect."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_unknown_unit_raises():
    """An unknown unit raises ValueError (pytest.raises)."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_zero_price_is_rejected():
    """convert_record raises BadRow for a price of zero."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_min_above_max_is_rejected():
    """convert_record raises BadRow when the minimum price is above the maximum."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_unclear_unit_is_rejected():
    """convert_record raises BadRow for a modal price below your MIN_QUINTAL_PRICE."""
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22): write this test, then remove the skip")
def test_good_record_converts():
    """A good record comes back with the three prices in rupees per kilogram and unit "kg"."""
    raise NotImplementedError("TODO(task 22): write this test")
