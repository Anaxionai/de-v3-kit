"""Add up the bytes scanned by every query in the CycleCity workgroup (task 26).

From cyclecity/:  AWS_PROFILE=cyclecity uv run python aws/athena/bytes_report.py
"""

WORKGROUP = "cyclecity-<your-id>"  # TODO(task 26): your id, as in run_query.py


def main() -> None:
    """Print how many queries the workgroup ran and the total of their DataScannedInBytes.

    List the query ids with list_query_executions (results come in pages), then read them
    with batch_get_query_execution, which takes at most 50 ids per call.
    """
    raise NotImplementedError("TODO(task 26): count the queries and add up their bytes")


if __name__ == "__main__":
    main()
