# Guided starter: P6 PageLake part 2 (add-on)

This starter is an **add-on** to the `pagelake/` folder you built in P5. It adds only the new files of module 8 (Airflow runs PageLake), at their places inside `pagelake/`. It never replaces a P5 file: your `lake.py`, `silver.py`, `gold.py`, tests and SQL stay as they are. It saves you the set-up: the DAG files with their settings and task names, the function signatures and docstrings, the SQL file headers, the test files and the runbook headings. Every function body, query, test, the DAG wiring and the reliability settings are still yours.

## What is included

| Path in `pagelake/` | What it is |
|---|---|
| `dags/pagelake_hello.py` | Your first DAG (task 8): the imports, three function stubs, and TODOs for the decorators, the wiring and the call |
| `dags/pagelake_daily.py` | The daily DAG (tasks 10-12): the imports, `@dag` with its schedule, start date and `catchup=False`, four `@task` stubs, and TODOs for the wiring, `max_active_runs` and the retry and alert settings |
| `pagelake/steps.py` | `LANGS`, `MissingHour`, `data_dir()` and the command line, complete; stubs of `missing_hours()`, `land_day()`, `silver_path()`, `check_language()` |
| `pagelake/alerts.py` | The stub of `send_alert(context)` |
| `pagelake/freshness.py` | `PROMISE_DAYS`, the `--today` option, and stubs of `status()` and the rest of `main()` |
| `sql/day_counts.sql`, `sql/duplicates.sql`, `sql/freshness.sql` | Headers and TODOs, no SQL yet. Each reads `FROM {silver}`, as P5's query files do |
| `tests/test_steps.py`, `tests/test_freshness.py` | Skipped tests with a docstring each. They make their own files in `tmp_path`: no fixtures, no bucket |
| `RUNBOOK.md` | The six headings of the runbook |
| `STARTER-P6.md` | This file. It is not your README |

There is no `compose.yaml`: task 8 step 3 copies it from the kit. There is no data: `data/raw/` comes from `get_hours.py` (task 8 step 2).

## Copy it in (task 8)

Task 8 says: "Guided level: copy the contents of `starters/p06-pagelake` into `pagelake/`; it only adds new files." First copy your own `pagelake/` folder forward (the first line of "Before you start"). Then, in Git Bash, inside task 8's folder:

```bash
git -C ~/de-kit pull
cp -rn ~/de-kit/starters/p06-pagelake/. pagelake/
```

`-n` never overwrites a file you already have, and `/.` copies every file of the starter, hidden ones too. Check with `ls pagelake/dags pagelake/pagelake`. Copy the starter only once: from task 9 on, copy your `pagelake/` folder forward as each brief says.

Fell behind in P5? Your mentor gives you a catch-up copy of `pagelake/` first; then copy this starter into it the same way.

## Lines you add to your own files

The starter cannot change your P5 files. The briefs ask for these lines:

| Task | File | Add |
|---|---|---|
| 8, step 1 | `NEXT.md` | `## Part 2` and one line |
| 9, step 1 | `.env.example` and `.env` | `PAGELAKE_DATA_DIR=data` |
| 12, step 1 | `.env.example` | `PAGELAKE_ALERT_WEBHOOK=` (empty) |
| 12, step 1 | `.env` (never committed) | `PAGELAKE_ALERT_WEBHOOK=<your webhook address>` |

`pyproject.toml` does not change: the DAGs need only `duckdb` and `boto3` inside Airflow, and the kit's `compose.yaml` installs them.

## Steps the starter has done

- Task 8, step 5: the imports. You still write `@dag`, the three `@task` functions, the wiring and the call.
- Task 9, step 2 (`LANGS`, `MissingHour`, `data_dir()`) and step 8 (the `__main__` command line, which only calls your functions).
- Task 10, steps 1 and 2: the imports and the `@dag` settings.
- Task 14, step 4: the `--today` option. You still write how `main()` picks today.

## How to run it

In `pagelake/`:

```bash
uv run pytest -q              # your P5 tests pass; the new ones are skipped until you write them
uv run ruff check
docker compose exec airflow airflow dags list-import-errors     # with Airflow running (task 8)
```

`list-import-errors` prints `No data found` straight after the copy: the DAG files import cleanly, and define no DAG until you write the call at the end. `uv run --env-file .env python -m pagelake.steps 2026-11-05` stops with `NotImplementedError: TODO(task 9): write land_day()`: task 9 starts with `missing_hours()`, which `land_day()` uses. When you write a test, remove its `@pytest.mark.skip` line.

## The TODOs

Search for them with `grep -rn "TODO(task" .` in `pagelake/`.

| Task | File | What you write |
|---|---|---|
| 8 | `dags/pagelake_hello.py` | `@dag`, three `@task` decorators, `count_raw()`, `count_bronze()`, `report()`, the wiring and the call |
| 9 | `pagelake/steps.py` | `missing_hours()`, `land_day()`, `silver_path()`, `check_language()` |
| 9 | `tests/test_steps.py` | Three tests: the end-of-hour file, a clean file, a repeated row |
| 10 | `dags/pagelake_daily.py` | The bodies of `land`, `rebuild_silver`, `check` and `rebuild_gold`, the fan-out and fan-in, and the call |
| 11 | `dags/pagelake_daily.py` | One active run at a time |
| 11 | `sql/day_counts.sql`, `sql/duplicates.sql` | The two checks |
| 12 | `pagelake/alerts.py` | `send_alert(context)` |
| 12 | `dags/pagelake_daily.py` | The two imports, `on_failure_callback` and `default_args` |
| 14 | `sql/freshness.sql` | The newest complete day |
| 14 | `pagelake/freshness.py` | `status()` and the rest of `main()` |
| 14 | `tests/test_freshness.py` | Three tests: 1 day old, 2 days old, no complete day |
| 14 | `RUNBOOK.md` | Every section |

Task 13 has no TODO, on purpose: its brief expects no code change, because the same DAG fills the past when its tasks read their day from the run. Task 15 is the wrap-up: `pagelake/README.md`, `docs/screenshots/` and `EXPLAIN.md` are yours.

## What you still write yourself

- Every function body, query and test in the table above, the DAG wiring and the retry and alert settings.
- The lines in "Lines you add to your own files", and your own `.env` (never committed).
- `evidence.md` in each task folder, `AI_LOG.md` (task 11), and in the wrap-up `pagelake/README.md` for both parts, `docs/screenshots/` and `EXPLAIN.md` without AI.

## Data and licence

This starter holds no data. Page-view data: Wikimedia Foundation (CC0 1.0), downloaded by the kit's `data/pageviews/get_hours.py` into your `data/raw/`.
