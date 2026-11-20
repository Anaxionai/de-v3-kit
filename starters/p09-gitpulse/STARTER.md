# Guided starter: P9 GitPulse

This folder is the start of your `gitpulse/` product folder for module 11 (Snowflake and dbt). It saves you the set-up: one SQL file per step, with its header and TODOs, and a dbt project skeleton with the profile, the source file and an empty file for every model, macro, test and snapshot the module builds. Every statement, grant, model, macro and test is still yours to write.

## What is included

| Path | What it is |
|---|---|
| `snowflake/01_monitor.sql` … `16_teardown.sql`, `99_export_ddl.sql` | One file per step of tasks 8 to 13, 26 and 27: what it is for, which role runs it, the object names, and TODOs. No statements |
| `sql/q01_top_merged.sql`, `sql/q02_name_on_date.sql` | The questions of tasks 22 and 25 |
| `docs/model.md` | Headings for the grain and the Mermaid diagram (task 22) |
| `.github/workflows/dbt-ci.yml` | The outline of the CI workflow (task 26) |
| `dbt/dbt_project.yml` | What `dbt init gitpulse` writes, without the `example` lines |
| `dbt/profiles.yml`, `dbt/.env.example`, `dbt/.gitignore` | Profile `gitpulse` with targets `dev` and `ci`; the three variable names; `target/`, `logs/`, `dbt_packages/`, `.env` ignored |
| `dbt/models/`, `dbt/macros/`, `dbt/tests/`, `dbt/snapshots/` | One file per model, macro, test and snapshot, each holding only comments and TODOs |
| `.python-version` | Python 3.12, so `uv` uses it from task 20 |
| `.gitignore` | Keeps `data/` (the downloaded hours) and `.venv/` out of Git |

There is no `pyproject.toml` on purpose: task 20 step 1 makes it with `uv init --bare`, which refuses to run where one exists. `evidence.md` lives in the task folder, next to `gitpulse/`. You write `gitpulse/README.md` in task 28.

## Copy it in

In task 8 (Open the trial, set a resource monitor and auto-suspend, and create roles), start from this starter instead of an empty folder. In Git Bash, inside the task folder:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p09-gitpulse gitpulse
ls -A gitpulse    # .github .gitignore .python-version STARTER.md dbt docs snowflake sql
```

From task 9 on, copy your `gitpulse/` folder forward as each brief says.

## How to run it

**Snowflake files (tasks 8 to 13, 26, 27).** Run `01` to `03`, `13` and `16` in a Snowsight worksheet with the role the file's header names. Run the others from `gitpulse/`:

```bash
snow sql -f snowflake/04_raw_events.sql
```

A file that still holds only its TODOs has no statement in it, so there is nothing to run yet.

**dbt (from task 20).** In task 20, run step 1 as written, then skip steps 2 and 3: the starter's `dbt/` already holds `dbt_project.yml`, `profiles.yml` and `.env.example`. Fill in their TODOs instead, then carry on from step 4.

```bash
cd gitpulse
uv init --bare --python 3.12
uv add dbt-core dbt-snowflake     # pin both to the versions in ~/de-kit/VERSIONS.md
cd dbt
cp .env.example .env              # fill in your three values; Git ignores .env
uv run --env-file .env dbt debug
```

Every model file holds only comments until you write it, and dbt builds only what you select. `models/intermediate/int_github__repository_names.sql` starts with `{{ config(enabled=false) }}`, so the `dbt build` of task 23 skips it; task 25 tells you to delete that line.

Until task 21 adds the folder configs, dbt warns `Custom key gitpulse found in config` about the empty `models: gitpulse:` block in `dbt_project.yml`. The warning is harmless and goes away then.

## Your TODOs

Find them with `grep -rn "TODO(task" gitpulse`.

| Task | File | What you write |
|---|---|---|
| 8 | `snowflake/01_monitor.sql` | The resource monitor, set on the account |
| 8 | `snowflake/02_warehouse_database.sql` | `GITPULSE_WH`, `GITPULSE` and its four schemas; `COMPUTE_WH` auto-suspend |
| 8 | `snowflake/03_roles.sql` | The three roles and every grant |
| 9 | `snowflake/04_raw_events.sql` | File format, stage and `RAW.EVENTS` |
| 9 | `snowflake/05_copy_events.sql` | The `COPY INTO` with the metadata columns |
| 9 | `snowflake/06_load_checks.sql` | Load checks and `COPY_HISTORY` |
| 10 | `snowflake/07_typed_tables.sql` | `RAW.PUSHES`, `RAW.PULL_REQUESTS`, `RAW.STARS` |
| 10 | `snowflake/08_typed_checks.sql` | Count checks and the `LATERAL FLATTEN` commits check |
| 11 | `snowflake/09_stream_and_task.sql` | The stream, and the task with one `INSERT ALL` |
| 12 | `snowflake/10_three_ways.sql`, `11_query_costs.sql` | The tag, the plans, three ways, the history query |
| 13 | `snowflake/12_time_travel_and_clone.sql` | Drop, `UNDROP`, clone, test, drop the clone |
| 20 | `dbt/profiles.yml` | The `env_var()` lines and the two databases |
| 20 | `dbt/models/staging/_github__sources.yml` | Source `github`, descriptions, freshness |
| 21 | `dbt/dbt_project.yml` | Folder configs for `staging` and `marts` |
| 21 | `dbt/macros/generate_schema_name.sql`, `clean_actor.sql` | The two macros |
| 21 | `dbt/models/staging/stg_github__*.sql` (four files) | The staging models |
| 22 | `dbt/dbt_project.yml` | Folder config for `intermediate` |
| 22 | `dbt/models/intermediate/int_github__activity_unioned.sql` | The union of the three activity types |
| 22 | `dbt/models/marts/fct_daily_activity.sql`, `dim_repository.sql`, `dim_actor.sql` | The fact and the two dimensions |
| 22 | `dbt/models/marts/_marts__models.yml` | The grain sentence |
| 22 | `sql/q01_top_merged.sql`, `docs/model.md` | The question; the grain and the `erDiagram` |
| 23 | `dbt/models/marts/_marts__models.yml` | Descriptions and tests |
| 23 | `dbt/models/staging/_github__sources.yml` | The `accepted_values` test on `action` |
| 23 | `dbt/tests/assert_fct_daily_activity_grain.sql` | The grain test |
| 24 | `dbt/models/marts/fct_daily_activity.sql` | Incremental config, `changed_days` and its filter |
| 25 | `dbt/models/intermediate/int_github__repository_names.sql` | The names model (and remove the disable line) |
| 25 | `dbt/snapshots/repository_names.yml`, `sql/q02_name_on_date.sql` | The snapshot; the name on a date |
| 26 | `snowflake/13_ci_user.sql`, `14_ci_clone.sql`, `15_ci_drop.sql` | The CI user, the clone, the drop |
| 26 | `.github/workflows/dbt-ci.yml` | The workflow's env and steps |
| 27 | `snowflake/16_teardown.sql`, `99_export_ddl.sql` | The teardown; the exported DDL |

Task 28 (the wrap-up) has no TODO: the README, the demo and `EXPLAIN.md` are all yours.

## What you still write yourself

- Every SQL statement and grant, every dbt model, macro, test, source and snapshot, and the CI steps.
- `pyproject.toml` and `uv.lock` (task 20), and your own `dbt/.env`.
- `evidence.md`, `AI_LOG.md`, `TEST_REVIEW.md` and `EXPLAIN.md` in the task folders, and `gitpulse/README.md` (task 28).

Keys stay in `~/snowflake-keys/`, outside every repository. No key, password or account secret goes in any file in this folder.

The data comes from [GH Archive](https://www.gharchive.org/); the kit script downloads it into `gitpulse/data/`, which Git ignores. This starter holds no data.
