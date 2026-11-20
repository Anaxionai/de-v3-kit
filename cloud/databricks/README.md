# Databricks Free Edition

In P7 (weeks 14 and 15) you run TaxiScale on Databricks Free Edition. You open the account in card 14 and use it in tasks 21 to 27. Free Edition is a no-cost Databricks workspace for learning. It sends no bill, so it has no budget alarm: its limit is a daily quota.

## Signing up

1. Open the Free Edition sign-up page from `https://www.databricks.com/learn/free-edition` (**Sign up for Free Edition**).
2. Choose a sign-up method: the page offers an existing Google or Microsoft account, or your email address. Use your **personal** email; Free Edition is for personal, non-commercial use.
3. Databricks creates a workspace for you and opens it.

What it costs: nothing. Databricks describes Free Edition as "provided at no cost to all users and perpetually free to use", with "No payment required" and "Forever free with daily limits on usage". The sign-up asks for no payment details.

Never share your password, and never create a personal access token for the course: nothing in P7 needs one.

## Limits

These are Databricks' published limits for Free Edition (last updated 18 October 2026):

| Limit | What it means for you |
|---|---|
| **Serverless compute only** | Databricks starts and sizes the compute for you. You cannot create your own cluster or change its size |
| **A daily fair-use quota** | "If you exceed your quota, your workspace's compute resources will be shut down and unavailable for the rest of the day." In extreme cases, for the rest of the month. **Your data and settings are kept** |
| **Outbound internet restricted to trusted domains** | A notebook cannot download the TLC trip files. You download them on your laptop and upload them (next section) |
| **5 concurrent job tasks per account** | A sixth job task waits until one finishes |
| **One SQL warehouse, size 2X-Small** | The smallest size |
| **One active pipeline per pipeline type** | P7 uses no pipelines |
| **No commercial use** | Use it for your own learning only. The centre does not run its own work on student accounts |
| **Inactive accounts may be deleted** | "Databricks may delete Free Edition accounts that are inactive for a prolonged period." Keep your notebooks as `.py` files in Git |

**When the quota runs out:** the notebook stops with a quota message. Nothing is lost. Continue the next day. To save quota, run each cell once, avoid loops that re-read all three months, and pause schedules (see "Schedules").

## Where things are

Run this in a notebook cell:

```sql
%sql
SELECT current_catalog(), current_schema();
```

Free Edition gives you a workspace catalog and a schema named `default`. The P7 briefs assume the catalog is named `workspace`. If yours has another name, use it in every path and command: `<catalog>.taxiscale`, `/Volumes/<catalog>/taxiscale/raw/`. The **Catalog** page in the sidebar shows it too.

## Uploading files to a volume

A volume is a Unity Catalog folder for files, with paths of the form `/Volumes/<catalog>/<schema>/<volume>/...`. P7 task 21 creates the volume `raw` in schema `taxiscale` first:

```sql
%sql
CREATE SCHEMA IF NOT EXISTS workspace.taxiscale;
CREATE VOLUME IF NOT EXISTS workspace.taxiscale.raw;
```

Then upload the files you downloaded on your laptop:

1. In the sidebar, click **New**, then **Add or upload data**.
2. Click **Upload files to a volume**.
3. Under **Files**, browse to the files or drag them into the drop zone. For P7, the three Parquet files in `taxiscale/data/yellow/`.
4. Under **Destination volume**, choose the volume and a folder, or paste a path such as `/Volumes/workspace/taxiscale/raw/yellow/`. You can create a folder inside the volume here. If no volume exists, **Create volume** makes one.
5. Click **Upload**.

The upload page accepts files **up to 5 GB each**. The P7 files are 50 to 60 MB each. If an upload stops, upload that file again.

Check what arrived:

```sql
%sql
LIST '/Volumes/workspace/taxiscale/raw/yellow/'
```

## Serverless: what is different from your Spark container

| On your laptop's Spark | On Free Edition's serverless compute |
|---|---|
| Spark UI on `localhost:4040` | No Spark UI. Under a cell, click **See performance**, then the statement, then **See query profile** |
| Any Spark setting | Only six settings: `spark.sql.shuffle.partitions`, `spark.sql.session.timeZone`, `spark.sql.ansi.enabled`, `spark.sql.files.maxPartitionBytes`, `spark.sql.legacy.timeParserPolicy` and `spark.databricks.execution.timeout`. Card 14 asks you to try another one and note what happens |
| RDDs and `spark.sparkContext` | Not available: use DataFrames and SQL |
| `input_file_name()` | Not supported: select `_metadata.file_name` instead |
| No time limit | A notebook query stops after 9,000 seconds (2.5 hours) by default |

## Exporting a notebook as a `.py` file

AxReview reads `.py` files, never `.ipynb`. After each Databricks task:

1. In the notebook, click **File**, then **Export**, then **Source file**.
2. Your browser downloads `<notebook name>.py`. Move it into `taxiscale/notebooks/`, for example `taxiscale/notebooks/taxiscale_setup.py`.
3. Check it in Git Bash:

```bash
head -1 taxiscale/notebooks/taxiscale_setup.py
```

The first line is `# Databricks notebook source`. Cells are separated by lines `# COMMAND ----------`.

## Schedules

P7 task 26 schedules `taxiscale_daily` as a job, proves one run, then pauses it. A paused schedule uses no quota.

- To run it once: in the job's **Schedules & Triggers** section, or the Schedules dialog of the notebook, choose **Run now**.
- To pause it: in the job details, under **Schedules & Triggers**, click **Pause**. Runs already started finish; no new run starts. **Resume** starts it again on the same schedule.
- At most 5 job tasks run at the same time on one account.

Leave the job paused when P7 ends. Nothing else needs tearing down: Free Edition never bills you. The P7 checklist in [`../teardown.md`](../teardown.md) lists what to check.

## Sources, checked 13 November 2026

- Databricks Free Edition (Databricks docs, 11 September 2026): https://docs.databricks.com/aws/en/getting-started/free-edition
- Free Edition limitations (Databricks docs, 18 October 2026): https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- Free trial and Free Edition compared (Databricks docs): https://docs.databricks.com/aws/en/getting-started/free-trial-vs-free-edition
- Databricks Free Edition (Databricks): https://www.databricks.com/learn/free-edition
- Upload files to a Unity Catalog volume (Databricks docs): https://docs.databricks.com/aws/en/ingestion/file-upload/upload-to-volume
- Unity Catalog volumes (Databricks docs): https://docs.databricks.com/aws/en/volumes/
- Set Spark configuration properties, serverless list (Databricks docs, 11 September 2026): https://docs.databricks.com/aws/en/spark/conf
- Serverless compute for notebooks (Databricks docs): https://docs.databricks.com/aws/en/compute/serverless/notebooks
- Export and import notebooks (Databricks docs): https://docs.databricks.com/aws/en/notebooks/notebook-export-import
- Schedule a notebook job (Databricks docs): https://docs.databricks.com/aws/en/notebooks/schedule-notebook-jobs
- Scheduled triggers for jobs (Databricks docs, 6 November 2026): https://docs.databricks.com/aws/en/jobs/scheduled
- Automating jobs with triggers, pause and resume (Databricks docs): https://docs.databricks.com/aws/en/jobs/triggers
