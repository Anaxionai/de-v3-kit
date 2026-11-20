# The Glue Data Catalog and Athena.
#
# TODO(task 11): the Glue database cyclecity_<your_id> (your id with - changed to _).
# TODO(task 11): the Athena workgroup cyclecity-<your-id>: output location
#   s3://cyclecity-<your-id>-clean/athena-results/, the workgroup's settings enforced, and a
#   100 MB limit per query (bytes_scanned_cutoff_per_query = 104857600).
# TODO(task 11): the crawler cyclecity-<your-id>-raw on s3://cyclecity-<your-id>-raw/stations/status/
#   with table_prefix "raw_", and its role: AWSGlueServiceRole plus read on that prefix (reading a
#   prefix also needs s3:ListBucket on the bucket).
