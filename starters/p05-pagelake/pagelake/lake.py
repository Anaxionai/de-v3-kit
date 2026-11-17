"""PageLake's way into the lake: the settings, a DuckDB connection and a boto3 client.

The Guided starter gives this file complete: it is set-up, not a task.

The settings come from environment variables (see .env.example): AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_ENDPOINT_URL and PAGELAKE_BUCKET.
Run every command from pagelake/ with `uv run --env-file .env python -m pagelake.<module>`.
"""

import os
from urllib.parse import urlparse

import boto3
import duckdb

SETTINGS = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_DEFAULT_REGION",
    "AWS_ENDPOINT_URL",
    "PAGELAKE_BUCKET",
)


def setting(name: str) -> str:
    """The value of one setting, or a clear stop when it is missing."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(
            f"The setting {name} is missing. Copy .env.example to .env, fill it in, "
            "and run with: uv run --env-file .env python -m pagelake.<module>"
        )
    return value


def bucket() -> str:
    """The bucket's name, from PAGELAKE_BUCKET (pagelake-<your-id>)."""
    return setting("PAGELAKE_BUCKET")


def s3_client():
    """A boto3 S3 client. boto3 reads the keys, the region and AWS_ENDPOINT_URL
    from the environment by itself."""
    for name in SETTINGS:
        setting(name)
    return boto3.client("s3")


def _quoted(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def connect() -> duckdb.DuckDBPyConnection:
    """A DuckDB connection that reads and writes s3://<bucket>/... on the emulator.

    It creates the secret `lake`: the keys, the region, the endpoint without
    http:// (localhost:4566), path-style addresses, and plain http when the
    endpoint starts with http://. The first call downloads the httpfs extension.
    """
    endpoint = urlparse(setting("AWS_ENDPOINT_URL"))
    use_ssl = "true" if endpoint.scheme == "https" else "false"
    con = duckdb.connect()
    con.sql("INSTALL httpfs")
    con.sql("LOAD httpfs")
    con.sql(
        f"""
        CREATE OR REPLACE SECRET lake (
            TYPE s3,
            KEY_ID {_quoted(setting("AWS_ACCESS_KEY_ID"))},
            SECRET {_quoted(setting("AWS_SECRET_ACCESS_KEY"))},
            REGION {_quoted(setting("AWS_DEFAULT_REGION"))},
            ENDPOINT {_quoted(endpoint.netloc)},
            URL_STYLE 'path',
            USE_SSL {use_ssl}
        )
        """
    )
    return con
