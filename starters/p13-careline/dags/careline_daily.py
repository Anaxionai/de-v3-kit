"""careline_daily: load one day's appointments file, check it, then publish it.

Task order: load_raw -> check_raw -> build_clean -> check_privacy -> build_report.
Every task works on the run's day (`ds`), never on the clock.

    docker compose exec airflow airflow dags test careline_daily <day>

Import the careline modules inside each task, not at the top of this file:
Airflow reads this file every 30 seconds, and Great Expectations is slow to import.
"""

import pendulum
from airflow.sdk import dag, task
from airflow.sdk.exceptions import AirflowFailException, AirflowSkipException  # noqa: F401  (your tasks raise them)


@dag(
    dag_id="careline_daily",
    schedule="@daily",
    catchup=False,
    # Before your first data day. `dags test` runs any day you name.
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
)
def careline_daily():
    @task
    def load_raw(ds=None) -> int:
        """Load the day's file into raw with load.load_day(ds); return the rows.

        First the completeness check, quality.check_file_present(ds): when the
        day's file is missing, log a warning and raise AirflowSkipException.
        """
        raise NotImplementedError("TODO(task 9): check the file is there, then load the day")

    @task
    def check_raw(ds=None) -> None:
        """Run quality.validate_day(ds). Raise AirflowFailException naming the failed
        critical Expectations; warnings alone let the run go on."""
        # TODO(task 10): also validate contract.contract_suite() here, as critical checks.
        raise NotImplementedError("TODO(task 9): fail only on critical failures")

    @task
    def build_clean(ds=None) -> None:
        """Rebuild the day's clean rows: run sql/clean.sql with {"day": ds}."""
        # TODO(task 11): run sql/masking.sql in place of sql/clean.sql.
        raise NotImplementedError("TODO(task 9): rebuild the day's clean rows")

    @task
    def check_privacy(ds=None) -> None:
        """Run checks/pii_scan.sql and a critical GX check that no text value in the
        day's clean rows matches the phone-or-email pattern in the brief (leave
        patient_key out: a hex hash often holds 10 digits in a row). Fail on any hit."""
        raise NotImplementedError("TODO(task 11): fail when personal data is downstream of raw")

    @task
    def build_report(ds=None) -> None:
        """Rebuild the day's report rows: run sql/report.sql with {"day": ds}."""
        raise NotImplementedError("TODO(task 9): rebuild the day's report rows")

    # TODO(task 9): chain load_raw, check_raw, build_clean and build_report in that order.
    # TODO(task 11): put check_privacy between build_clean and build_report.


# TODO(task 9): call careline_daily() here, so Airflow finds the DAG.
