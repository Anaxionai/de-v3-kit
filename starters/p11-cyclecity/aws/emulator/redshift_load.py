"""Load one snapshot of the station feed into Redshift on the emulator with COPY, then query it.

From cyclecity/, with AWS_PROFILE=emulator and REDSHIFT_PASSWORD set:
    PYTHONPATH=aws/lambda uv run python aws/emulator/redshift_load.py
psycopg comes from task 24 step 1: uv add "psycopg[binary]".
"""

# TODO(task 24): your id in these three names.
CLEAN_BUCKET = "cyclecity-<your-id>-clean"
CLUSTER = "cyclecity-<your-id>-wh"
ROLE_NAME = "cyclecity-<your-id>-redshift"
STATUS_KEY = "redshift/status.json"


def main() -> None:
    """Write the stations as JSON Lines to s3://CLEAN_BUCKET/STATUS_KEY. Connect with psycopg to
    localhost on the port describe-clusters returns, with the password from the
    REDSHIFT_PASSWORD environment variable (never from a file). Create table station_status
    with SORTKEY (last_reported), COPY the file into it with IAM_ROLE (the role's ARN) and
    FORMAT AS JSON 'auto', and print the results of two queries."""
    raise NotImplementedError("TODO(task 24): write, COPY and query")


if __name__ == "__main__":
    main()
