"""Run one Athena .sql file in the CycleCity workgroup; print its rows and bytes scanned.

From cyclecity/:  uv run python aws/athena/run_query.py aws/athena/q01_trips_by_month.sql
AWS_PROFILE chooses the target: cyclecity (AWS) or emulator (where bytes scanned is always 0).
"""

import sys

# TODO(task 11): your id in both names (the database uses _ where your id has -).
DATABASE = "cyclecity_<your_id>"
WORKGROUP = "cyclecity-<your-id>"


def start_query(athena, sql: str) -> str:
    """Start sql in WORKGROUP with DATABASE as its database; return the execution id.

    The workgroup is enforced, so its output location (athena-results/ in the clean
    bucket) is used without naming it here.
    """
    raise NotImplementedError("TODO(task 11): start the query")


def wait(athena, query_id: str) -> dict:
    """Poll until the query is SUCCEEDED, FAILED or CANCELLED; return its QueryExecution.

    Stop with the state and its reason when it did not succeed.
    """
    raise NotImplementedError("TODO(task 11): wait for the query to finish")


def print_results(athena, query_id: str, execution: dict) -> None:
    """Print every result row (results come in pages), then DataScannedInBytes."""
    raise NotImplementedError("TODO(task 11): print the rows and the bytes scanned")


def main(path: str) -> None:
    """Read the .sql file, then start, wait and print, with a boto3 Athena client."""
    raise NotImplementedError("TODO(task 11): run one file")


if __name__ == "__main__":
    main(sys.argv[1])
