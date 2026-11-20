# Guided starters

Every project in the course has three levels. Your mentor tells you yours.

- **Core**: you start the project from an empty folder.
- **Guided**: you start from a starter in this folder.
- **Stretch**: you do Core, plus the module's Stretch goals.

## What a starter is

A starter is the first version of a project's product folder, such as `pricewatch/` or
`scorebook/`. It does the set-up work that is not the point of the project: the project
files, the folder layout, the settings, the test set-up, the names of the functions with
what each must do, and SQL files with their headings. Your time then goes on the ideas the
tasks teach.

A starter never contains a solution. Every function, query, model or resource a task asks
you to write is a stub with a marker that names the task:

- Python: `raise NotImplementedError("TODO(task 9): ...")`
- SQL and DAX: a `-- TODO(task 9): ...` comment
- YAML, TOML, Terraform and shell: a `# TODO(task 9): ...` comment
- Markdown: a `TODO(task 9): ...` line under each heading

The number is the task's number in that project's module. A test for code you have not
written yet is skipped (`@pytest.mark.skip(reason="TODO(task 9) ...")`), so the tests pass
from the first day. Remove the skip when you have written the code it tests.

Reviewers accept a starter's file names and layout, as long as you wrote what each TODO
asks for.

## How to use a starter

1. In the project's first build task, run `git pull` in `~/de-kit`.
2. In Git Bash, inside that task's folder, copy the starter in as the product folder. For
   example, for PriceWatch:

   ```bash
   cp -r ~/de-kit/starters/p01-pricewatch pricewatch
   cd pricewatch
   ```

   `cp -r` also copies the hidden files, such as `.gitignore` and `.python-version`.
3. Read `STARTER.md` in the copied folder. It says which steps of the brief the starter
   has already done, how to run it, and lists every TODO with its task.
4. Work through the tasks. To see what is left, run `grep -rn "TODO(task" .` in the
   product folder.
5. From the next task on, copy your product folder forward, as every brief says. Copy
   the starter only once: copying it again would overwrite your work.

`STARTER.md` is not your project's README. You write the product's `README.md` yourself
in the project's wrap-up task. Keep `.venv/`, `data/` and `.env` out of Git, as for Core.

## The starters

| Starter | Project | Product folder | Module and weeks | Copy it in at | What it holds |
|---|---|---|---|---|---|
| `p01-pricewatch` | P1 PriceWatch | `pricewatch/` | 3, weeks 5-6 | task 8 | Python: uv project, week 1 modules, week 2 modules in `later/`, empty tests |
| `p02-scorebook` | P2 Scorebook | `scorebook/` | 4, weeks 7-8 | task 7 | SQL: `schema.sql`, check and view headings, `psql.sh`, loader stubs |
| `p03-retailbase` | P3 RetailBase | `retailbase/` | 5, week 9 | task 7 | SQL: the four numbered files, one file per question, model headings |
| `p04-clearair` | P4 ClearAir | `clearair/` | 6, weeks 10-11 | task 8 | Python: package stubs, skipped tests with fixtures, Docker, CI and Kubernetes stubs |
| `p05-pagelake` | P5 PageLake | `pagelake/` | 7, week 12 | task 8 | Python: uv project, package stubs, DuckDB query files |
| `p06-pagelake` | P6 PageLake part 2 (add-on) | `pagelake/` (new files in `dags/`, `pagelake/`, `sql/`, `tests/`) | 8, week 13 | task 8 | Add-on to your P5 `pagelake/`: DAG and step stubs, alert and freshness stubs, check queries, skipped tests, runbook headings. Copy it with `cp -rn ~/de-kit/starters/p06-pagelake/. pagelake/` and read `STARTER-P6.md` |
| `p07-taxiscale` | P7 TaxiScale | `taxiscale/` | 9, weeks 14-15 | task 8 | Python: Spark job and notebook stubs, skipped tests |
| `p08-editstream` | P8 EditStream | `editstream/` | 10, week 16 | task 8 | Python: producer, consumer and stream stubs, skipped tests |
| `p09-gitpulse` | P9 GitPulse | `gitpulse/` | 11, weeks 17-18 | task 8 | Numbered Snowflake files and a dbt project skeleton |
| `p10-cyclecity` | P10 CycleCity | `cyclecity/` | 12, weeks 19-20 | task 8 | Terraform in `infra/`, pipeline and notebook stubs |
| `p11-cyclecity` | P11 CycleCity part 2 (add-on) | `cyclecity/aws/` | 13, weeks 21-22 | task 8 | Add-on to your P10 `cyclecity/` (`cp -r ~/de-kit/starters/p11-cyclecity/aws cyclecity/`): Terraform in `aws/infra/`, function, job and pipeline stubs, SQL files, docs headings |
| `p12-gitpulse` | P12 GitPulse part 2 (add-on) | `gitpulse/bigquery/` | 14, week 23 | task 7 | Add-on to your P9 `gitpulse/`: one SQL file per question, a finished `bytes_report.sql`, budget and findings headings |
| `p13-careline` | P13 CareLine | `careline/` | 15, week 24 | task 8 | Python: DAG, check and contract stubs, skipped tests |
| `p14-retailbase` | P14 RetailBase part 2 (add-on) | `retailbase/bi/` | 16, week 25 | task 8 | Add-on to your P3 `retailbase/`: Power BI measure and check files, document headings (no `.pbix`) |
| `p15-careline` | P15 CareLine part 2 (add-on) | `careline/` (new files in `careline/`, `sql/`, `tests/`, `evalset/`) | 17, week 26 | task 7 | Add-on to your P13 `careline/`: masking, chunking, embedding, search, extraction, refresh and evaluation stubs, the two notes and AI SQL files, skipped tests, the test set's header. Copy it with `cp -rn ~/de-kit/starters/p15-careline/. careline/` and read `STARTER-P15.md` |

An **add-on** (marked in the table) is not a whole product folder. It adds new files to the
product folder you built in part 1, and replaces none of them. Copy only the folder its
`STARTER.md` names, into your own product folder, for example
`cp -r ~/de-kit/starters/p12-gitpulse/bigquery gitpulse/bigquery`.

Where a brief tells you to copy one of the kit's Compose files into your product folder
(Airflow, Spark or Kafka), do that yourself, as the brief says, unless the project's
`STARTER.md` says the starter already has it.

## When something does not run

Each starter runs as shipped: `uv sync` works, the tests pass (skipped), and every `.sql`
file runs. A stub stops with `NotImplementedError` or does nothing until you write it.
If anything else fails, tell your mentor and say which starter and which command.
