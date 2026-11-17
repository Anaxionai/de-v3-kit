"""Tests for split_text(). Task 8 asks for these four tests.

split_text() is pure, so the tests need no database and no model: make up texts
with as many sentences and words as each case needs. Write each body, run
`uv run pytest -q`, then remove the skip.
"""

import pytest

from careline.chunk import split_text  # noqa: F401  (your tests call it)


@pytest.mark.skip(reason="TODO(task 8): write this test, then remove the skip")
def test_short_text_gives_one_chunk():
    """A text with fewer words than max_words comes back as exactly one chunk."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8): write this test, then remove the skip")
def test_no_chunk_passes_max_words():
    """No chunk has more than max_words words. Keep out of this text any sentence
    that is longer than max_words on its own."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8): write this test, then remove the skip")
def test_new_chunk_starts_with_last_sentence_of_previous():
    """With overlap=1, every chunk after the first starts with the last sentence of
    the chunk before it."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8): write this test, then remove the skip")
def test_no_sentence_is_lost():
    """Every sentence of the text is, whole, in at least one chunk."""
    raise NotImplementedError("TODO(task 8): write this test")
