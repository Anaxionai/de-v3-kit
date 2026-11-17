# Versions

The tools, images and libraries the course uses, and the version of each.
Briefs never name versions: when a version matters, a task points here.
**Checked on 12 and 13 November 2026** against each project's official release page, container registry or PyPI. "Tested" in the Notes column means the course team ran it on Windows 11 with Docker Desktop on 13 November 2026.

How to read the tables:

- **Pinned** means: use exactly this version. The kit's own files use it, such as `datalab/docker-compose.yml`.
- **Course version** means: install this version. A newer patch release (the last number) is fine.
- **Tested** means: the version the course was tested with. Your project's lock file (`uv.lock`) pins the exact version you get.

## On your laptop (Windows)

[`setup/windows.md`](setup/windows.md) installs these.

| Tool | Version | Kind | Notes |
|---|---|---|---|
| Windows | 11, version 23H2 or newer | minimum | Docker Desktop needs 23H2 (build 22631) or newer |
| Git for Windows (Git Bash) | 2.56.1 | course version | Any 2.45 or newer works |
| VS Code | the newest (1.146 on 13 November 2026) | — | It updates itself |
| uv | 0.13.8 | course version | 0.12 or newer. Run `uv python pin --global 3.12` once, so uv never picks its newest Python (3.15) |
| Python | 3.12.16 | course version | Any 3.12 release, installed with `uv python install 3.12`. Every project pins it with `uv python pin 3.12` (a `.python-version` file) |
| Docker Desktop | 4.99.0 | course version | The newest release (9 November 2026), with the WSL 2 engine. Free under the Personal plan for individual learning, and for small businesses with fewer than 250 employees and less than $10 million in yearly revenue |
| WSL | 2.1.5 or newer | minimum | Check with `wsl --version`; update with `wsl --update`. The newest is 3.0.5 |
| DuckDB | 2.0.0 | course version | The Python package `duckdb`, and the DuckDB command-line program if you want it. In DuckDB 2.0, read results with `.fetchall()`: `.fetchone()` on `con.sql(...)` was removed |
| AWS CLI | 2.40.1 | course version | Any 2.x release. `winget install -e --id Amazon.AWSCLI` |
| Power BI Desktop | the newest from the Microsoft Store | — | P14. It updates itself from the Store |

## Data lab images

These are pinned in the kit's Compose files under [`datalab/`](datalab/). Do not change them in your own copy.

| Service | Image | Kind | Notes |
|---|---|---|---|
| PostgreSQL 16 with pgvector | `pgvector/pgvector:0.8.7-pg16` | pinned | PostgreSQL 16.15 and pgvector 0.8.7. Tested |
| S3 emulator (Floci) | `floci/floci:2.4.0` | pinned | MIT licence, no account needed. Tested: S3, IAM, Lambda, Step Functions, Glue catalogue, Athena, Kinesis, Firehose, Redshift, Secrets Manager |
| Floci's Athena helper | `floci/floci-duck:0.4.1` | pinned | Started by Floci on the first Athena query |
| Apache Airflow | `apache/airflow:3.4.0-python3.12` | pinned | Airflow 3.4.0 on Python 3.12. Tested in `lite` and `full` |
| Apache Spark | `apache/spark:4.2.1` | pinned | Spark 4.2.1, Scala 2.13, Java 21, Python 3.10. The kit builds `de-kit-spark:4.2.1-r2` from it. Tested in `lite` and `full` |
| Apache Kafka | `apache/kafka:4.4.0` | pinned | One broker in KRaft mode. Tested |
| Kafka Connect with Debezium | `quay.io/debezium/connect:3.7.1.Final` | pinned | Debezium 3.7.1 (its Kafka Connect is 4.3.1). Tested with the PostgreSQL connector |

### Why Spark 4.2 and not 4.3

Spark 4.3.0 is the newest Spark (30 October 2026). The course uses **Spark 4.2.1**, because Delta Lake 4.4.1, the newest Delta release, is built for Spark 4.2, 4.1 and 4.0, and no Delta release supports Spark 4.3 yet (Delta's release notes, 5 October 2026). The Spark 4.3.0 image's Python (3.10) is also older than PySpark 4.3 needs (3.11 or newer). Databricks Free Edition (P7, week 2) runs its own Spark and is not affected.

| Library inside the kit's Spark image | Version | Kind |
|---|---|---|
| Delta Lake | 4.4.1 (`io.delta:delta-spark_4.2_2.13:4.4.1`) | pinned |
| Spark's Kafka source | `org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.1` (with `kafka-clients` 3.9.2) | pinned |
| pytest | 9.2.0 | pinned |

## Lakehouse table formats

| Tool | Version | Kind | Notes |
|---|---|---|---|
| Apache Iceberg | 1.12.0 | — | The newest Iceberg release, for reading the specification and the docs (P5). On AWS, Glue bundles its own Iceberg version (1.10.0 in Glue 5.1: see the AWS Glue row) and Athena supports Iceberg tables directly (P11) |
| PyIceberg | 0.12.0 | tested | The Python library for Iceberg tables (P5). Tested against the S3 emulator with a SQL catalogue |
| Delta Lake | 4.4.1 | pinned | In the kit's Spark image (above) |
| `deltalake` (Python, no Spark) | 1.6.6 | tested on PyPI | Only for Stretch goals |

## dbt

The course uses **dbt Core 1.x**, not dbt v2. dbt's documentation now shows its newer "Fusion" engine (dbt v2) first. Fusion is a separate engine with its own installer and licence terms, and the course does not use it. dbt Core 1.x is open source (Apache License 2.0), installs from PyPI with `uv add`, and has the DuckDB adapter that the dbt learn cards use on your laptop. When a dbt docs page shows two versions, read the dbt Core one.

| Package | Version | Kind | Notes |
|---|---|---|---|
| `dbt-core` | 1.12.7 | course version | The newest 1.x release |
| `dbt-snowflake` | 1.12.5 | course version | For P9 GitPulse on Snowflake |
| `dbt-duckdb` | 1.11.1 | course version | For the learn cards' try-its, on your laptop. Works with `dbt-core` 1.12 |

## Cloud and infrastructure tools

| Tool | Version | Kind | Notes |
|---|---|---|---|
| Snowflake CLI (`snow`) | 3.33.0 | course version | P9 |
| Terraform | 1.17.2 | course version | Or run it from the image `hashicorp/terraform:1.17.2`. The newest release (11 November 2026, HashiCorp releases). Tested: the P10 and P11 starters pass `terraform fmt -check`, `init` and `validate` |
| `hashicorp/azurerm` provider | 5.13.0 | pinned | In `required_providers`: `version = "5.13.0"` (P10). The newest release (5 November 2026, Terraform Registry). Tested: `terraform validate` on the P10 starter |
| `hashicorp/aws` provider | 6.73.0 | pinned | In `required_providers`: `version = "6.73.0"` (P11). The newest release (11 November 2026, Terraform Registry). Tested on the S3 emulator. On the emulator this version needs `skip_requesting_account_id` and `skip_credentials_validation`, in the `emulator` workspace only: see the P11 starter's `aws/infra/providers.tf` |
| `hashicorp/archive` provider | 2.8.1 | pinned | P11: `archive_file` zips the Lambda code. In `required_providers`: `version = "2.8.1"`. The newest release (11 September 2026, Terraform Registry). Run `terraform init` again after you add it. Tested: `terraform validate` |
| Azure CLI | 2.92.0 | course version | P10 |
| Google Cloud CLI (with `bq`) | 593.0.0 | course version | P12 |
| k3d | 5.9.0 | course version | `winget install -e --id k3d.k3d --version 5.9.0`. Tested |
| k3s (inside k3d) | `rancher/k3s:v1.35.5-k3s1` | pinned | k3d 5.9.0's default image. Tested |
| kubectl | 1.35.4 | course version | `winget install -e --id Kubernetes.kubectl --version 1.35.4`. kubectl supports a cluster one minor version older or newer. Tested |

## Cloud runtimes

You set these in a Terraform file or choose them in the cloud console.

| Runtime | Version | Kind | Notes |
|---|---|---|---|
| AWS Lambda Python runtime (P11 ingest function) | `python3.12` | pinned | In `aws_lambda_function`: `runtime = "python3.12"`, the same Python as your laptop and your tests. It runs on Amazon Linux 2023 and is supported until 31 October 2028 (AWS Lambda docs, "Lambda runtimes", 13 November 2026). AWS also offers `python3.13`, `python3.14` and, in preview, `python3.15` |
| AWS Glue (P11 clean job) | `5.1` | pinned | In `aws_glue_job`: `glue_version = "5.1"`. It runs Spark 3.5.6 and Python 3.11, and Iceberg 1.10.0 when the job sets `--datalake-formats` to `iceberg` (AWS Glue docs, release notes and "Using the Iceberg framework in AWS Glue", 13 November 2026). Glue 6.0 (Spark 4.1.1, Python 3.13) is newer and the default for new jobs. The course stays on 5.1 for two reasons. AWS's Iceberg page gives the Iceberg version only up to 5.1. Glue 6.0 also turns on Spark's ANSI mode, so a value that does not cast stops the job instead of becoming NULL |
| Databricks Runtime on Azure Databricks (P10 cluster `cc-single`) | 18 LTS | pinned | Choose "18 LTS", not the Machine Learning variant. Apache Spark 4.1.0, released 10 June 2026, supported until 10 June 2029 (Microsoft Learn, "Databricks Runtime release notes versions and compatibility", updated 6 November 2026). Runtime 19 (Spark 4.2.0) is newer, but it is not a long-term support (LTS) release |

## Images for your own Dockerfiles and Compose files

| Use | Image | Kind |
|---|---|---|
| Python jobs (for example P4's loader) | `python:3.12.16-slim-bookworm` | pinned |
| uv inside a Dockerfile: `COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /uvx /bin/` | `ghcr.io/astral-sh/uv:0.13.8` | pinned |
| Python 3.12 with uv, for one-off runs (see `setup/windows.md`, Step 12) | `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` | course version |
| The AWS CLI v2 in a container | `amazon/aws-cli:2.40.1` | pinned |

## GitHub Actions

Use these versions in workflow files, written as `uses: name@version`. Run jobs on `runs-on: ubuntu-24.04`.

| Action | Version |
|---|---|
| `actions/checkout` | `v7` (now `v7.0.1`) |
| `actions/setup-python` | `v7` (now `v7.1.0`) |
| `astral-sh/setup-uv` | `v10.3.3` (a full tag: setup-uv publishes no moving `v10` tag) |

## The dev container

Pinned in [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json):

| Part | Version |
|---|---|
| Base image | `mcr.microsoft.com/devcontainers/base:3.0.12-ubuntu24.04` |
| Docker inside the container | feature `ghcr.io/devcontainers/features/docker-in-docker:4` |
| AWS CLI | feature `ghcr.io/devcontainers/features/aws-cli:1` |
| kubectl | feature `ghcr.io/devcontainers/features/kubectl-helm-minikube:1`, kubectl 1.35.4 |
| GitHub CLI | feature `ghcr.io/devcontainers/features/github-cli:1` |
| uv | 0.13.8, with Python 3.12 pinned globally |

## Python libraries

Add them with `uv add`, for example `uv add "pandas==3.1.1"` to pin one.

| Package | Tested | Notes |
|---|---|---|
| `pandas` | 3.1.1 | |
| `pyarrow` | 26.0.1 | See "Smart App Control" in `setup/windows.md` if it fails to import |
| `polars` | 2.1.0 | |
| `duckdb` | 2.0.0 | |
| `psycopg` | 3.3.9 | Install as `psycopg[binary]` |
| `pgvector` | 0.5.1 | The Python package for pgvector's `vector` type |
| `sqlalchemy` | 2.1.8 | |
| `requests` | 2.34.2 | |
| `httpx` | 0.28.1 | |
| `pydantic` | 2.14.3 | |
| `python-dotenv` | 1.2.4 | |
| `boto3` | 1.44.1 | |
| `pyiceberg` | 0.12.0 | Install as `pyiceberg[sql-sqlite,pyarrow]` for the SQL catalogue |
| `kafka-python` | 3.0.13 | |
| `confluent-kafka` | 2.16.1 | |
| `great-expectations` (GX Core) | 1.25.0 | P13. The newest release on PyPI (12 November 2026). Tested next to Airflow 3.4.0 in the Airflow image: no broken requirements |
| `google-genai` | 3.3.0 | P15, the Gemini API library |
| `matplotlib` | 3.11.2 | |
| `jupytext` | 1.19.6 | Saves notebooks as `.py` files |
| `pytest` | 9.2.0 | On Windows with Smart App Control, run tests as `uv run python -m pytest` if `pytest.exe` is blocked |
| `ruff` | 0.17.5 | Ruff 0.17's default rule set is much broader than in older versions, so `uv run ruff check` may report more than older tutorials show |
| `apache-airflow-providers-postgres` | 7.1.1 | Already in the Airflow image |
