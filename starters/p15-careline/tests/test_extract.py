"""Tests for validate(). Task 10 asks for one good row and one bad row for each rule.

validate() is pure, so these tests never call the model. TEXT is a made-up,
masked note to check rows against. Write each body, then remove the skip.
"""

import pytest

from careline.extract import VisitFacts, validate  # noqa: F401  (your tests call them)

TEXT = (
    "Pain in the right knee for ten days. Worse on climbing stairs. Cannot squat or sit on the floor. "
    "No past illnesses of note. Walks with a slight limp. No warning signs; routine care. "
    "Knee strengthening exercises shown. Call back on [PHONE] with the results. Follow up in two weeks."
)


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_good_row_has_no_problems():
    """A row that agrees with TEXT (symptom "pain in the right knee", body area
    "knee", urgency "routine") gives an empty list."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_body_area_not_in_the_list_is_a_problem():
    """A body area outside BODY_AREAS, such as "leg", gives one problem."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_symptom_not_in_text_is_a_problem():
    """A symptom the note does not state, such as "knee swelling", gives the problem
    "symptom not in text"."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_unsupported_urgent_is_a_problem():
    """Urgency "urgent" for TEXT, which holds neither "urgent" nor "emergency",
    gives one problem."""
    raise NotImplementedError("TODO(task 10): write this test")
