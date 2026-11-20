# The ingest function, its log group and its hourly schedule.
#
# TODO(task 9): zip ../lambda/ingest.py with data "archive_file" (output_path inside this folder;
#   aws/.gitignore keeps *.zip out of Git). archive_file comes from the hashicorp/archive provider
#   in providers.tf: run terraform init again if init ran before it was there.
# TODO(task 9): the function cyclecity-${var.student_id}-ingest: handler ingest.handler, the Python
#   runtime in ~/de-kit/VERSIONS.md, 256 MB, 60 seconds, environment variable RAW_BUCKET, and
#   source_code_hash from the zip, so that apply redeploys changed code.
# TODO(task 9): a log group /aws/lambda/<the function's name> that keeps logs for 7 days.
# TODO(task 9): an EventBridge rule cyclecity-${var.student_id}-hourly with rate(1 hour), a target
#   that is the function, and a Lambda permission that lets EventBridge invoke it.
# TODO(task 13): add ALERT_SECRET_ID (the secret's name) to the function's environment.
