# Databricks notebook source
# MAGIC %md
# MAGIC # CycleCity silver: clean trips, one month at a time
# MAGIC Reads the bronze CSV files and writes one Delta table, `silver/trips`, partitioned by `month`.
# MAGIC Set the widget `month` to a month such as `202401`, or to `all` for every month in bronze.

# COMMAND ----------

# ruff: noqa: F821
# (spark and dbutils exist only inside Databricks; the line above tells ruff so.)

dbutils.widgets.text("month", "202401")

LAKE_ID = "<lake_id>"  # TODO(task 21): the lake_id from infra/variables.tf.
BRONZE = f"abfss://bronze@stcc{LAKE_ID}.dfs.core.windows.net/trips"
SILVER = f"abfss://silver@stcc{LAKE_ID}.dfs.core.windows.net"
GOLD = f"abfss://gold@stcc{LAKE_ID}.dfs.core.windows.net"

# COMMAND ----------


def load_month(m: str) -> int:
    """Clean one month of bronze trips, write it to silver, and return the rows written.

    Input: the CSV files under f"{BRONZE}/month={m}/", read with header=True. Every column
    arrives as text: ride_id is hex text before 2026 and a number from 2026, and times may
    or may not carry milliseconds.
    Output: Delta at f"{SILVER}/trips", partitioned by month. Only month m is replaced
    (replaceWhere on the month), so running the same month twice leaves its count unchanged.
    The cleaning the task checks:
    - started_at and ended_at cast with to_timestamp;
    - a month column (m) and duration_min;
    - drop trips that do not end after they start, or that last over 24 hours;
    - drop duplicate ride_id values.
    """
    raise NotImplementedError("TODO(task 21): clean and write one month")


# COMMAND ----------

# TODO(task 21): read the widget. For "all", call load_month for each month= folder that
#   dbutils.fs.ls(BRONZE) lists; otherwise call it for the widget's month. End with
#   dbutils.notebook.exit and the row count, so Data Factory sees it in the run output.
