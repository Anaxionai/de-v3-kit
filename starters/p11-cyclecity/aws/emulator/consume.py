"""Read every record from the stream's one shard on the emulator and summarise them.

From cyclecity/, with AWS_PROFILE=emulator:
    PYTHONPATH=aws/lambda uv run python aws/emulator/consume.py
"""

STREAM = "cyclecity-<your-id>-status"  # TODO(task 24): your id


def main() -> None:
    """Read the shard from a TRIM_HORIZON iterator with get_records, following the next
    iterator, until MillisBehindLatest is 0. Print how many records were read and the
    stations with no bikes (num_bikes_available 0)."""
    raise NotImplementedError("TODO(task 24): read the shard until caught up")


if __name__ == "__main__":
    main()
