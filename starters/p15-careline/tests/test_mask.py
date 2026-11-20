"""Tests for careline/mask.py: task 7 tests mask_text(), task 9 tests the guard.

The names, phone numbers and email below are made up: test data, not a leak.
Write each body, run `uv run pytest -q`, then remove the skip. No database and
no model: NAMES stands in for load_names(conn).
"""

import pytest

from careline.mask import assert_masked, find_personal, mask_text  # noqa: F401  (your tests call them)

NAMES = ["D'Souza", "Gauri", "Menon", "Ravi", "Yadav"]
# The five ways a phone number is typed into a note (data/clinic/README.md in the kit).
PHONE_FORMS = ["9876543210", "98765 43210", "98765-43210", "+91 98765 43210", "098765-43210"]


@pytest.mark.skip(reason="TODO(task 7): write this test, then remove the skip")
def test_every_phone_form_is_masked():
    """Put each of PHONE_FORMS in a sentence, such as "Call back on ... with the results.".
    After mask_text() the sentence holds [PHONE] and find_personal() finds nothing."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7): write this test, then remove the skip")
def test_email_is_masked():
    """"Send the report to gauri.menon60@example.com." becomes "Send the report to [EMAIL].":
    the names inside the address do not leave pieces of it behind."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7): write this test, then remove the skip")
def test_name_in_capitals_is_masked():
    """"Name on the file: GAURI MENON." becomes "Name on the file: [NAME] [NAME].\""""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7): write this test, then remove the skip")
def test_title_and_surname_are_masked():
    """"Ms Menon prefers an early slot." and "Referred to Dr D'Souza for a second opinion."
    keep the title and lose the surname."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7): write this test, then remove the skip")
def test_appointment_id_stays():
    """"Seen under A09783001." is not personal data: mask_text() returns it unchanged
    and find_personal() finds nothing."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_guard_refuses_a_phone_number():
    """assert_masked() raises ValueError for a list with one text that holds a phone
    number, and the error message does not contain the number."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_guard_lets_masked_text_through():
    """assert_masked() returns None for texts that went through mask_text()."""
    raise NotImplementedError("TODO(task 9): write this test")
