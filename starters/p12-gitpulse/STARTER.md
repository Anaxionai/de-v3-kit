# Guided starter: P12 GitPulse part 2 (BigQuery)

This starter is an **add-on** to your own `gitpulse/` folder from P9. It adds one new folder, `gitpulse/bigquery/`, and changes nothing you built on Snowflake and dbt. It saves you the set-up: the query-size limit file, one SQL file per question with its header, the bytes report, the budget ledger and the findings page. Every query is still yours to write.

This `STARTER.md` stays in the kit. Read it here: `~/de-kit/starters/p12-gitpulse/STARTER.md`.

## What is included

| Path inside `gitpulse/` | What it is |
|---|---|
| `bigquery/bigqueryrc.example` | The three lines of the 2 GB query-size limit, for `~/.bigqueryrc` |
| `bigquery/sql/q01_events_per_type.sql` … `q05_events_per_hour.sql` | One file per question of task 7: a comment naming it, the question, the source table and where your P9 answer is, and a TODO where your query goes |
| `bigquery/sql/bytes_report.sql` | Complete. Lists today's query jobs with their bytes from `INFORMATION_SCHEMA.JOBS_BY_USER` |
| `bigquery/docs/budget.md` | The scan-budget ledger: a place for your `.bigqueryrc` lines, a table for q01 to q05, and a heading for each later task |
| `bigquery/docs/findings.md` | Five headings, one per question, each with `BigQuery:`, `P9:` and `Same or different:`, and the GH Archive credit line |

`evidence.md` and `AI_LOG.md` are not here: they live in the task folder, next to `gitpulse/`.

## Copy it in

In task 7 (Create the project, set a query-size limit and estimate five queries), first copy your `gitpulse/` folder forward from P9, as the brief says. Then, in Git Bash, inside the task 7 folder:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p12-gitpulse/bigquery gitpulse/bigquery
ls gitpulse/bigquery    # bigqueryrc.example  docs  sql
```

Run the `cp` before you make `gitpulse/bigquery/` yourself. If that folder already exists, `cp -r` puts the copy inside it, as `gitpulse/bigquery/bigquery/`. From task 8 on, copy your `gitpulse/` folder forward as each brief says. Copy the starter only once.

## Set the query-size limit (task 7, step 3)

```bash
cp gitpulse/bigquery/bigqueryrc.example ~/.bigqueryrc
cat ~/.bigqueryrc
```

`cat` must print the three lines. Then copy the same three lines under `## Query-size limit` in `bigquery/docs/budget.md`. `~/.bigqueryrc` lives outside every repository; the example file only saves you typing.

## How to run it

There is nothing to install in this folder: you run the files with `bq` from the task folder.

```bash
bq query --dry_run < gitpulse/bigquery/sql/q01_events_per_type.sql   # estimate, costs nothing
bq query < gitpulse/bigquery/sql/q01_events_per_type.sql             # real run, counts towards the budget
bq query < gitpulse/bigquery/sql/bytes_report.sql                    # what today's runs were billed
```

A file that still holds only its TODO has no query in it, so `bq` has nothing to run.

## Your TODOs

Find them with `grep -rn "TODO(task" gitpulse/bigquery`.

| Task | File | What you write |
|---|---|---|
| 7 | `sql/q01_events_per_type.sql` | Events per type on 2018-01-01, with each share (`SUM(COUNT(*)) OVER ()`) |
| 7 | `sql/q02_top_starred.sql` | The day's 10 most-starred repositories, by `RANK()` |
| 7 | `sql/q03_top_merged.sql` | The 5 repositories with most merged pull requests, and the bot merges (`JSON_VALUE` on `payload`) |
| 7 | `sql/q04_daily_totals.sql` | Events, pushes and stars on 2018-01-01, and on 2018-01-02 before 06:00 UTC |
| 7 | `sql/q05_events_per_hour.sql` | Events per UTC hour of 2018-01-01, with `LAG` |
| 7 | `docs/budget.md` | Your `.bigqueryrc` lines, a dry-run estimate per query, and q04 with commits |
| 8 | `docs/budget.md` | The real bytes of each final run, and the AI move's bytes before and after |
| 8 | `docs/findings.md` | The five answers with numbers, beside your P9 numbers |
| 9 | `docs/budget.md` | The three q06 runs and the saving in per cent |
| 10 | `docs/budget.md` | The nested table: build, q07, q08 and the public dry run |
| 11 | `docs/budget.md` | The bytes of the summary, the view, the late day and the reader queries |
| 12 | `docs/budget.md` | The bytes billed per day this week, and the total |

## Files you create yourself

Tasks 9 to 12 create new files that have no stub here, on purpose: each brief names the file and says step by step what goes in it, and writing it is the task. Use the names the briefs give, in `gitpulse/bigquery/`:

- task 9: `sql/build_events.sql`, `sql/q06_stars_public.sql`, `sql/q06_stars_date.sql`, `sql/q06_stars_pruned.sql`, `docs/partitioning.md`;
- task 10: `sql/build_pushes.sql`, `sql/q07_commit_check.sql`, `sql/q07_commit_check_public.sql`, `sql/q08_top_committers.sql`;
- task 11: `sql/q09_daily_summary.sql`, `sql/build_daily_mv.sql`, `sql/append_20180108.sql`, `docs/serving.md`;
- task 12: `docs/compare.md`.

## What you still write yourself

- Every query: q01 to q09, the build files, the materialised view and the late day.
- Every number in `docs/budget.md`, and every answer in `docs/findings.md`.
- In task 8, step 3 asks Core students to write `bytes_report.sql`. Guided students get it complete (step 4): read it, make sure you can say what each column means, then run it as step 5 says.
- `gitpulse/README.md` in task 13. There is no README here: you update your own from P9, with two new headings, `## Part 1: Snowflake and dbt` and `## Part 2: BigQuery`.
- `evidence.md`, `AI_LOG.md` and `EXPLAIN.md` in the task folders.

## Data and licence

This starter holds no data. The queries read GH Archive's public day tables in BigQuery (`githubarchive.day.YYYYMMDD`); `~/de-kit/data/bigquery/README.md` lists their sizes and the scan budget. GH Archive states no licence; `~/de-kit/data/gharchive/README.md` explains what that means and what personal data to keep out. Credit it with this line: "Data: GH Archive (https://www.gharchive.org), a record of GitHub's public events."
