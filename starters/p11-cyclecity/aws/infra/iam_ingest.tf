# The ingest function's role: cyclecity-${var.student_id}-ingest-role, trusted by lambda.amazonaws.com.
#
# TODO(task 9): the role, with AWSLambdaBasicExecutionRole and an inline policy that allows
#   s3:GetObject and s3:PutObject on the raw bucket. Wide on purpose: task 10 narrows it.
# TODO(task 10): replace both with an aws_iam_policy_document: s3:GetObject and s3:PutObject on
#   the stations/ prefix of the raw bucket only, and logs:CreateLogStream and logs:PutLogEvents on
#   the function's own log group (its ARN followed by :*). No managed policy and no * action.
# TODO(task 13): allow secretsmanager:GetSecretValue on the alert secret's ARN, and nothing else.
# TODO(task 23): allow s3:PutObject on the trips/ prefix of the raw bucket too: the second prefix
#   the function writes, granted when the code needs it.
