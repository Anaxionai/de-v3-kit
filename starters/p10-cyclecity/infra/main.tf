# CycleCity's Azure resources. Each task adds its part under its TODO, in this order.
# Names come from var.student_id (and var.lake_id for the storage account).
# Run Terraform only in the newest copy of cyclecity/: the state file travels with the folder.

# TODO(task 8): an azurerm_resource_group named rg-cyclecity-${var.student_id} in var.location.

# TODO(task 9): an azurerm_storage_account with the label lake, named stcc${var.lake_id}:
#   Standard tier, LRS replication, hierarchical namespace on.
# TODO(task 9): three azurerm_storage_container blocks, bronze, silver and gold, each linked to the
#   account with storage_account_id (the older storage_account_name argument is gone).

# TODO(task 10): data "azurerm_client_config" "current", whose object_id is you and tenant_id
#   is your directory.
# TODO(task 10): an azurerm_data_factory named adf-cyclecity-${var.student_id} with a
#   SystemAssigned identity.
# TODO(task 10): two azurerm_role_assignment blocks: the factory's identity gets Storage Blob Data
#   Contributor on the bronze container only; you get Storage Blob Data Reader on the account.

# TODO(task 11): an azurerm_key_vault named kv-cc-${var.student_id}: standard SKU, your tenant_id,
#   Azure roles for access (rbac_authorization_enabled), soft-delete retention of 7 days.
# TODO(task 11): two role assignments on the vault: you get Key Vault Secrets Officer, the
#   factory's identity gets Key Vault Secrets User. The secret itself is set with the Azure CLI,
#   never in Terraform (the state file would hold its value).

# TODO(task 20): an azurerm_databricks_workspace named dbw-cyclecity-${var.student_id} on the
#   trial SKU, with managed resource group rg-cyclecity-${var.student_id}-dbx.

# TODO(task 21): an azurerm_databricks_access_connector named ac-cyclecity-${var.student_id}
#   with a SystemAssigned identity.
# TODO(task 21): four role assignments for the connector's identity: Storage Blob Delegator on the
#   account, Storage Blob Data Reader on bronze, Storage Blob Data Contributor on silver and on gold.

# TODO(task 22): the factory's identity gets Contributor on the Databricks workspace.
