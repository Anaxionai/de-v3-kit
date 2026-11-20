# Guided starter: P4 ClearAir

This folder is the start of your `clearair/` product folder for module 6 (ingestion and packaging). It saves you the set-up: the uv project and its lock file, the settings file, the package with every function's name and docstring, the test files, and the configuration files with a TODO that says what goes in them. Every function body, query, test and configuration is still yours to write.

## What is included

| Path | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A uv project for Python 3.12 with `httpx` and `psycopg[binary]`, and `pytest` and `ruff` for development. `pythonpath = ["."]` is set for the tests |
| `.env.example` | Every setting of the module, with an empty key. `CLEARAIR_FAIL_AFTER_CALLS` is only a comment |
| `clearair/settings.py` | `load_settings()` |
| `clearair/client.py` | `ApiError`, `get_json`, `find_sensors`, `save_page`, `fetch_pages`, `summarise_pages` |
| `clearair/load.py` | `ensure_schema`, `rows_from_page`, `upsert_readings` |
| `clearair/watermark.py` | `read_watermark`, `write_watermark`, `window_start`, `next_watermark` |
| `clearair/retry.py` | `is_retryable`, `call_with_retries` |
| `clearair/stationdb.py` | `upsert_stations`, `full_load`, `incremental_load`, `find_deleted`, `mark_deleted` |
| `clearair/cli.py` | The command line, complete: `load-api` (`--until`, `--raw`) and `load-stations` (`--full`). The two commands' bodies are yours |
| `sql/schema.sql`, `sql/checks.sql` | Headers and TODOs for the tables and the checks |
| `tests/` | One test file per task, every test skipped until you write it; `conftest.py` reads the fixtures |
| `tests/fixtures/` | A hand-made `/v3/locations` page and a `/v3/sensors/<id>/hours` page, shaped like the API's answers |
| `Dockerfile`, `.dockerignore`, `compose.yaml`, `.gitignore`, `.github/workflows/tests.yml`, `k8s/cronjob.yaml` | Comments and a TODO only |

There is no `README.md`: you write it in the wrap-up. `evidence.md`, `AI_LOG.md` and `EXPLAIN.md` live in the task folder, next to `clearair/`. The fixtures are made up (no real station or reading), so they need no credit.

## Copy it in

In task 8 (Call the air-quality API for one city and save the raw pages), run this in Git Bash inside the task folder instead of step 1:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p04-clearair clearair
cd clearair
uv sync
cp .env.example .env
```

Step 2 is done for you: `.env.example` already lists the task 8 settings and those of tasks 10, 11 and 21. Carry on from step 3 (fill in `.env`). When a later step says "add X to `.env` and `.env.example`", check that it is in your `.env`. When a step says "add the option" or "add the command", it is already in `cli.py`: write what it does.

From task 9 on, copy your `clearair/` folder forward as each brief says, without `.venv/` and `data/`.

## How to run it

In `clearair/`:

```bash
uv sync
uv run pytest -q          # every test is skipped until you write it
uv run ruff check
uv run --env-file .env python -m clearair.cli --help
uv run --env-file .env python -m clearair.cli load-api
```

The last command stops with `NotImplementedError: TODO(task 8): write the load-api command`: that is where you start. When you write a test, remove its `@pytest.mark.skip` line.

## The TODOs

Search for them with `grep -rn "TODO(task" .` in `clearair/`.

| Task | File | What you write |
|---|---|---|
| 8 | `clearair/settings.py` | `load_settings()` |
| 8 | `clearair/client.py` | `ApiError`, `get_json()`, `find_sensors()`, `save_page()` |
| 8 | `clearair/cli.py` | the `load-api` command |
| 9 | `clearair/client.py` | `fetch_pages()`, `summarise_pages()`, every page of `/locations` |
| 9 | `clearair/cli.py` | every page of each sensor, and the log per sensor |
| 9 | `tests/test_client.py` | four tests of `fetch_pages()` |
| 10 | `sql/schema.sql` | the `readings` table |
| 10 | `clearair/load.py` | `ensure_schema()`, `rows_from_page()`, `upsert_readings()` |
| 10 | `clearair/cli.py` | one transaction per sensor, and `--raw` |
| 10 | `tests/test_load.py` | two edge-case tests from the AI move |
| 11 | `sql/schema.sql` | the `load_state` table |
| 11 | `clearair/watermark.py` | all four functions |
| 11 | `clearair/cli.py` | the window from the watermark, and `--until` |
| 11 | `tests/test_watermark.py` | four tests |
| 12 | `clearair/retry.py` | `is_retryable()`, `call_with_retries()` |
| 12 | `clearair/client.py` | the `CLEARAIR_FAIL_AFTER_CALLS` practice switch |
| 12 | `clearair/cli.py` | every `get_json()` call wrapped in `call_with_retries()` |
| 12 | `tests/test_retry.py` | three tests |
| 13 | `sql/checks.sql` | three check queries |
| 21 | `sql/schema.sql` | the `stations` table |
| 21 | `clearair/stationdb.py` | `upsert_stations()`, `full_load()`, `incremental_load()` |
| 21 | `clearair/cli.py` | the `load-stations` command |
| 22 | `clearair/stationdb.py` | `find_deleted()`, `mark_deleted()` |
| 22 | `clearair/cli.py` | `mark_deleted()` at the end of `load-stations` |
| 22 | `tests/test_stationdb.py` | three tests |
| 23 | `Dockerfile`, `.dockerignore` | the image and its ignore list |
| 24 | `compose.yaml` | the services `db` and `loader` |
| 25 | `.github/workflows/tests.yml`, `.gitignore` | the workflow and the ignore list |
| 26 | `k8s/cronjob.yaml` | the CronJob `clearair-load` |

Task 27, the wrap-up, has no TODO: `clearair/README.md`, the screenshots in `clearair/docs/` and `EXPLAIN.md` are yours from the start.

## What you still write yourself

- Every function body, every SQL statement and every test.
- The `Dockerfile`, `.dockerignore`, `compose.yaml`, the workflow, `.gitignore` and the CronJob.
- Your own `.env` (never committed) and the commands' evidence in `evidence.md`.
- The AI move's entry in `AI_LOG.md`, and `EXPLAIN.md` without AI.
