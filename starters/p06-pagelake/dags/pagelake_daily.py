"""pagelake_daily: land one day, rebuild its silver partition, check the six
languages side by side, then rebuild gold (tasks 10 to 12).

The tasks call the tested functions in pagelake/steps.py, silver.py and gold.py,
and take their day from the run (`ds`, such as "2026-11-04"), never from the
clock. Pass a path between tasks, not rows: XCom is for small values.

    docker compose exec airflow airflow dags list-import-errors
    docker compose exec airflow airflow dags test pagelake_daily 2026-11-04
"""

from datetime import date  # noqa: F401  (your tasks use it)

import pendulum
from airflow.sdk import CronDataIntervalTimetable, dag, task

from pagelake import gold, lake, silver, steps  # noqa: F401  (your tasks use them)

# TODO(task 12): import timedelta from datetime, and send_alert from pagelake.alerts.


@dag(
    dag_id="pagelake_daily",
    schedule=CronDataIntervalTimetable("@daily", timezone="UTC"),
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    catchup=False,
    # TODO(task 11): allow one active run at a time (rebuild_gold reads every day).
    # TODO(task 12): add on_failure_callback (one alert per failed run), and
    # default_args with retries, retry_delay and execution_timeout for every task.
)
def pagelake_daily():
    @task
    def land(ds=None) -> int:
        """Land the run's day in bronze and return the number of files (24).

        Call steps.land_day with the day as a date, the drop folder
        (steps.data_dir() / "raw") and lake.bucket(). Airflow fills ds.
        """
        raise NotImplementedError("TODO(task 10): land the run's day")

    @task
    def rebuild_silver(landed: int, ds=None) -> str:
        """Rebuild the day's silver partition with P5's silver.load_day, then
        return the day's path from steps.silver_path: a short text, not rows."""
        raise NotImplementedError("TODO(task 10): rebuild the day's silver partition")

    @task
    def check(path: str, lang: str) -> dict:
        """Check one language of the rebuilt day with steps.check_language on a
        lake.connect() connection, and return its result."""
        raise NotImplementedError("TODO(task 10): check one language")

    @task
    def rebuild_gold(results: list[dict]) -> dict:
        """Rebuild gold with P5's gold.build_gold(), once all six checks passed."""
        raise NotImplementedError("TODO(task 10): rebuild gold")

    # TODO(task 10): wire the tasks. land, then rebuild_silver; then one check task
    # per language in steps.LANGS, named check_<lang> (use .override), each given
    # the silver path; then pass the list of all six results to rebuild_gold.


# TODO(task 10): call pagelake_daily() here, so Airflow finds the DAG.
