# Guided starter: P13 CareLine

This folder is the start of your `careline/` product folder for module 15 (quality, contracts, privacy and incidents). It saves you the set-up: the uv project, the folder layout, the database connection, the function signatures, the SQL and check files with their headers, the contract's outline and the document headings. Every query, check, suite, rule and answer is still yours to write.

## What is included

| File | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | The uv project: Python 3.12, `pandas`, `psycopg[binary]`, `great_expectations` and `pyyaml`, plus `pytest` and `ruff` for development. `pythonpath = ["."]` is set for pytest |
| `.gitignore` | Complete: keeps `data/`, `.env`, `.venv/` and caches out of Git |
| `.env.example` | Complete: `_PIP_ADDITIONAL_REQUIREMENTS` for Airflow and the placeholder `CARELINE_SALT=change-me` |
| `careline/db.py` | `connect()` and `python -m careline.db <file>` complete; `run_sql_file()` is a stub |
| `careline/load.py` | `day_path()` complete; `load_reference()`, `load_day()`, `set_salt()` and `main()` are stubs |
| `careline/quality.py` | Stubs of the two suites, `validate_day()`, `save_results()`, `check_file_present()` and `validate_frame()` |
| `careline/contract.py` | Stubs of `load_contract()`, `check_header()` and `contract_suite()` |
| `dags/careline_daily.py` | The imports, the `@dag` settings and five task stubs; the order and the call are TODOs |
| `sql/*.sql`, `checks/*.sql` | One file per statement group the tasks grade: a header comment and a TODO, no SQL yet |
| `checks/rules.md`, `docs/privacy.md` | Table headers only |
| `contracts/appointments.yaml` | The ODCS keys, empty, and a commented example property |
| `contracts/README.md`, `docs/lineage.md`, `INCIDENT.md` | Headings only |
| `tests/test_contract.py`, `tests/test_quality.py` | Skipped tests with a docstring each |

There is no `compose.yaml` (task 9 copies the kit's Airflow file), no `sample/` (task 10 copies the generated samples) and no `.github/workflows/` (you write the workflow in task 12).

## Copy it in (task 8)

Task 8 says "start from `starters/p13-careline` instead of an empty folder". In Git Bash, inside the task folder:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p13-careline careline
cd careline
uv sync
```

Then follow task 8 from step 2: `uv sync` replaces step 1's `uv init` and `uv add`. From task 9 on, copy your `careline/` folder forward as each brief says, then make the data again with `make_clinic.py` and the same `--end` day.

Later steps that the starter has already done for you: `uv add great_expectations` (task 9, step 1) and `uv add --dev pytest` with `pythonpath` (task 10, step 8) change nothing, and `.env.example` already has the lines of task 9, step 9 and task 11, step 2. Still create your own `.env` (`cp .env.example .env`, then your real salt in task 11).

## How to run it

In `careline/`, with the data lab's core profile running (`docker compose --profile core up -d` in `~/de-kit/datalab`):

```bash
uv run pytest -q                                    # every test is skipped until you write it
uv run ruff check                                   # lint
uv run python -m careline.db sql/00_raw.sql         # run a SQL file (once run_sql_file() works)
uv run python -m careline.load --all                # load every day (once load.py works)
docker compose --profile lite up -d                 # Airflow, after you copied compose.yaml (task 9)
docker compose exec airflow airflow dags test careline_daily <day>
```

Inside Airflow the product folder is `/opt/airflow/project` and the working folder is somewhere else. That is why `db.py` builds every path from `PRODUCT_DIR` (`Path(__file__).resolve().parents[1]`): keep doing the same.

## Your TODOs

Find them with `grep -rn "TODO(task" .` in `careline/`.

| Task | File | What you write |
|---|---|---|
| 8 | `careline/db.py` | `run_sql_file()` |
| 8 | `careline/load.py` | `load_reference()`, `load_day()`, `main()` with `--all` |
| 8 | `sql/00_raw.sql`, `checks/profile.sql`, `checks/rules.md` | The raw tables, the profile, at least 8 rules |
| 9 | `careline/quality.py` | `blocking_suite()`, `warning_suite()`, `save_results()`, `validate_day()`, `check_file_present()` |
| 9 | `sql/01_layers.sql`, `sql/clean.sql`, `sql/report.sql` | The clean and report layers, and the per-day rebuilds |
| 9 | `dags/careline_daily.py` | `load_raw`, `check_raw`, `build_clean`, `build_report`, their order and the call |
| 10 | `careline/contract.py` | `load_contract()`, `check_header()`, `contract_suite()` |
| 10 | `careline/load.py`, `dags/careline_daily.py` | `check_header()` in `load_day()`, the contract suite in `check_raw` |
| 10 | `contracts/appointments.yaml`, `contracts/README.md` | The contract, and its safe and breaking changes |
| 10 | `tests/test_contract.py` | Three tests on the samples |
| 11 | `careline/load.py` | `set_salt()` and `--set-salt` |
| 11 | `sql/masking.sql`, `sql/roles.sql`, `sql/01_layers.sql`, `checks/pii_scan.sql` | Masking, the analyst role, the new clean tables, the scan |
| 11 | `dags/careline_daily.py`, `docs/privacy.md` | `check_privacy` and its place in the order, the column table |
| 12 | `careline/quality.py`, `tests/test_quality.py` | `validate_frame()`, two tests on the samples |
| 13 | `sql/trace_revenue.sql`, `docs/lineage.md` | The trace and the two diagrams |
| 14 | `INCIDENT.md` | The report, and one prevention change in your code |

Task 12's workflow file has no stub: write `.github/workflows/data-tests.yml` from its brief, as for ClearAir in P4. Task 15 is the wrap-up.

## What you still write yourself

- Every function body, query, suite, test and document in the table above.
- `sample/` (task 10), `.github/workflows/data-tests.yml` (task 12) and your `.env` with the real salt (task 11).
- `AI_LOG.md` (task 8), `evidence.md` in each task folder, and in the wrap-up `careline/README.md`, the screenshots and `EXPLAIN.md`.

## Data and licence

This starter holds no data. The kit's `data/clinic/make_clinic.py` makes a clinic's data for your student id: every name, phone number and email is made up. Keep `data/` out of Git all the same, and treat it as personal data.
