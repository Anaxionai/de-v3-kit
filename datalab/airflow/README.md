# Airflow for one product

`compose.yaml` in this folder runs Apache Airflow 3 for one product. The course uses it in P6 PageLake part 2 and P13 CareLine.

| Profile | What runs | For |
|---|---|---|
| `lite` | One container, `airflow`: the web page, scheduler, DAG processor and triggerer together (`airflow standalone`), with the local executor and a small SQLite database | 8 GB laptops |
| `full` | Each part in its own container, with PostgreSQL as Airflow's database and the local executor | 16 GB laptops |

Run every command in Git Bash, with Docker Desktop running. The examples use PageLake; for CareLine, read `careline` where they say `pagelake`.

## 1. Copy the file into your product folder

Inside your task folder:

```bash
cp ~/de-kit/datalab/airflow/compose.yaml pagelake/compose.yaml      # P6; for P13: careline/compose.yaml
cd pagelake
```

Airflow expects this layout in the product folder (the folder that holds `compose.yaml`):

```text
pagelake/
  compose.yaml        the copy of this kit file
  .env                your settings (never committed); .env.example is committed
  dags/               your DAG files
  pagelake/           your Python package, with __init__.py
  sql/                SQL files your code reads
  data/raw/           data files (ignored by Git)
```

## 2. Start Airflow

Start the data lab profile your product needs first: `storage` (the S3 emulator) for PageLake, `core` (PostgreSQL) for CareLine. Then, in the product folder:

```bash
docker compose --profile lite up -d
docker compose --profile lite ps
```

The first start downloads the Airflow image once (about 700 MB). Every start then installs the extra Python packages (step 5), so Airflow needs about 30 to 90 seconds. Run `ps` again until the service `airflow` shows STATUS `Up` and then `(healthy)`.

On a 16 GB laptop you may use `--profile full` in every command instead.

## 3. The web page and sign-in

Open http://localhost:8080 and sign in:

| User | Password |
|---|---|
| `airflow` | `airflow` |

This password works only on your laptop. Never use it on a real server.

## 4. Your DAGs, your package and the working folder

Your whole product folder is mounted inside the container at `/opt/airflow/project`, and that folder is the container's **working folder**:

| On your laptop | Inside the container |
|---|---|
| `pagelake/` | `/opt/airflow/project`, the working folder |
| `pagelake/dags/` | `/opt/airflow/project/dags`, Airflow's DAG folder |
| `pagelake/pagelake/steps.py` | `/opt/airflow/project/pagelake/steps.py` |
| `pagelake/sql/` | `/opt/airflow/project/sql` |
| `pagelake/data/raw/` | `/opt/airflow/project/data/raw` |

So a relative path behaves as it does on your laptop when you run commands in the product folder: `sql/gold_top_pages.sql`, `read_csv('sql/not_articles.csv')` and `data/raw` work in a task and in `dags test`, with no change to your code. Check it with `docker compose exec airflow pwd`: it prints `/opt/airflow/project`.

`/opt/airflow/project` is also on `PYTHONPATH`, so a DAG imports your package as usual:

```python
from airflow.sdk import dag, task
from airflow.sdk.exceptions import AirflowFailException, AirflowSkipException

from pagelake import lake, steps
```

- Airflow looks for new DAG files every 30 seconds. A new DAG appears paused: unpause it on the web page or with the command in step 7.
- A DAG that does not appear has an import error. See it with `docker compose exec airflow airflow dags list-import-errors`. With no errors it prints `No data found`.
- A DAG file defines a DAG only when it calls the decorated function at the end, such as `pagelake_daily()`.

## 5. Settings, `.env` and extra Python packages

When your product folder has a `.env` file, Compose loads every line of it into the container, so your DAG code reads them with `os.environ` (PageLake's `lake.py` reads `PAGELAKE_BUCKET` and the `AWS_...` keys this way). If the file does not exist, Airflow starts without it.

A few settings in `compose.yaml` win over the same names in `.env`, because inside the container `localhost` is the container itself:

| Setting | Inside the container | For |
|---|---|---|
| `working_dir` | `/opt/airflow/project` (step 4) | every product |
| `AWS_ENDPOINT_URL` | `http://host.docker.internal:4566`, the data lab's S3 emulator | PageLake: `lake.py` and boto3 read it, so the same code works in Airflow |
| `DATALAB_DB_HOST` | `host.docker.internal`, the data lab's PostgreSQL | CareLine |
| `_PIP_ADDITIONAL_REQUIREMENTS` | `duckdb==2.0.0 boto3==1.44.1`, unless `.env` sets it | the extra packages (below) |

So your `.env` keeps `http://localhost:4566` or `localhost` for runs on your laptop, and the same code works in Airflow.

### Extra Python packages

The Airflow image already has `pandas`, `requests`, `psycopg` and the PostgreSQL and HTTP providers. Without a line in `.env`, the kit installs `duckdb==2.0.0 boto3==1.44.1`: everything PageLake's DAGs import. PageLake needs no line. PyIceberg is not needed in Airflow: no PageLake task touches the Iceberg table.

Another product lists its packages in `.env`, on one line, with versions. CareLine does this in P13:

```text
_PIP_ADDITIONAL_REQUIREMENTS=great_expectations==1.25.0 pyyaml pandas psycopg[binary]
```

That line replaces the default list. The packages are installed every time the container starts, which is why a start takes up to a minute longer. After you change `.env`, recreate the container: `docker compose --profile lite up -d`. Check what is installed with `docker compose exec airflow python -c "import duckdb, boto3; print(duckdb.__version__, boto3.__version__)"`.

The course team installed Great Expectations 1.25.0 this way next to Airflow 3.4.0: `pip check` found no broken requirements.

Save `.env` with LF line endings (VS Code shows `LF` at the bottom right). With CRLF, every value ends in an invisible character, and the package names are wrong.

## 6. Reaching the data lab

Start the data lab profile in `~/de-kit/datalab` before Airflow, and stop it after: `storage` for PageLake, `core` for CareLine.

```bash
(cd ~/de-kit/datalab && docker compose --profile storage up -d)     # CareLine: --profile core
```

- **The S3 emulator** (PageLake): your code builds its DuckDB secret and its boto3 client from `AWS_ENDPOINT_URL`, which is `http://host.docker.internal:4566` inside the container. The keys (`test`), the region and `PAGELAKE_BUCKET` come from your `.env`.
- **PostgreSQL** (CareLine): from a DAG it is at `host.docker.internal:5432`, user `de`, password `de`, with one database per product. For example:

  ```python
  import os
  import psycopg

  host = os.environ.get("DATALAB_DB_HOST", "localhost")
  with psycopg.connect(host=host, dbname="careline", user="de", password="de") as conn:
      print(conn.execute("SELECT count(*) FROM raw.appointments").fetchall())
  ```

## 7. The command line

Run Airflow's commands inside the container. In `lite` the service is `airflow`; in `full` use `airflow-scheduler`.

| To do this | Command |
|---|---|
| List the DAGs | `docker compose exec airflow airflow dags list` |
| Show import errors | `docker compose exec airflow airflow dags list-import-errors` |
| Run a whole DAG once for one date, without the scheduler | `docker compose exec airflow airflow dags test pagelake_daily 2026-11-04` |
| Save that run's output to a file (`-T` when you pipe) | `docker compose exec -T airflow airflow dags test pagelake_daily 2026-11-03 2>&1 \| tee data/outage.txt` |
| Unpause or pause a DAG | `docker compose exec airflow airflow dags unpause pagelake_daily` (or `pause`) |
| Start a run now | `docker compose exec airflow airflow dags trigger pagelake_daily` |
| List the runs and their state | `docker compose exec airflow airflow dags list-runs pagelake_daily` |
| Only the failed runs, or one week | add `--state failed`, or `-s 2026-11-02 -e 2026-11-08` |
| Backfill (run the past) for a range of dates | `docker compose exec airflow airflow backfill create --dag-id pagelake_daily --from-date 2026-11-02 --to-date 2026-11-08 --max-active-runs 1 --reprocess-behavior completed` |
| See what a backfill would run, without running it | the same command with `--dry-run` |

- `dags test` prints every task's log in the terminal, one `[DAG TEST] end task` line per task, and ends with `DagRun Finished` and the state. It waits out retry delays, printing `No tasks to run` lines in between.
- **`dags test` and the day.** `dags test pagelake_daily 2026-11-04` sets the logical date to 2026-11-04, but its data interval is the day before (3 to 4 November). Read the run's day from `ds`, not from `data_interval_start`.

### Backfills

- In Airflow 3 the scheduler runs a backfill, so **unpause the DAG first**. Unpausing also starts the newest scheduled run (for yesterday), as the schedule says.
- The backfill prints one `Created backfill Dag run.` line per logical date. Its runs are named `backfill__<date>`, but **read the logical date column, not the run name**: a run's name carries the end of its data interval, so the run for 6 November is named `backfill__2026-11-07T00:00:00+00:00`. A day that already had a run (from `dags test`, for example) keeps its old name, such as `manual__…`.
- `--reprocess-behavior` decides what happens to days that already have a run: `none` (the default) skips them, `failed` runs again only the days whose run failed, and `completed` runs every day again. The `--dry-run` output starts with `Runs to be attempted:` and a table of logical dates: trust that table. Without `--dry-run`, the command still prints a `Created backfill Dag run.` line for every date of the range, but only the days the dry run listed run again (check with `dags list-runs`).
- `--max-active-runs 1` makes the backfill run one day at a time. That limit is the backfill's own: it is applied independently of the DAG's `max_active_runs` setting, so a backfill run can start while a scheduled run is still running.

## 8. Logs

- **A task's log**: on the web page, open the DAG, the run and the task, then **Logs**. The same files are in the container, one per try: `/opt/airflow/logs/dag_id=<dag>/run_id=<run>/task_id=<task>/attempt=1.log`. List them with `MSYS_NO_PATHCONV=1 docker compose exec airflow ls /opt/airflow/logs/dag_id=pagelake_daily`.
- **Airflow's own log** (start-up, scheduler, errors): `docker compose --profile lite logs --tail 50 airflow`.

Run history and logs live in the volume `<folder>_airflow-home` (`full`: `<folder>_airflow-db-data` and `<folder>_airflow-logs`), not in your product folder, so Git never sees them.

## 9. Stop and reset

| To do this | Command |
|---|---|
| Stop Airflow, keep run history and logs | `docker compose --profile lite down` |
| Stop it and delete history and logs | `docker compose --profile lite down -v` |

Always name the profile: `docker compose down` on its own stops nothing here. Stop the data lab too, in `~/de-kit/datalab`, with its own profile.

## 10. The `full` profile

`docker compose --profile full up -d` starts `airflow-db` (PostgreSQL for Airflow's own data, user and password `airflow`, local only), a one-time `airflow-init`, then `airflow-apiserver` (the web page on 8080), `airflow-scheduler`, `airflow-dag-processor` and `airflow-triggerer`. The sign-in, the folders, the working folder and `.env` are the same as in `lite`. Run commands in `airflow-scheduler`, for example `docker compose exec airflow-scheduler airflow dags list`.

## Memory

Measured on the course versions, idle with one small DAG: `lite` about 1.5 GB; `full` about 1.5 GB in five containers (scheduler 660 MB, API server 300 MB, triggerer 220 MB, DAG processor 190 MB, PostgreSQL 70 MB). On an 8 GB laptop, run `lite` and one data lab profile (`storage` or `core`), and nothing else.

## Codespaces and Linux

Airflow runs as user 50000. On Linux and in GitHub Codespaces, that user cannot write to your product folder. Add your own user number to `.env` once, then start Airflow again:

```bash
echo "AIRFLOW_UID=$(id -u)" >> .env
```

On Windows with Docker Desktop you do not need this.

## Troubleshooting

- **`port is already allocated` or `address already in use` for 8080**: another program uses port 8080, often Airflow from another product folder or a Spark master. Find it with `docker ps --format "table {{.Names}}\t{{.Ports}}"` and stop it with `docker compose --profile lite down` in its folder.
- **The container keeps restarting, or `ps` shows `Exited`**: read the end of its log with `docker compose --profile lite logs --tail 50 airflow`.
  - `ERROR: Could not find a version` or `No matching distribution`: a package name or version in `_PIP_ADDITIONAL_REQUIREMENTS` is wrong. Fix `.env`, then `up -d` again.
  - `Exited (137)`: Docker ran out of memory. Stop other stacks, and check `~/.wslconfig` (see `setup/windows.md`).
  - Odd characters such as `\r` in the log: `.env` has CRLF line endings. Save it as LF.
- **`unhealthy` for more than 3 minutes**: the web server did not start. The log shows why; the most common cause is the first package installation over a slow network. Wait, then run `docker compose --profile lite ps` again.
- **A DAG does not appear**: wait 30 seconds, then run `airflow dags list-import-errors` (step 7).
- **`ModuleNotFoundError: No module named 'pagelake'`**: the package folder must sit next to `compose.yaml` and hold an `__init__.py`.
- **`the input device is not a TTY`**: add `-T` after `exec` when you pipe the output, as in `docker compose exec -T airflow ...`.
- **`Could not connect to the endpoint URL`** (PageLake): the S3 emulator is not running. Start the data lab's `storage` profile. With an old copy of this `compose.yaml`, copy the kit's file again: it sets `AWS_ENDPOINT_URL`.
- **`connection refused` to PostgreSQL** (CareLine): start the data lab's `core` profile, and use `DATALAB_DB_HOST`, not `localhost`.
- **`EOFError` in a task**: the code waits for keyboard input, such as an `input()` line left in P5's `compact_day`. A task has no keyboard: remove the line.
- **`sqlite3.OperationalError: database is locked` from `backfill create`** (`lite` profile): Airflow's small SQLite database was busy while the scheduler wrote to it. Run the same command again. If it then says another backfill is running for the DAG, wait for that backfill's runs to finish (`dags list-runs`) and try again.
- **Backfill runs stay queued**: the DAG is paused. Unpause it (step 7).
- **The sign-in fails**: the user is `airflow` and the password is `airflow`. If it still fails, run `docker compose --profile lite down` and `up -d` again.
- **A `.env` change has no effect** (a new webhook address, for example): recreate the container with `docker compose --profile lite up -d`, or add `--force-recreate`. Check with `docker compose exec airflow printenv <NAME>`.
- **`Permission denied` when a task writes to `data/`** (Linux or Codespaces): see "Codespaces and Linux" above.

## Image versions

| Service | Image |
|---|---|
| Airflow | `apache/airflow:3.4.0-python3.12` (Airflow 3.4.0 on Python 3.12) |
| Airflow's database in `full` | `pgvector/pgvector:0.8.7-pg16` (PostgreSQL 16, the same image as the data lab) |
