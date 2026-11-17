# CycleCity's AWS half (P11). This aws/infra/ folder serves two targets, chosen by the workspace:
#   workspace emulator  ->  the laptop emulator  (export AWS_PROFILE=emulator)
#   workspace default   ->  your AWS account     (export AWS_PROFILE=cyclecity)
# The provider takes the credentials, and the emulator's endpoint_url, from the AWS CLI profile.
# Check both before every apply: echo $AWS_PROFILE and terraform workspace show.
# Run Terraform for AWS only in this folder: cyclecity/infra/ is your P10 Azure code.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.73.0"
    }
    # archive_file zips the Lambda code (task 9).
    archive = {
      source  = "hashicorp/archive"
      version = "2.8.1"
    }
  }
}

provider "aws" {
  region = var.region
  # The emulator serves buckets by path (localhost:4566/<bucket>), not by host name.
  s3_use_path_style = terraform.workspace == "emulator"
  # On the emulator only: no account id. With an account id, this provider reads bucket tags
  # from <account-id>.localhost, a name Windows cannot resolve, and the apply fails.
  skip_requesting_account_id  = terraform.workspace == "emulator"
  skip_credentials_validation = terraform.workspace == "emulator"
}
