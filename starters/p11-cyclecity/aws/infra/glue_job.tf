# The clean job. It runs on AWS only: the emulator stores Glue jobs but never runs their scripts.
#
# TODO(task 21): upload ../glue/clean_job.py with aws_s3_object to scripts/clean_job.py in the clean
#   bucket, with etag = filemd5(<the script>), so that apply uploads a changed script.
# TODO(task 21): the job cyclecity-<your-id>-clean from that script: the Glue version in
#   ~/de-kit/VERSIONS.md, worker type G.1X, 2 workers, timeout 10, max_retries 0, and the job
#   argument --datalake-formats set to iceberg.
# TODO(task 21): the role cyclecity-<your-id>-glue-role: AWSGlueServiceRole, s3:ListBucket, read on
#   trips/ and on the script, read and write on iceberg/ (Iceberg reads its own metadata there).
# TODO(task 22): add "--month" = "all" to the job's default arguments.
