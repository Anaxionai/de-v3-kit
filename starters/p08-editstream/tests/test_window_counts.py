"""Test count_per_language() on small batch DataFrames (tasks 11 and 12).

A watermark has no effect on a batch DataFrame, so these tests check the
windows and the deduplication, not lateness.
Run in the Spark container: docker compose exec spark pytest tests -q
"""

import pytest

pytest.importorskip("pyspark")  # on your laptop, without PySpark, these tests are skipped

from stream.window_counts import count_per_language  # noqa: F401  (your tests call it)


@pytest.mark.skip(reason="TODO(task 11): write this test, then remove the skip")
def test_counts_per_window_and_language(spark):
    """Five edits made with spark.createDataFrame (columns event_id, event_time,
    language) over two minutes and two languages. Assert `edits` for every
    (window_start, language) pair."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 12): write this test, then remove the skip")
def test_an_edit_sent_twice_counts_once(spark):
    """The same edit twice (same event_id and event_time) and one other edit in
    that minute: `edits` for that window and language is 2."""
    raise NotImplementedError("TODO(task 12): write this test")
