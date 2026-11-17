"""The contract refuses bad files: tests on the two generated samples (task 10).

Task 10, step 1 copies data/sample/appointments_good.csv and appointments_bad.csv
into sample/. These tests need no database. Run them with `uv run pytest -q`.
"""

from pathlib import Path

import pytest

from careline import contract  # noqa: F401  (your tests call it)

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample"
GOOD = SAMPLE_DIR / "appointments_good.csv"
BAD = SAMPLE_DIR / "appointments_bad.csv"


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_good_sample_passes_the_contract_suite():
    """Read GOOD with pandas (every value as text) and validate contract_suite():
    every Expectation succeeds."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_bad_sample_fails_the_contract_suite():
    """BAD has a duplicated id, an empty patient_id, a negative fee and a status
    of DONE: the contract suite does not succeed."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_renamed_fee_column_is_refused():
    """GOOD's columns with fee_rupees renamed to fee: check_header() raises
    ValueError, and the message names both columns."""
    raise NotImplementedError("TODO(task 10): write this test")
