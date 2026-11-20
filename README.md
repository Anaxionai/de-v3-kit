# Data Engineering course kit

This is the course kit for the Data Engineering track.
It holds what your tasks need beyond your own code: the laptop setup guides, a data lab that runs databases and data tools on your laptop, the course datasets and their download scripts, the cloud guides, the Guided starters and the capstone briefs.
Your task briefs link to files in this kit.

## Get the kit

Run this once, in Git Bash, in week 2:

```bash
cd ~ && git clone https://github.com/Anaxionai/de-v3-kit.git de-kit
```

This makes the folder `~/de-kit`, which is `C:\Users\<your name>\de-kit` on Windows.
Keep it next to your course repository, never inside it.

Check it: `ls ~/de-kit` lists `README.md`, `VERSIONS.md`, `setup`, `datalab` and the other folders below.

## Update the kit

When a task says "Run `git pull` in `~/de-kit`", run:

```bash
cd ~/de-kit
git pull
```

Do not change the kit's files. Copy a file into your own repository first, then change your copy.
If `git pull` says your local changes would be overwritten, run `git restore .` in the kit folder. It undoes your changes to the kit's files. Then run `git pull` again.

Every command in the kit's READMEs is written for **Git Bash** in VS Code. [`setup/windows.md`](setup/windows.md) sets it up.

## What is in the kit

| Path | What it is | Used in |
|---|---|---|
| `README.md` | This file | the whole course |
| `VERSIONS.md` | The version of every tool, image and library the course uses | the whole course |
| `LICENSE` | The MIT licence for the kit's code | — |
| `setup/windows.md` | Windows laptop setup: Git Bash in VS Code, uv with Python 3.12, WSL 2, Docker Desktop, the memory limit, Smart App Control | Launchpad, weeks 1 and 2 |
| `setup/wslconfig.example` | A `.wslconfig` file that limits WSL 2's memory and swap, for 8 GB and 16 GB laptops | Launchpad, week 2 |
| `setup/codespaces.md` | Running a lab in GitHub Codespaces when your laptop has 8 GB: the machine, the free hours, how to stop it | P4, P8, P13 |
| `.devcontainer/` | The dev container that Codespaces and VS Code start: Docker, uv, Python 3.12 and the course's tools | P8, P13 |
| `try-it.md` | Free sites where you practise each new idea in the browser | learn cards |
| `datalab/` | The data lab: PostgreSQL 16 with pgvector and an S3 emulator, by Compose profile, and how to run them | the map weeks onwards |
| `datalab/storage/` | Using the AWS CLI, DuckDB and Python against the S3 emulator | P5, P6, P11 |
| `datalab/airflow/` | Airflow for one product, `lite` and `full` profiles | P6, P13 |
| `datalab/spark/` | Spark with Delta Lake for one product, `lite` and `full` profiles | P7, P8 |
| `datalab/kafka/` | One Kafka broker, and Kafka Connect with Debezium | P8 |
| `datalab/k3d/` | A one-node Kubernetes cluster on your laptop with k3d | P4 |
| `data/` | The course datasets: for each one its source, licence, size, download script and a sample. `data/README.md` is the guide | all modules |
| `data/airquality/sample/` | Sample pages of the air-quality API, for students whose API key has not arrived | P4 |
| `cloud/` | The cloud calendar, budgets, and one guide per platform: Snowflake, Azure, Fabric, AWS, Google Cloud and Databricks, and the teardown checklist | P7, P9 onwards |
| `capstone/` | How the capstone works, four data-product briefs, and the plan template | CP1 to CP3 |
| `starters/` | The Guided starters: a starting point for each project, for students on the Guided level. A part-2 project's starter (P6, P11, P12, P14, P15) adds only its new files to your own product folder | all projects |

## Running the kit's Python scripts

Run the kit's Python scripts with `uv run`, from your own project folder, for example:

```bash
uv run python ~/de-kit/data/pageviews/get_hours.py --help
```

uv uses Python 3.12 when you have pinned it (see Step 5 of `setup/windows.md`). A script that needs a library says so at its top, and its README gives the exact command.

## Line endings

The kit's `.gitattributes` file makes Git check out every text file with LF line endings, on Windows too.
Shell scripts, Compose files and data files then work in Git Bash and inside Linux containers. Do not convert them to CRLF.

## Licence and attribution

- **The kit's code** is under the MIT licence: see [`LICENSE`](LICENSE). That covers the scripts, tests, Compose files and configuration written for the kit, unless a folder says otherwise.
- **Datasets.** The kit downloads public datasets, and each keeps its own licence. `data/README.md` lists every dataset with its source and licence, and the credit line to use when you publish results. For example, Cricsheet's ball-by-ball data is under the Open Data Commons Attribution License 1.0, and Wikimedia's page-view data is public domain (CC0), with credit to the Wikimedia Foundation.
- **Generated data.** The clinic, customer-change and station data that the kit's scripts generate is made up. People and places in it are invented.
- **Tools and images.** The tools and container images the course uses keep their own licences: Apache Airflow, Apache Spark, Apache Kafka, Apache Iceberg, Delta Lake and Debezium are under the Apache License 2.0; PostgreSQL and pgvector under the PostgreSQL Licence; Floci (the S3 emulator) under the MIT licence. Docker Desktop is free under the Personal plan for individual learning, and for small businesses with fewer than 250 employees and less than $10 million in yearly revenue.
- **Passwords and keys in the kit** (`de`/`de` for PostgreSQL, `test`/`test` for the S3 emulator, `airflow`/`airflow` for Airflow) are fake and work only on your laptop. The kit holds no real secret.
- Company and product names belong to their owners.
