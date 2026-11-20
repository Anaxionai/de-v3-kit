# CycleCity's Terraform settings: the azurerm provider at the version in ~/de-kit/VERSIONS.md.
# Terraform signs in through the Azure CLI (az login) and uses its default subscription.
# The state stays in infra/terraform.tfstate on your laptop; .gitignore keeps it out of Git.
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "5.13.0"
    }
  }
}

# features {} is required. Leave the Key Vault defaults alone: terraform destroy then purges the
# vault, so its name is free again for your next run.
provider "azurerm" {
  features {}
}
