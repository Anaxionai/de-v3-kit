"""Shared test set-up: one small SparkSession for every test.

The Guided starter gives this file complete: it is test set-up, not a task.
Run the tests in the Spark container, from taxiscale/:
    docker compose exec spark python3 -m pytest -q
"""

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("taxiscale-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .config("spark.eventLog.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()
