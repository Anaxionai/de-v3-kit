"""The connection to CareLine's database, and a runner for SQL files.

Run a SQL file from the careline/ folder, with the data lab's core profile running:

    uv run python -m careline.db sql/00_raw.sql
"""

import os
import sys
from pathlib import Path

import psycopg

# The product folder (the one that holds pyproject.toml). Inside Airflow it is
# /opt/airflow/project and the working folder is somewhere else, so every path
# to sql/, checks/, contracts/ and data/ starts from here.
PRODUCT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PRODUCT_DIR / "data"


def connect() -> psycopg.Connection:
    """Open a connection to the database careline as user de.

    The host comes from DATALAB_DB_HOST: localhost on your laptop, and
    host.docker.internal inside Airflow (the kit's compose.yaml sets it).
    Given complete: it is set-up, not the point of a task.
    """
    host = os.environ.get("DATALAB_DB_HOST", "localhost")
    return psycopg.connect(host=host, port=5432, user="de", password="de", dbname="careline")


def run_sql_file(path: str | Path, params: dict | None = None) -> None:
    """Run every statement of a SQL file in one transaction, and print each result.

    - A relative path is taken from PRODUCT_DIR, so the same call works in Airflow.
    - Split the file into statements at ";" and skip pieces that hold only
      comments and spaces (a file of comments only runs nothing). So never put
      ";" inside a string or a comment in your SQL files.
    - Pass `params` to every statement, so a file can use %(day)s. With
      params, write a literal % in the SQL as %%.
    - After a statement that returns rows (a SELECT), print its column names
      and its rows.
    """
    raise NotImplementedError("TODO(task 8): run a SQL file statement by statement")


if __name__ == "__main__":
    run_sql_file(sys.argv[1])
