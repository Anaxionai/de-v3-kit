"""CycleCity clean job: raw trip CSV files into the Iceberg table trips (AWS Glue, Spark).

It is your P10 silver notebook as a job. It runs on AWS only: Terraform uploads it to
s3://cyclecity-<your-id>-clean/scripts/clean_job.py (aws/infra/glue_job.tf), and the job runs
with --datalake-formats iceberg.
"""

import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

# TODO(task 21): your id in these three names (the database uses _ where your id has -).
RAW_TRIPS = "s3://cyclecity-<your-id>-raw/trips/"
WAREHOUSE = "s3://cyclecity-<your-id>-clean/iceberg/"
TABLE = "glue_catalog.cyclecity_<your_id>.trips"

# TODO(task 22): also read the job argument --month ("all", or one month such as 202404).
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

# The Iceberg settings from the Glue Iceberg page. They must be on the SparkConf before the
# SparkContext exists: settings added later are ignored.
conf = SparkConf()
conf.set(
    "spark.sql.extensions",
    "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
)
conf.set("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog")
conf.set("spark.sql.catalog.glue_catalog.warehouse", WAREHOUSE)
conf.set(
    "spark.sql.catalog.glue_catalog.catalog-impl",
    "org.apache.iceberg.aws.glue.GlueCatalog",
)
conf.set("spark.sql.catalog.glue_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")

sc = SparkContext(conf=conf)
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# TODO(task 21): read RAW_TRIPS as CSV with header=True. Every column arrives as text, and Spark
#   reads the month= folders as a number column.
# TODO(task 22): read only the folder month=<month> when --month is a month, every folder when it
#   is all. Add .option("basePath", RAW_TRIPS) to the read: without it, Spark drops the month
#   column when it reads one month= folder.
# TODO(task 21): cast month to string and the four coordinates to double. Add duration_min as in
#   P10's notebooks/silver.py.
# TODO(task 21): cast started_at and ended_at with .cast("timestamp_ntz"): local times with no time
#   zone, like the table's timestamp columns.
# TODO(task 21): drop trips that do not end after they start, or that last over 24 hours.
# TODO(task 21): keep one row per ride_id. Add row_hash: sha2 of the 13 raw text columns joined by
#   "|" (concat_ws), 256 bits. Print the row counts before and after cleaning.
# TODO(task 21): select the columns in the order of aws/athena/q20_create_trips.sql and write with
#   df.writeTo(TABLE).append().
# TODO(task 22): replace the append with a temporary view updates and a MERGE INTO TABLE on ride_id
#   and month: update every column only when row_hash differs, insert when not matched.

job.commit()
