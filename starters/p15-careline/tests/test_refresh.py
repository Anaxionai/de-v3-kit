"""Tests for changed_notes(). Task 11 asks you to test its three cases.

changed_notes() is pure, so the tests need no database and no model: make up two
small dictionaries of note id to version. Write each body, then remove the skip.
"""

import pytest

from careline.refresh import changed_notes  # noqa: F401  (your tests call it)


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_no_change_gives_nothing():
    """When every current version equals the chunks' version, both lists are empty."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_one_corrected_note():
    """A note at version 2 whose chunks carry version 1 is corrected, and only that note."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_one_new_note():
    """A note in clean.visit_notes with no chunks yet is new, and only that note."""
    raise NotImplementedError("TODO(task 11): write this test")
