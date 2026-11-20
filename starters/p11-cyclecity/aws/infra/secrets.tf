# The alert webhook's secret. Terraform creates the secret only: its value is put with the AWS CLI
# from a file outside the repository, because Terraform state would hold any value set here.
#
# TODO(task 13): aws_secretsmanager_secret cyclecity-<your-id>-alert-webhook with
#   recovery_window_in_days = 0, and no secret version.
