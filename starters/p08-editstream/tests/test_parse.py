"""Test parse_events() on a small DataFrame, without Kafka (task 10).

Run in the Spark container: docker compose exec spark pytest tests -q
"""

import pytest

pytest.importorskip("pyspark")  # on your laptop, without PySpark, these tests are skipped

from stream.parse import parse_events  # noqa: F401  (your test calls it)


@pytest.mark.skip(reason="TODO(task 10): write this test, then remove the skip")
def test_parse_keeps_only_wikipedia_edits(spark):
    """Make a DataFrame with one column `value` (a string or bytes) and four rows:
    an edit on en.wikipedia.org, an edit on www.wikidata.org, a `log` event
    and broken JSON. parse_events() must return exactly one row, with
    language "en" and an event_time."""
    raise NotImplementedError("TODO(task 10): write this test")
