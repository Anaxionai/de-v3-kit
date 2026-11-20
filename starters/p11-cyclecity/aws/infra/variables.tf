variable "student_id" {
  description = "Your GitHub username in lower case. Every resource name contains it."
  type        = string
}

variable "region" {
  description = "The AWS region for every CycleCity resource on AWS."
  type        = string
  default     = "ap-south-1"
}
