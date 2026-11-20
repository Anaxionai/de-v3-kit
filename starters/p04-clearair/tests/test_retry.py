"""Tests for call_with_retries(). Task 12 asks you to write these three.

Pass sleep=waits.append (with waits = []) so that no test really waits, and
give call_with_retries a fake func that raises the errors you list, then succeeds.
"""

import pytest

from clearair.client import ApiError  # noqa: F401  (your tests will use it)
from clearair.retry import call_with_retries  # noqa: F401


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_two_503s_then_success():
    """503, 503, then success: 3 calls, waits [1, 2], and the result comes back."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_401_is_not_retried():
    """401: 1 call, no wait, and the error is raised."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_four_503s_give_up():
    """503 four times: 4 calls, waits [1, 2, 4], then the error is raised."""
    raise NotImplementedError("TODO(task 12): write this test")
