# CycleCity's two buckets on AWS. Bucket names are global, so they carry your id:
#   cyclecity-<your-id>-raw    stations/status/, stations/state/ (the watermark), trips/month=YYYYMM/
#   cyclecity-<your-id>-clean  athena-results/, trips_parquet/, iceberg/, scripts/
#
# TODO(task 8): both buckets, named from var.student_id, with force_destroy = true.
# TODO(task 8): a public access block on each bucket, with all four options set to true.
# TODO(task 8): a lifecycle configuration on the clean bucket that expires objects under
#   athena-results/ after 7 days.
