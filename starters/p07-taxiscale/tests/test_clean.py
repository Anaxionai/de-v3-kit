"""Tests for clean_trips(). Task 9 asks you to write these five.

Build each test's rows with spark.createDataFrame() and the TLC column names that
clean_trips() uses: tpep_pickup_datetime, tpep_dropoff_datetime, PULocationID,
DOLocationID, trip_distance, passenger_count, payment_type, fare_amount and
total_amount. Compare the result with assertDataFrameEqual, or check which rows
stay (give each row a different PULocationID, for example). Write each test, remove
its skip, and run in the Spark container: docker compose exec spark python3 -m pytest -q
"""

import pytest

from jobs.clean import clean_trips  # noqa: F401  (your tests will use it)


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_wrong_month_is_dropped(spark):
    """A trip picked up outside the months asked for is dropped."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_impossible_duration_is_dropped(spark):
    """A trip of 0 minutes or less, or of 360 minutes or more, is dropped."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_impossible_miles_are_dropped(spark):
    """A trip of 0 miles or less, or of 100 miles or more, is dropped."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_negative_fare_is_dropped(spark):
    """A trip with a fare below 0 is dropped."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9): write this test, then remove the skip")
def test_good_row_is_kept(spark):
    """A good trip stays, with the new names and the three new columns."""
    raise NotImplementedError("TODO(task 9): write this test")
