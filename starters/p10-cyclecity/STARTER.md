# Guided starter: P10 CycleCity

This folder is the start of your `cyclecity/` product folder for module 12 (Azure). It saves you the set-up: the Terraform provider and variables, one TODO per task in `main.tf` and `outputs.tf`, the Python check's skeleton, the two Databricks notebooks with their paths and stubs, and the docs pages with their headings. Every resource, role, notebook step and answer is still yours to write.

## What is included

| Path | What it is |
|---|---|
| `infra/providers.tf` | The `azurerm` provider at the version in `~/de-kit/VERSIONS.md`, with `features {}` |
| `infra/variables.tf` | `student_id`, `location` (`centralindia`) and `lake_id` |
| `infra/main.tf`, `infra/outputs.tf` | One TODO per task, in task order. No resources yet |
| `cyclecity/__init__.py`, `cyclecity/check_secret.py` | The Key Vault check's skeleton (task 11) |
| `notebooks/silver.py`, `notebooks/gold.py` | Databricks source-format notebooks: the `month` widget, the lake paths and stubs (tasks 21, 24) |
| `adf/`, `databricks/` | Empty: the JSON you export from Data Factory and the cluster lands here |
| `docs/access.md`, `answers.md`, `serving.md`, `cost.md` | Headings and TODOs (tasks 10, 24, 25, 26) |
| `fabric/queries.sql` | The two T-SQL queries of task 25, as TODOs |
| `.env.example` | `KEY_VAULT_URL`, filled in task 11 |
| `.gitignore` | `.terraform/`, `*.tfstate`, `*.tfstate.*`, `.env`, `.venv/`, `data/` |
| `.python-version` | Python 3.12, for task 11 |

There is no `pyproject.toml` on purpose: task 11 step 6 makes it with `uv init --bare`, which refuses to run where one exists. `evidence.md` and `AI_LOG.md` live in the task folder, next to `cyclecity/`. You write `cyclecity/README.md` in task 27.

## Copy it in

In task 8 (Open the account, set a budget alarm and create the resource group), start from this starter instead of an empty folder. In Git Bash, inside the task folder:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p10-cyclecity cyclecity
```

In task 8, `providers.tf`, `variables.tf` and `.gitignore` are ready: set your id in `variables.tf`, then write the resource group in `main.tf` (steps 5 to 8). From task 9 on, copy your `cyclecity/` folder forward with `cp -r` as each brief says, so `infra/terraform.tfstate` comes too.

## How to run it

Terraform, from `cyclecity/infra/`:

```bash
terraform init      # the first time; cp -r brings .terraform/ along to later copies
terraform plan
terraform apply
```

With the starter as shipped, `terraform plan` has nothing to add: every resource is still a TODO.

The Key Vault check, from `cyclecity/`, after task 11 step 6 (`uv init --bare --python 3.12`, then `uv add azure-identity azure-keyvault-secrets`):

```bash
KEY_VAULT_URL=$(terraform -chdir=infra output -raw key_vault_uri) uv run python -m cyclecity.check_secret
```

The notebooks: the briefs say "create notebook `silver` in `Shared/cyclecity`". To start from the starter's file instead, open Workspace, Shared, create the folder `cyclecity`, then on that folder choose Import, File, and pick `notebooks/silver.py`. Databricks reads the first line, `# Databricks notebook source`, and makes a notebook named `silver`. Do the same with `gold.py` in task 24. When a task says "Export the notebook (File, Export, Source file)", save the export over the starter's file.

Data Factory (tasks 12, 13, 22, 23): you build the pipelines in ADF Studio and save them with `az datafactory ... list` or `show` into `adf/`. There is no stub for them: the exported JSON is your work.

## Your TODOs

Find them with `grep -rn "TODO(task" cyclecity`.

| Task | File | What you write |
|---|---|---|
| 8 | `infra/variables.tf` | Your id |
| 8 | `infra/main.tf` | The resource group |
| 9 | `infra/variables.tf`, `infra/main.tf` | `lake_id`; the storage account `lake` and three containers |
| 10 | `infra/main.tf`, `infra/outputs.tf` | Client config, data factory, two role assignments; `adf_principal_id` |
| 10 | `docs/access.md` | The access table and what the factory cannot do |
| 11 | `infra/main.tf`, `infra/outputs.tf` | Key vault and two role assignments; `key_vault_uri` |
| 11 | `cyclecity/check_secret.py`, `.env.example` | The check; the vault address |
| 20 | `infra/main.tf`, `infra/outputs.tf` | The Databricks workspace; `databricks_url` |
| 21 | `infra/main.tf`, `infra/outputs.tf` | Access connector and four role assignments; `access_connector_id` |
| 21 | `notebooks/silver.py` | `LAKE_ID`, `load_month`, the month loop |
| 22 | `infra/main.tf` | Contributor for the factory on the workspace |
| 24 | `notebooks/gold.py` | Grains, `station_day`, `station_hour`, the writes, Q1 to Q3, the check |
| 24 | `docs/answers.md` | The three answers with numbers and actions |
| 25 | `fabric/queries.sql`, `docs/serving.md` | Two T-SQL queries; copy or shortcut |
| 26 | `docs/cost.md` | The cost by service, the biggest cost, one saving |

Tasks with no TODO here, and why:
- Tasks 12, 13 and 23 are built in ADF Studio and saved as exported JSON in `adf/` (task 23 also adds the drill line to your workspace's `silver` notebook, then removes it).
- Task 20's cluster is made in the Databricks UI and saved as `databricks/cluster.json`.
- Task 27 (the wrap-up): the README, the demo and `EXPLAIN.md` are all yours.

## What you still write yourself

- Every Terraform resource, role assignment and output, and every notebook's logic and queries.
- `pyproject.toml` and `uv.lock` (task 11), the pipelines in Data Factory, and the exported JSON.
- `evidence.md`, `AI_LOG.md` and `EXPLAIN.md` in the task folders, and `cyclecity/README.md` (task 27).

No key, SAS token, connection string or webhook address goes in any file in this folder. The trip data comes from the Citi Bike system data page; the pipelines download it into your storage account, and this starter holds none. CycleCity is not affiliated with Citi Bike or Lyft.
