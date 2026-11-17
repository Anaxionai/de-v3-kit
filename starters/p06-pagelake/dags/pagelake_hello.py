"""pagelake_hello: your first DAG. It counts the course week on your laptop and in
your bucket (task 8).

Airflow reads every file in dags/. Write the Airflow parts yourself: the
decorators, the line that passes two results to report, and the call at the
end. Then run, in the pagelake/ folder:

    docker compose exec airflow airflow dags list-import-errors
    docker compose exec airflow airflow dags test pagelake_hello 2026-11-02

Inside Airflow, pagelake/ is the working folder, so data/raw is the same folder
as on your laptop.
"""

from airflow.sdk import dag, task  # noqa: F401  (you use both below)

from pagelake import lake  # noqa: F401  (count_bronze uses it)


# TODO(task 8): decorate with @dag(dag_id="pagelake_hello", schedule=None).
def pagelake_hello():
    """The DAG: count the raw files and the bronze objects, then report both."""

    # TODO(task 8): make this a task with @task.
    def count_raw() -> int:
        """The number of .gz files in data/raw/ (168 for the course week)."""
        raise NotImplementedError("TODO(task 8): count the .gz files in data/raw")

    # TODO(task 8): make this a task with @task.
    def count_bronze() -> int:
        """The number of keys under bronze/pageviews/ in your bucket (168).

        Count them with the list_objects_v2 paginator of lake.s3_client(), in
        lake.bucket(). No endpoint, key or bucket name in this file: lake.py
        reads them from the environment.
        """
        raise NotImplementedError("TODO(task 8): count the bronze objects")

    # TODO(task 8): make this a task with @task.
    def report(raw: int, bronze: int) -> None:
        """Print both counts on one line, such as "raw files: 168, bronze objects: 168"."""
        raise NotImplementedError("TODO(task 8): print both counts")

    # TODO(task 8): pass the results of count_raw() and count_bronze() to report().


# TODO(task 8): call pagelake_hello() here, so Airflow finds the DAG.
