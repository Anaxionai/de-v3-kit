"""Send one snapshot of the live station feed through a Kinesis stream on the emulator.

From cyclecity/, with AWS_PROFILE=emulator:
    PYTHONPATH=aws/lambda uv run python aws/emulator/produce.py
PYTHONPATH=aws/lambda lets this script import your fetch() and find_feed() from ingest.py.
"""

STREAM = "cyclecity-<your-id>-status"  # TODO(task 24): your id


def main() -> None:
    """Get the stations with find_feed() and fetch() from ingest (GBFS_URL, then station_status),
    put_record each station on STREAM as JSON with its station_id as the PartitionKey, and print
    how many records were sent."""
    raise NotImplementedError("TODO(task 24): send every station to the stream")


if __name__ == "__main__":
    main()
