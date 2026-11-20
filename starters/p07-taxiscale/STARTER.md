# Guided starter: P7 TaxiScale

This folder is the start of your `taxiscale/` product folder for module 9 (Spark and Databricks). It saves you the set-up: the uv project with the test settings, the `jobs/` package with every function's name and docstring, a ready SparkSession fixture for the tests, the test file, the SQL files with their headers and `docs/plans.md` with the headings the briefs name. Every cleaning rule, join, aggregation, plan reading and fix is still yours.

## What is included

| Path | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | What `uv init --bare --python 3.12` makes, plus `[tool.pytest.ini_options]` with `pythonpath = ["."]` and `testpaths = ["tests"]`. No libraries: Spark and pytest live in the kit's Spark container |
| `jobs/__init__.py` | Empty: it makes `jobs` a package the tests can import |
| `jobs/read_month.py` | `main()` |
| `jobs/clean.py` | `clean_trips(df, months)` and `main()` (`--month`) |
| `jobs/join_aggregate.py` | `read_zones()`, `join_zones()`, `daily_zone_totals()`, `salted_join()` and `main()` |
| `jobs/skew.py` | `top_keys()`, `partition_sizes()` and `main()` |
| `sql/daily_zone.sql` | Header and TODO: the Spark SQL version, over the temporary views `trips` and `zones` |
| `sql/catalog.sql`, `docs/catalog.md` | Header, headings and TODOs for the catalog task |
| `tests/conftest.py` | **Complete.** A session-scoped `spark` fixture with `master("local[1]")` |
| `tests/test_clean.py` | Five tests of `clean_trips()`, skipped until you write them |
| `docs/plans.md` | The headings of tasks 11, 12 and 13, each with a TODO |

There is no `compose.yaml`: task 8 step 1 copies it from the kit, so there is only one copy of it. There is no `notebooks/` folder and no `changes/` folder: you make those on Databricks in tasks 21 to 26. There is no `README.md`: you write it in the wrap-up. `evidence.md`, `AI_LOG.md` and `EXPLAIN.md` live in the task folder, next to `taxiscale/`. The starter holds no data.

The jobs and tests run inside the kit's Spark image, whose Python is 3.10. Keep your code to Python 3.10 features.

## Copy it in

In task 8 (Start Spark in Docker and read one month of trips), run this in Git Bash inside the task folder instead of making the folder by hand:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p07-taxiscale taxiscale
cp ~/de-kit/datalab/spark/compose.yaml taxiscale/compose.yaml
cd taxiscale
```

That covers steps 1 and 2. Carry on from step 3 (download the month). In task 9, step 1 (the pytest settings) and step 6 (`tests/conftest.py`) are done for you.

From task 9 on, copy your `taxiscale/` folder forward as each brief says. Never commit `data/`.

## How to run it

In `taxiscale/`, with Spark running (`docker compose --profile lite up -d`):

```bash
docker compose exec spark python3 -m pytest -q          # every test is skipped until you write it
docker compose exec spark spark-submit jobs/read_month.py
```

The tests need the container: your laptop's Python has no Spark. The job stops with `NotImplementedError: TODO(task 8): write main()`: that is where you start. If Git Bash says "the input device is not a TTY", add `-T` after `exec`. When you write a test, remove its `@pytest.mark.skip` line.

## The TODOs

Search for them with `grep -rn "TODO(task" .` in `taxiscale/`.

| Task | File | What you write |
|---|---|---|
| 8 | `jobs/read_month.py` | `main()` |
| 9 | `jobs/clean.py` | `clean_trips()`, `main()` |
| 9 | `tests/test_clean.py` | five tests |
| 10 | `jobs/join_aggregate.py` | `read_zones()`, `join_zones()`, `daily_zone_totals()`, `main()` |
| 10 | `sql/daily_zone.sql` | the Spark SQL version |
| 11 | `jobs/join_aggregate.py` | `explain("formatted")` in `main()` |
| 11 | `docs/plans.md` | the plan, the shuffles, the stages, what you learned |
| 12 | `jobs/join_aggregate.py` | `--join sortmerge|broadcast` |
| 12 | `docs/plans.md` | the two plans and `## Why` |
| 13 | `jobs/skew.py` | `top_keys()`, `partition_sizes()`, `main()` |
| 13 | `jobs/join_aggregate.py` | `salted_join()` and `--join salted` |
| 13 | `docs/plans.md` | `## Skew` |
| 27 | `sql/catalog.sql`, `docs/catalog.md` | the reports schema, the view, the grants and the diagram |

Tasks with no TODO, and why:

- Tasks 21 to 26 happen on Databricks. Their files are notebooks you export from your workspace (`notebooks/taxiscale_setup.py`, `taxiscale_daily.py`, `taxiscale_merge.py`, `taxiscale_table_care.py`) and the change batch `changes/change_batch_01.csv`, built from your own table. A starter copy would be a wrong copy.
- Task 28, the wrap-up: `taxiscale/README.md`, the screenshots and `EXPLAIN.md` are yours from the start.

## What you still write yourself

- Every function marked TODO, `sql/daily_zone.sql` and the five tests.
- `docs/plans.md` and `docs/catalog.md`, from your own plans and numbers.
- The Databricks notebooks and the change batch.
- The commands' evidence in `evidence.md`, the AI move's entry in `AI_LOG.md`, and `EXPLAIN.md` without AI.
