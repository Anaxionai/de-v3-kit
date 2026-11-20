"""Reload one match inside a transaction: delete its rows, then insert them again.

Task 24. Run it from scorebook/:

    uv run python load/reload_match.py data/matches/980987.json --fail
    uv run python load/reload_match.py data/matches/980987.json

Keep this file in load/, next to load_matches.py, so the import below finds it.
"""

from pathlib import Path

import psycopg
from load_matches import (  # noqa: F401  (reload_match and main use them)
    DATABASE_URL,
    DELIVERY_COLUMNS,
    delivery_rows,
    innings_rows,
    match_row,
    read_match,
)


def count_rows(conn: psycopg.Connection, match_id: int) -> str:
    """Return the number of rows in matches, innings and deliveries for one match, as one
    line of text, such as "matches=1, innings=2, deliveries=242"."""
    raise NotImplementedError("TODO(task 24): write count_rows(conn, match_id)")


def reload_match(conn: psycopg.Connection, path: Path, fail: bool = False) -> None:
    """Delete one match and insert it again, all inside `with conn.transaction():`.

    - Delete the match from deliveries, then innings, then matches: children first.
    - If fail is true, raise RuntimeError("simulated crash after the deletes") right after
      the deletes, still inside the transaction.
    - Insert the match, its innings and its deliveries as the loader does, with the
      loader's functions.
    """
    raise NotImplementedError("TODO(task 24): write reload_match(conn, path, fail)")


def main() -> None:
    """Connect with psycopg.connect(DATABASE_URL, autocommit=True), print the counts, call
    reload_match (fail is true when sys.argv holds --fail; catch RuntimeError and print
    it), then print the counts again."""
    raise NotImplementedError("TODO(task 24): write main()")


if __name__ == "__main__":
    main()
