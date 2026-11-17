"""The blocking suite on the two generated samples, without a database (task 12).

GitHub Actions runs these tests on every pull request in your public careline repository.
"""

from pathlib import Path

import pytest

from careline import quality  # noqa: F401  (your tests call it)

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample"
GOOD = SAMPLE_DIR / "appointments_good.csv"
BAD = SAMPLE_DIR / "appointments_bad.csv"


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_blocking_suite_passes_on_the_good_sample():
    """validate_frame(GOOD as a DataFrame, blocking_suite(...)) succeeds. Take the
    day and the doctor ids from the sample itself, not from the database."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_blocking_suite_fails_on_the_bad_sample():
    """validate_frame(BAD as a DataFrame, blocking_suite(...)) does not succeed."""
    raise NotImplementedError("TODO(task 12): write this test")
