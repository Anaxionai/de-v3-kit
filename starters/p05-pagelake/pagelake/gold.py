"""The gold layer: small tables built from silver with SQL.

    uv run --env-file .env python -m pagelake.gold

sql/gold_<name>.sql becomes s3://<bucket>/gold/<name>/<name>.parquet.
The command line is set-up and is complete; build_gold() is yours.
"""

GOLD_TABLES = ("top_pages", "views_by_language")


def build_gold() -> dict[str, int]:
    """Build both gold tables from silver and return the rows of each, such as
    {"top_pages": 420, "views_by_language": 42}.

    For each name in GOLD_TABLES: read sql/gold_<name>.sql, fill {silver} as
    query.py does (query.fill()), wrap it in
    COPY (...) TO 's3://<bucket>/gold/<name>/<name>.parquet' (FORMAT parquet),
    and count the rows written. Take a final ";" off the query first (and any
    comment after it), and put the query on its own lines inside the brackets:
    a ";" or a "--" comment inside COPY ( ... ) breaks the statement.
    """
    raise NotImplementedError("TODO(task 10): write build_gold()")


def main() -> None:
    for name, rows in build_gold().items():
        print(f"{name}: {rows} rows")


if __name__ == "__main__":
    main()
