# Every CycleCity resource name is built from these values (see the TODOs in main.tf).

variable "student_id" {
  description = "Your GitHub username in lower case. Resource names contain it."
  type        = string
  default     = "<your-id>" # TODO(task 8): put your id here.
}

variable "location" {
  description = "The Azure region for every CycleCity resource."
  type        = string
  default     = "centralindia"
}

variable "lake_id" {
  description = "The storage account name is stcc + lake_id: lower-case letters and digits only, at most 20 characters."
  type        = string
  default     = "<your-id>" # TODO(task 9): your id without hyphens; add two digits if the name is taken.
}
