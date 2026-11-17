"""Shared test set-up: one small local Spark session for every test.

The tests need PySpark, so they run in the Spark container, from editstream/:

    docker compose exec spark pytest tests -q

On your laptop, `uv run pytest` skips them (PySpark is not installed there).
The Guided starter gives this file complete: it is test set-up, not a task.
"""

import pytest


@pytest.fixture(scope="session")
def spark():
    from pyspark.sql import SparkSession

    session = (
        SparkSession.builder.master("local[1]")
        .appName("editstream-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("WARN")
    yield session
    session.stop()
