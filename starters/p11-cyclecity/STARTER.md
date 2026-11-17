# Guided starter: P11 CycleCity part 2 (AWS)

This starter is an **add-on** to your own `cyclecity/` folder from P10: only the new `aws/`
folder that module 13 builds, with the set-up done and every resource, policy, query and line of
logic left for you as a TODO. It replaces no file you already have; P10's files stay as they are.

## What is included

| Path | What it is |
|---|---|
| `aws/.gitignore` | `*.zip` and `out.json` (P10's `.gitignore` already keeps Terraform state out) |
| `aws/infra/providers.tf`, `variables.tf`, `terraform.tfvars` | `hashicorp/aws` and `hashicorp/archive` at the versions in `~/de-kit/VERSIONS.md`; path-style S3 and the two `skip_` settings in the `emulator` workspace only; `student_id` and `region` |
| `aws/infra/s3.tf`, `lambda.tf`, `iam_ingest.tf`, `catalog.tf`, `secrets.tf`, `glue_job.tf`, `sfn.tf` | One file per part, with TODOs only. No resources yet |
| `aws/lambda/ingest.py` | `fetch`, `find_feed`, `select_new`, `read_watermark`, `write_watermark`, `land_month`, `send_alert`, `handler`, the two exceptions and the `__main__` block, as stubs |
| `aws/tests/test_ingest.py` | One example test of `select_new` with three hand-made stations, skipped until task 9 |
| `aws/athena/run_query.py`, `bytes_report.py` | Script skeletons (tasks 11, 26) |
| `aws/athena/q00_*.sql` ... `q21_*.sql` | One file per statement, with its question and a TODO; `q00` lists the 13 trip columns, `q20` the Iceberg columns and types |
| `aws/glue/clean_job.py` | Glue boilerplate with the Iceberg settings on the `SparkConf`, and TODOs for the logic |
| `aws/sfn/pipeline.asl.json` | The state names as an outline of `Pass` states. It is valid JSON, not yet a valid state machine: `Alert` and `Fail` become reachable when task 23 adds the `Catch` fields |
| `aws/emulator/` | `redshift-trust.json`, and stubs for `produce.py`, `consume.py`, `redshift_load.py`, `NOTES.md` |
| `aws/docs/` | `access.md`, `scan-savings.md`, `merge.md`, `access-review.md`, `cost.md` with their headings |

`evidence.md` and `AI_LOG.md` live in the task folder, next to `cyclecity/`. You write
`aws/docs/usage-only.json` in task 26 (step 2 gives its one line), and the README for both
clouds in task 28.

## Copy it in

In task 8, first copy your `cyclecity/` folder forward as the brief says (or the catch-up copy
your mentor gave you). Then, in Git Bash, inside the same task folder:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p11-cyclecity/aws cyclecity/
```

Copy it once, before you make any `aws/` folder yourself: if `cyclecity/aws/` already exists,
`cp -r` puts a second `aws/` inside it. From task 9 on, copy your `cyclecity/` folder forward as
each brief says.

## What the starter has done, task by task

- **Task 8:** steps 2, 3 and 4 are done (`aws/infra/`, `aws/.gitignore`, the provider, the
  variables and the emulator settings). Put your id in `aws/infra/terraform.tfvars`, then write
  `s3.tf` (steps 5 and 6). `providers.tf` already has `hashicorp/archive` for task 9, so your
  first `terraform init` installs both, and task 9's second `terraform init` changes nothing.
- **Task 9, step 1:** the starter does not change your `pyproject.toml`. Run the brief's
  commands in `cyclecity/`: `uv add boto3`, `uv add --dev pytest`, then add these lines to
  `pyproject.toml`:

  ```toml
  [tool.pytest.ini_options]
  pythonpath = [".", "aws/lambda"]
  ```
- **Task 11, step 7:** the `__main__` block already sends `ingest.py trips <month>` to
  `land_month`; you write `land_month` itself.
- **Task 24, step 1:** run `uv add "psycopg[binary]"` in `cyclecity/`, as the brief says.

## How to run it

From `cyclecity/`, after task 9 step 1:

```bash
uv run pytest            # 1 skipped until you remove the skip in task 9
uvx ruff check aws       # optional: lint the new files
```

Terraform, from `cyclecity/aws/infra/`, as task 8 shows. Check the target before every apply:

```bash
export AWS_PROFILE=emulator          # or cyclecity for AWS
terraform workspace show             # emulator with emulator, default with cyclecity
terraform init
terraform plan
```

As shipped, `terraform plan` has nothing to add. Without the two `skip_` settings in
`providers.tf`, the emulator apply fails: the provider would read bucket tags from
`000000000000.localhost`, which Windows cannot resolve. On AWS (`default`) all three are off.

## Your TODOs

Find them with `grep -rn "TODO(task" cyclecity/aws`.

| Task | File | What you write |
|---|---|---|
| 8 | `infra/terraform.tfvars`, `infra/s3.tf` | Your id; both buckets, public access blocks, the 7-day rule |
| 9 | `lambda/ingest.py` | `fetch`, `find_feed`, `select_new`, the watermark functions, `handler` |
| 9 | `tests/test_ingest.py` | Remove the skip; a second test, at the watermark |
| 9 | `infra/lambda.tf`, `infra/iam_ingest.tf` | Zip, function, log group, hourly rule and permission; the wide role |
| 10 | `infra/iam_ingest.tf`, `docs/access.md` | The `stations/*` policy; calls, AI draft, removals |
| 11 | `infra/catalog.tf` | Glue database, workgroup, crawler and its role |
| 11 | `lambda/ingest.py` | `land_month` |
| 11 | `athena/run_query.py`, `q00`, `q09`, `q01`, `q02` | The runner; the table, its partitions, two questions |
| 12 | `athena/q10` to `q13`, `docs/scan-savings.md` | CTAS and three versions of one question; the cost table |
| 13 | `infra/secrets.tf`, `lambda.tf`, `iam_ingest.tf` | The secret, `ALERT_SECRET_ID`, the one permission |
| 13 | `lambda/ingest.py` | `send_alert`, and the alert paths in `handler` |
| 21 | `athena/q20_create_trips.sql`, `q21_check_trips.sql` | The Iceberg table; the check |
| 21 | `glue/clean_job.py`, `infra/glue_job.tf` | Read, cast, filter, de-duplicate, hash, write; the job and its role |
| 22 | `glue/clean_job.py`, `infra/glue_job.tf`, `docs/merge.md` | `--month` and the `MERGE`; the default argument; why `row_hash` |
| 23 | `lambda/ingest.py`, `infra/iam_ingest.tf` | `FeedUnavailable`, `month` and `base_url` in `handler`; `trips/*` |
| 23 | `sfn/pipeline.asl.json`, `infra/sfn.tf` | The real states; the state machine and its role |
| 24 | `emulator/produce.py`, `consume.py`, `redshift_load.py`, `NOTES.md` | Kinesis and Redshift on the emulator |
| 25 | `docs/access-review.md` | The review, and the one permission you remove in `infra/` |
| 26 | `athena/bytes_report.py`, `docs/cost.md` | The byte total; the two bills side by side and one more month |

Task 27 (the teardown) writes no code: it runs `terraform destroy` and pastes listings. Task 28
(the wrap-up) has no TODO: the README for both clouds, `NEXT.md`, the demo and `EXPLAIN.md` are
all yours.

## What you still write yourself

- Every Terraform resource and policy, every function body, query, job step and state.
- The `pyproject.toml` lines above, `evidence.md`, `AI_LOG.md` and `EXPLAIN.md` in the task
  folders, `aws/docs/usage-only.json`, the `## Part 2` note in `NEXT.md` (task 8), and the README
  (task 28).

No key, password or webhook address goes in any file: the webhook lives in
`~/cyclecity-webhook.txt` and in Secrets Manager only. The trip files and the station feed come
from the operator (`~/de-kit/data/bikes/README.md`); this starter holds no data. CycleCity is not
affiliated with Citi Bike or Lyft.
