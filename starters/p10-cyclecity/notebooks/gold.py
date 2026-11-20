# Databricks notebook source
# MAGIC %md
# MAGIC # CycleCity gold: station demand
# MAGIC Builds `station_day` and `station_hour` from silver, writes them to `gold` as Delta (and once as
# MAGIC Parquet under `gold/export/` for Fabric), and answers the operations team's three questions.

# COMMAND ----------

# ruff: noqa: F821
# (spark and dbutils exist only inside Databricks; the line above tells ruff so.)

LAKE_ID = "<lake_id>"  # TODO(task 24): the lake_id from infra/variables.tf.
SILVER = f"abfss://silver@stcc{LAKE_ID}.dfs.core.windows.net"
GOLD = f"abfss://gold@stcc{LAKE_ID}.dfs.core.windows.net"

# The silver table from task 21.
trips = spark.read.format("delta").load(SILVER + "/trips")

# COMMAND ----------

# MAGIC %md
# MAGIC ## station_day
# MAGIC TODO(task 24): write the grain of station_day here, in one sentence.

# COMMAND ----------


def station_day(trips):
    """Return the station_day DataFrame built from the silver trips DataFrame.

    Departures: count trips by start_station_id and the date of started_at.
    Arrivals: count trips by end_station_id and the date of ended_at.
    Full-outer-join the two on station and day, fill missing counts with 0, add
    net_flow = arrivals - departures, and keep a station_name (one consistent choice).
    The check in step 9: total departures must equal the number of silver rows, so trips
    with an empty start_station_id need a group of their own.
    """
    raise NotImplementedError("TODO(task 24): build station_day as the docstring says")


# COMMAND ----------

# MAGIC %md
# MAGIC ## station_hour
# MAGIC TODO(task 24): write the grain of station_hour here, in one sentence.

# COMMAND ----------


def station_hour(trips):
    """Return station_hour: the same counts as station_day, by station, day and hour."""
    raise NotImplementedError("TODO(task 24): build station_hour")


# COMMAND ----------

# TODO(task 24): write both tables as Delta to f"{GOLD}/station_day" and f"{GOLD}/station_hour"
#   with mode("overwrite"), and each once as Parquet to f"{GOLD}/export/<table>" for task 25.

# COMMAND ----------

# TODO(task 24): Q1, the 5 stations with the most departures in the latest full month, and their
#   departures in the same month a year before.
# TODO(task 24): Q2, on weekday mornings (07:00 to 09:59), the 5 stations that lose the most bikes
#   per day on average.
# TODO(task 24): Q3, for each day of the week, the hour with the most departures across all
#   stations, and how many on average.
# TODO(task 24): the check, total departures in station_day next to the number of silver rows.
