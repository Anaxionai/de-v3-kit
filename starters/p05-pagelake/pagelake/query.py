"""Run one SQL file against the silver layer and print the result.

    uv run --env-file .env python -m pagelake.query sql/q1_one_day.sql
    uv run --env-file .env python -m pagelake.query sql/q1_one_day.sql --layout pageviews_by_lang --explain

In a SQL file, write FROM {silver}. It becomes
    read_parquet('s3://<bucket>/silver/<layout>/*/*.parquet', hive_partitioning = true)
for the layout you choose (default: pageviews). <bucket> in the file becomes your
bucket's name. With --explain, the command prints EXPLAIN ANALYZE: the plan with
the files scanned, the data read and the time.

The Guided starter gives this file complete: it is set-up, not a task.
"""

import argparse
from pathlib import Path

import duckdb

from pagelake import lake


def silver_sql(bucket: str, layout: str = "pageviews") -> str:
    """What {silver} becomes in a SQL file."""
    return f"read_parquet('s3://{bucket}/silver/{layout}/*/*.parquet', hive_partitioning = true)"


def fill(sql: str, bucket: str, layout: str = "pageviews") -> str:
    """Replace {silver} and <bucket> in a SQL text."""
    return sql.replace("{silver}", silver_sql(bucket, layout)).replace(
        "<bucket>", bucket
    )


def has_statement(sql: str) -> bool:
    """True when the text holds SQL, not only comments and blank lines."""
    return any(line.split("--", 1)[0].strip(" ;\t") for line in sql.splitlines())


def run(path: str, layout: str = "pageviews", explain: bool = False) -> int:
    """Run one SQL file and print its result. Return 0, or 1 when it failed."""
    text = Path(path).read_text(encoding="utf-8")
    if not has_statement(text):
        print(f"{path} holds no SQL yet, only comments: write the query first.")
        return 1
    sql = fill(text, lake.bucket(), layout)
    con = lake.connect()
    try:
        if explain:
            for row in con.sql("EXPLAIN ANALYZE " + sql).fetchall():
                print(row[1])
            return 0
        result = con.sql(sql)
        if result is None:
            print("done")
        else:
            result.show(max_rows=50)
        return 0
    except duckdb.Error as error:
        print(f"The query failed: {error}")
        return 1


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python -m pagelake.query", description="Run a SQL file against silver."
    )
    parser.add_argument("file", help="the SQL file, such as sql/q1_one_day.sql")
    parser.add_argument(
        "--layout",
        default="pageviews",
        help="the folder under silver/ (default: pageviews)",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="print EXPLAIN ANALYZE instead of the result",
    )
    args = parser.parse_args(argv)
    raise SystemExit(run(args.file, args.layout, args.explain))


if __name__ == "__main__":
    main()
