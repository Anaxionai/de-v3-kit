# Guided starter: P5 PageLake

This folder is the start of your `pagelake/` product folder for module 7 (a lakehouse on object storage). It saves you the set-up: the uv project and its lock file, the settings, the connection to the lake, the query runner, every command line, the test files, the SQL files with their headers and the documents with their headings. Every function a task asks for, every query and every answer is still yours.

## What is included

| Path | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A uv project for Python 3.12 with `duckdb` and `boto3`, and `pytest` and `ruff` for development. `pythonpath = ["."]` is set for the tests |
| `.env.example` | The emulator's settings and `PAGELAKE_BUCKET`, with LF line endings |
| `pagelake/lake.py` | **Complete.** The settings, `connect()` (DuckDB with the `lake` secret), `s3_client()` and `bucket()` |
| `pagelake/query.py` | **Complete.** `python -m pagelake.query <file.sql> [--layout <layout>] [--explain]`, and `silver_sql()` and `fill()` |
| `pagelake/land.py` | `bronze_key()`, `land()`, and the command line |
| `pagelake/silver.py` | `hour_files()`, `write_hour()`, `load_day()`, and the command line (`<start-date> --days N`, `load-day <date>`) |
| `pagelake/gold.py` | `build_gold()` and the command line |
| `pagelake/iceberg_table.py` | `get_catalog()`, `day_arrow()`, `create_table()`, `append_day()`, the `snapshots`, `add-column` and `time-travel` commands, `count_day()`, `replace_day()` |
| `pagelake/compact.py` | `compact_day()` and the command line |
| `tests/test_land.py`, `tests/test_silver.py` | The tests of `bronze_key()` and `hour_files()`, skipped until you write them |
| `sql/*.sql` | One file per query, each with a header and a TODO. `sql/not_articles.csv` holds only its header `lang,title` |
| `docs/*.md` | `partitioning.md`, `findings.md`, `table-format.md`, `compaction.md`, `rerun.md`, with their headings and a TODO |

PyIceberg is not installed yet: task 11 adds it with `uv add "pyiceberg[pyarrow,sql-sqlite]"`. There is no `README.md`: you write it in the wrap-up. `evidence.md`, `AI_LOG.md` and `EXPLAIN.md` live in the task folder, next to `pagelake/`. The starter holds no data.

## Copy it in

In task 8 (Land one week of hourly pageview files in a bronze bucket), run this in Git Bash inside the task folder instead of step 1:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p05-pagelake pagelake
cd pagelake
uv sync
cp .env.example .env
```

Step 2 is done for you. Carry on from step 3: replace `<your-id>` in `.env` and make the bucket. In task 9, steps 1 (`connect()`) and 8 (`query.py`) are done for you: read both files, then write the rest. When a step says "add a command", it is already in the command line: write the function it calls.

From task 9 on, copy your `pagelake/` folder forward as each brief says, without `.venv/` and `data/`.

## How to run it

In `pagelake/`, with the S3 emulator running (`docker compose --profile storage up -d` in `~/de-kit/datalab`):

```bash
uv sync
uv run pytest -q              # every test is skipped until you write it
uv run ruff check
uv run --env-file .env python -m pagelake.land data/raw
```

The last command stops with `NotImplementedError: TODO(task 8): write bronze_key()` or `land()`: that is where you start. `python -m pagelake.query sql/q1_one_day.sql` says the file holds no SQL yet; on an empty bucket it says no files were found. When you write a test, remove its `@pytest.mark.skip` line.

## The TODOs

Search for them with `grep -rn "TODO(task" .` in `pagelake/`.

| Task | File | What you write |
|---|---|---|
| 8 | `pagelake/land.py` | `bronze_key()`, `land()` |
| 8 | `tests/test_land.py` | two tests of `bronze_key()` |
| 9 | `pagelake/silver.py` | `hour_files()`, `write_hour()` |
| 9 | `tests/test_silver.py` | two tests of `hour_files()` |
| 9 | `sql/q1_one_day.sql`, `sql/q2_one_language.sql`, `sql/make_by_lang.sql` | the queries and the second layout |
| 9 | `docs/partitioning.md` | your measurements and your choice |
| 10 | `sql/look_top_titles.sql`, `sql/gold_top_pages.sql`, `sql/gold_views_by_language.sql` | the look and the two gold queries |
| 10 | `pagelake/gold.py` | `build_gold()` |
| 10 | `docs/findings.md` | your findings |
| 11 | `pagelake/iceberg_table.py` | `get_catalog()`, `day_arrow()`, `create_table()`, `append_day()`, `snapshots()`, `add_column()`, `time_travel()` |
| 11 | `docs/table-format.md` | what Iceberg added |
| 12 | `sql/q3_day_total.sql` | the day total |
| 12 | `pagelake/compact.py` | `compact_day()` |
| 12 | `docs/compaction.md` | before and after |
| 13 | `pagelake/silver.py` | `load_day()` |
| 13 | `pagelake/iceberg_table.py` | `count_day()`, `replace_day()` |
| 13 | `sql/q4_day_total.sql` | a copy of q3 for 2026-11-04 |
| 13 | `docs/rerun.md` | why the re-run is safe |

`sql/not_articles.csv` (task 10) is yours to fill: a CSV file cannot hold a TODO line. Task 14, the wrap-up, has no TODO: `pagelake/README.md`, the screenshots and `EXPLAIN.md` are yours from the start.

## What you still write yourself

- Every function marked TODO, every SQL query and every test.
- The non-article list, the documents in `docs/`, and your own `.env` (never committed).
- The commands' evidence in `evidence.md`, the AI move's entry in `AI_LOG.md`, and `EXPLAIN.md` without AI.
