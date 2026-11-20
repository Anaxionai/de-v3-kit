# The data lab

The data lab runs the course's databases and services on your laptop, in Docker Desktop. Nothing here costs money, and nothing leaves your laptop.

It has two parts:

- **The shared services**, in this folder: one Compose file, `docker-compose.yml`, with two profiles (named groups of services). `core` is PostgreSQL. `storage` is an S3 emulator (a program that imitates Amazon S3 on your laptop).
- **The product stacks**: Airflow, Spark and Kafka. Each product runs its own copy. You copy `airflow/compose.yaml`, `spark/compose.yaml` or `kafka/compose.yaml` into your product folder and start it there. Each one has a `lite` profile for 8 GB laptops and a `full` profile for 16 GB laptops.

Kubernetes is not a profile. It runs in k3d: see [`k3d/README.md`](k3d/README.md).

## Before you start

- Docker Desktop is running, with the WSL 2 engine. [`setup/windows.md`](../setup/windows.md) shows how to install it.
- You use Git Bash in the VS Code terminal for every command.
- Go to this folder first. Every command in this part of the file runs from here:

```bash
cd ~/de-kit/datalab
docker compose version
```

The second command prints `Docker Compose version v` and a number. If it prints an error, start Docker Desktop and wait until it says **Engine running**.

## The two profiles

| Profile | What it starts | Container name | Used in |
|---|---|---|---|
| `core` | PostgreSQL 16 with pgvector | `datalab-postgres-1` | the map weeks, P2, P3, P4, P13, P14, P15 |
| `storage` | Floci, a local AWS, used mostly as S3 | `datalab-floci-1` | P5, P6, P11 |

The Compose project is always named `datalab`, so the container names above never change.

## Start, check and stop

| To do this | Command |
|---|---|
| Start PostgreSQL | `docker compose --profile core up -d` |
| Start the S3 emulator | `docker compose --profile storage up -d` |
| Check that it runs | `docker compose --profile core ps` |
| Stop it and keep the data | `docker compose --profile core down` |
| Stop everything in the lab | `docker compose --profile "*" down` |

The first start of each profile downloads its image once. On a slow connection this takes 5 to 10 minutes.

`ps` shows one line per service. The `STATUS` column says `Up` and, after a few seconds, `(healthy)`.

Always name a profile. `docker compose down` on its own stops nothing here, because every service belongs to a profile.

## Reset a profile (delete its data)

```bash
docker compose --profile core down -v
docker compose --profile core up -d
```

The `-v` flag deletes the profile's volumes (storage that Docker keeps between runs). The next start creates every database again, empty. Other profiles keep their data.

| Service | Keeps its data after `down`? |
|---|---|
| PostgreSQL | Yes, in the volume `datalab_postgres-data` |
| Floci | Yes: buckets and objects, in the volume `datalab_floci-data` |

## Ports, users and passwords

These passwords and keys work only on your laptop. Never use them on a real server or a real cloud account.

| Service | Profile | Address from your laptop | Sign-in |
|---|---|---|---|
| PostgreSQL 16 | `core` | `localhost:5432` | user `de`, password `de` |
| S3 emulator | `storage` | `http://localhost:4566` | access key `test`, secret key `test`, region `ap-south-1` |
| Redshift clusters on the emulator (P11) | `storage` | `localhost`, ports 7100 to 7104 | the user and password you give `create-cluster` |

## PostgreSQL

### The databases

The first start creates one database per product, named after the product folder:

| Database | Used by |
|---|---|
| `tiny` | the map weeks: the tiny pipeline and the first container task |
| `scorebook` | P2 Scorebook |
| `retailbase` | P3 RetailBase, and P14 RetailBase part 2 (the Power BI report reads it) |
| `clearair` | P4 ClearAir |
| `careline` | P13 CareLine, and P15 CareLine part 2 (the visit notes and their vectors, with pgvector) |

There is also a database named `de`, which is empty. The databases are made only when the volume is new. If one is missing, your volume is older than this file: reset the profile (see above) or create it with `CREATE DATABASE <name>;`.

### psql inside the container

You do not need PostgreSQL on Windows: `psql` (PostgreSQL's command-line client) runs inside the container.

Open psql on one database:

```bash
docker exec -it datalab-postgres-1 psql -U de -d scorebook
```

Leave psql with `\q`. In the separate Git Bash window (not VS Code's terminal), put `winpty` in front if you see `the input device is not a TTY`.

Run a SQL file from your product folder, or load a CSV file, from any folder:

```bash
docker exec -i datalab-postgres-1 psql -U de -d scorebook < sql/schema.sql
docker exec -i datalab-postgres-1 psql -U de -d scorebook -c "COPY matches FROM STDIN (FORMAT csv, HEADER)" < data/matches.csv
```

Use `-i`, not `-it`, when you send a file with `<`. The file is read on your laptop and sent to psql, so give its path on your laptop.

In this folder, `docker compose exec postgres psql -U de -d scorebook` does the same as the first command.

### From Python on your laptop

The address is `postgresql://de:de@localhost:5432/scorebook`. For example, with psycopg, in a uv project pinned to Python 3.12 (`uv python pin 3.12`):

```bash
uv add "psycopg[binary]"
uv run python -c "import psycopg; print(psycopg.connect('postgresql://de:de@localhost:5432/scorebook').execute('SELECT 1').fetchone())"
```

It prints `(1,)`. If it fails with `An Application Control policy has blocked this file`, read "Smart App Control" in [`setup/windows.md`](../setup/windows.md).

### pgvector

pgvector (the extension that stores embeddings) is installed but not switched on. Switch it on once in each database that needs it:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

User `de` is allowed to do this. The extension stays in the database after `down` and `up`.

### Change data capture

The server runs with `wal_level=logical`, so a tool such as Debezium can read the database's own log of changes (P8). If `SHOW wal_level;` prints `replica`, your copy of the kit is old: run `git pull` in `~/de-kit`, then `docker compose --profile core down` and `docker compose --profile core up -d`. Your data stays.

## The S3 emulator

The `storage` profile runs Floci, a free AWS emulator, at `http://localhost:4566`. [`storage/README.md`](storage/README.md) shows how to use it from the AWS CLI, DuckDB and Python, and which other AWS services it imitates.

```bash
docker compose --profile storage up -d
curl -s http://localhost:4566/_floci/health
```

The second command prints JSON that contains `"version":"2.4.0"` and `"s3":"running"`.

## The product stacks: lite and full

Airflow, Spark and Kafka run per product, from your product folder. Copy the kit's file into the product folder as `compose.yaml`, then start one profile there. The folder's README gives every command.

| Stack | Copy from | Start on an 8 GB laptop | Start on a 16 GB laptop |
|---|---|---|---|
| Airflow (P6, P13) | `~/de-kit/datalab/airflow/compose.yaml` | `docker compose --profile lite up -d` | `docker compose --profile full up -d` |
| Spark (P7, P8) | `~/de-kit/datalab/spark/compose.yaml` | `docker compose --profile lite up -d` | `docker compose --profile full up -d` |
| Kafka (P8) | `~/de-kit/datalab/kafka/compose.yaml` | `docker compose up -d` | `docker compose up -d` (add `--profile cdc` for Debezium) |

- `lite` runs everything in one container where it can. It fits next to VS Code and a browser on an 8 GB laptop.
- `full` runs each part in its own container, as a team runs it at work. It needs a 16 GB laptop, or GitHub Codespaces (see [`setup/codespaces.md`](../setup/codespaces.md)).
- Run one product stack at a time. Stop it with `docker compose --profile lite down` (or `full`) in the same folder before you start another.
- A product stack never needs another product's containers. It may need the `core` profile here, when its task says so.

## Memory advice

Docker Desktop's total memory is capped in `~/.wslconfig` (see [`setup/windows.md`](../setup/windows.md)): 4 GB on an 8 GB laptop, 8 GB on a 16 GB laptop.

Memory measured on the course versions, idle, with `docker stats --no-stream`:

| What runs | About |
|---|---|
| `core` (PostgreSQL) | 45 MB |
| `storage` (Floci) | 40 to 85 MB, up to 200 MB after use, plus about 128 MB for each Lambda function while it runs and 100 MB for each Redshift cluster |

The product stacks use more: their READMEs give their numbers.

- On an 8 GB laptop, run `core` and one product stack in its `lite` profile, and nothing else. Close browser tabs you do not need.
- Stop each profile when its task is done.
- Check live use with `docker stats --no-stream`.

## Reaching the lab from your own containers

Inside a container, `localhost` is the container itself, not your laptop. Use `host.docker.internal` instead, and add this to the service in your own `compose.yaml`:

```yaml
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

A container then reaches PostgreSQL at `host.docker.internal:5432` and the S3 emulator at `http://host.docker.internal:4566`. The kit's Airflow and Spark files already have these lines.

## Git Bash and paths inside containers

Git Bash changes any argument that starts with `/` into a Windows path. That breaks a Docker command that names a path inside a container. Put `MSYS_NO_PATHCONV=1` in front of that one command:

```bash
MSYS_NO_PATHCONV=1 docker exec datalab-postgres-1 ls /var/lib/postgresql/data
```

Commands with no such path need nothing extra, for example `docker compose --profile core ps`. Never `export` the variable for the whole terminal: it breaks other commands.

## Troubleshooting

- **`port is already allocated`** or **`address already in use`**: another program uses that port. Find it with `docker ps --format "table {{.Names}}\t{{.Ports}}"`. A PostgreSQL installed on Windows also takes port 5432: stop it in the Windows Services app.
- **A service is not `Up`** or says `unhealthy`: read its last log lines, for example `docker compose --profile core logs --tail 30 postgres`.
- **`password authentication failed for user "de"`**: the volume was made with another password. Reset the profile with `docker compose --profile core down -v`. This deletes the data.
- **`database "<name>" does not exist`**: the volume is older than the kit. Reset the profile, or run `CREATE DATABASE <name>;` in psql.
- **`type "vector" does not exist`**: run `CREATE EXTENSION IF NOT EXISTS vector;` in your database.
- **`docker compose down` did nothing**: name the profile, or use `--profile "*"`.
- **`Cannot connect to the Docker daemon`** or **`error during connect`**: start Docker Desktop and wait until it says **Engine running**.
- **The laptop is slow**: run `docker stats --no-stream` and stop the profiles and stacks you are not using.

## Image versions

The images are pinned in `docker-compose.yml`. [`VERSIONS.md`](../VERSIONS.md) lists every version the course uses.

| Service | Image |
|---|---|
| PostgreSQL 16 with pgvector | `pgvector/pgvector:0.8.7-pg16` |
| Floci (S3 emulator) | `floci/floci:2.4.0` |
| Floci's Athena helper, started on first use | `floci/floci-duck:0.4.1` |
