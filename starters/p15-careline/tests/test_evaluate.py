"""Tests for hit_rate(). Task 12 asks you to test it.

hit_rate() is pure, so the tests need no database and no model: make up a few
(expected_note, note_ids) pairs. Write each body, then remove the skip.
"""

import pytest

from careline.evaluate import hit_rate  # noqa: F401  (your tests call it)


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_hit_at_1_counts_only_the_first_chunk():
    """An expected note that is second in its list is a miss at k=1."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_hit_at_3_counts_the_first_three_chunks():
    """An expected note that is third in its list is a hit at k=3, and a list
    without it is a miss."""
    raise NotImplementedError("TODO(task 12): write this test")
