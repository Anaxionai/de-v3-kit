# Teardown: leave nothing running

A cloud project is finished only when its bill has stopped. The last build task of each cloud project tears it down and pastes two things into `evidence.md`: **the empty listings** and **the cost so far**.

Before any teardown:

1. **Record your demo and take your screenshots first.** After the teardown the data is gone.
2. Check that every number your wrap-up needs is already in your evidence files.
3. **Keep the budget alarm** (or the Snowflake monitor). It costs nothing and still warns you if something was missed.

| Project | Platform | Teardown task | Week |
|---|---|---|---|
| P7 TaxiScale | Databricks Free Edition | task 26 pauses the schedule (no teardown task) | 15 |
| P9 GitPulse | Snowflake | task 27 | 18 |
| P10 CycleCity | Azure (and Fabric) | task 26 | 20 |
| P11 CycleCity part 2 | AWS (and the emulator) | task 27 | 22 |
| P12 GitPulse part 2 | BigQuery | task 12 | 23 |

## Databricks Free Edition (P7)

Free Edition never bills you, so nothing must be deleted. Check three things at the end of week 15:

- [ ] The job `taxiscale_daily_<your-id>` is **paused**: in the job details, **Schedules & Triggers** shows **Resume**, not **Pause**.
- [ ] Every notebook you used is exported as a `.py` file in `taxiscale/notebooks/` and pushed. Databricks may delete Free Edition accounts that stay inactive for a long time.
- [ ] No personal access token exists: your user settings, **Developer**, **Access tokens** lists none.

Optional: drop the practice objects with `DROP SCHEMA IF EXISTS workspace.taxiscale_reports CASCADE;` and `DROP SCHEMA IF EXISTS workspace.taxiscale CASCADE;`. This deletes the tables and the uploaded files. Keep them if you want to show them in an interview.

## Snowflake (P9 task 27)

Work in this order, in a Snowsight worksheet as `ACCOUNTADMIN` (or with `snow sql --role ACCOUNTADMIN`).

1. **Record the demo first.**
2. **Export what you built:**
   ```sql
   SELECT GET_DDL('DATABASE', 'GITPULSE', TRUE);
   ```
   Copy the result into `gitpulse/snowflake/99_export_ddl.sql`.
3. **Read the credits per warehouse:**
   ```sql
   SELECT warehouse_name, SUM(credits_used) AS credits
   FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
   GROUP BY warehouse_name ORDER BY credits DESC;
   ```
   This view can be up to 3 hours behind. Also note the free balance left, from the tile in Snowsight's left navigation bar.
4. **Stop the task:** `ALTER TASK GITPULSE.RAW.FLATTEN_NEW_EVENTS SUSPEND;`
5. **Drop everything GitPulse made** (`gitpulse/snowflake/16_teardown.sql`):
   ```sql
   DROP DATABASE IF EXISTS GITPULSE_CI;
   DROP DATABASE GITPULSE;
   DROP DATABASE SCRATCH;
   DROP WAREHOUSE GITPULSE_WH;
   DROP USER GITPULSE_CI;
   DROP ROLE GITPULSE_LOADER;
   DROP ROLE GITPULSE_TRANSFORMER;
   DROP ROLE GITPULSE_READER;
   ALTER WAREHOUSE COMPUTE_WH SUSPEND;
   ```
   The last line fails if `COMPUTE_WH` is already suspended. That is fine.
6. **Keep the resource monitor** `GITPULSE_MONITOR`. It costs nothing.
7. **Prove it is empty:**
   ```sql
   SHOW DATABASES LIKE 'GITPULSE%';
   SHOW WAREHOUSES;
   SHOW TASKS IN ACCOUNT;
   SHOW USERS LIKE 'GITPULSE%';
   ```
   **Empty looks like this:** the first, third and fourth return no rows (Snowsight says the query produced no results). `SHOW WAREHOUSES` returns one row: `COMPUTE_WH`, with `state` `SUSPENDED`.
8. **Remove the CI secrets and keys:** in the `gitpulse-dbt` repository on GitHub, **Settings**, **Secrets and variables**, **Actions**: delete `SNOWFLAKE_ACCOUNT` and `SNOWFLAKE_CI_PRIVATE_KEY`. Then:
   ```bash
   rm ~/snowflake-keys/gitpulse_ci_key.p8 ~/snowflake-keys/gitpulse_ci_key.pub
   ```

**The cost so far:** total the credits from step 3 and convert them at **USD 2.20 a credit** (Standard, AWS Mumbai), about **₹209** at ₹95 to the dollar. Example: 3.4 credits × ₹209 = ₹710.60 of free usage. You pay nothing: the trial's USD 400 covers it.

Dropped databases stay in Time Travel for 1 day and in Fail-safe for 7 days, with very small storage. The trial suspends itself 30 days after sign-up, in week 21; you do not need to cancel it.

## Azure (P10 task 26)

Work in the newest copy of `cyclecity/`, in `cyclecity/infra/`.

1. **Record the demo first.**
2. **Destroy:**
   ```bash
   terraform plan -destroy
   terraform destroy
   ```
   Read the plan: every CycleCity resource is listed. Type `yes`. The last line is `Destroy complete! Resources: N destroyed.` If the workspace fails to delete, wait 10 minutes and run `terraform destroy` again.
3. **Prove the state is empty:**
   ```bash
   terraform state list
   ```
   **Empty looks like this:** the command prints nothing.
4. **Prove no group is left:**
   ```bash
   az group list -o table
   ```
   Neither `rg-cyclecity-<your-id>` nor `rg-cyclecity-<your-id>-dbx` may appear. With no groups at all, the command prints nothing.
5. **Prove no resource is left:**
   ```bash
   az resource list -o table
   ```
   If it lists `NetworkWatcher_centralindia`, Azure made it in group `NetworkWatcherRG` when the Databricks network was created. Delete the group and list again:
   ```bash
   az group delete -n NetworkWatcherRG --yes
   ```
   **Empty looks like this:** the command prints nothing.
6. **Purge the deleted key vault.** A deleted vault is kept for a while (soft delete) and holds its name:
   ```bash
   az keyvault list-deleted -o table
   az keyvault purge -n kv-cc-<your-id>
   az keyvault list-deleted -o table
   ```
   Run `purge` only if the vault is listed. **Empty looks like this:** the last command prints nothing.
7. **Keep the budget:** `az consumption budget list -o table` still lists `monthly-2000`.
8. **The cost so far:** in the portal, open **Cost Management**, **Cost analysis**, for your subscription and this month. Group by **Service name** and type the table as text into `evidence.md`, with the total in rupees. Cost data can be a day late, and up to 72 hours late on pay-as-you-go: paste what it shows and say so.

The Databricks account and its Unity Catalog objects live in Databricks' own account, not in your subscription. Step 5 proves nothing of yours is left in Azure.

**Afterwards, choose one** ([`azure/README.md`](azure/README.md), "How to stop paying"):

- Keep the subscription **empty**, with the budget on. Check Cost analysis once a week until week 30.
- Or **cancel** it: **Subscriptions**, your subscription, **Cancel subscription**. Billing stops at once. You can delete it 3 days later.

## Microsoft Fabric (P10 task 25, and P14)

Fabric costs you nothing, so there is nothing to tear down in week 20.

- Your SQL is in `cyclecity/fabric/queries.sql`, in Git.
- On the shared centre trial (route B), leave the workspace as it is; the centre cleans up.
- On your own trial (route A), the trial ends about week 28. Lakehouse items stay in OneLake for 7 days after that.

**Optional, after week 28: delete your own directory.** Only if you used route A and want nothing left. Microsoft allows it only when:

- the directory has no subscriptions: cancel your Azure subscription, wait until it can be deleted (3 days), and delete it;
- no users remain except one Global Administrator: delete the `fabric` user;
- there are no applications and all invoices are paid.

Then sign in to `https://entra.microsoft.com`, select **Microsoft Entra ID**, open **Overview**, **Manage tenants**, tick your directory, and select **Delete**. If a check fails, the page links to the fix. An empty directory costs nothing, so you may also leave it.

## AWS (P11 task 27)

Keep the budget. Work in the newest copy of `cyclecity/`, and run Terraform only in `cyclecity/aws/infra/`. `cyclecity/infra/` is your P10 Azure code, already destroyed in P10: never run Terraform there again.

1. **Record the demo first.**
2. **Destroy on AWS.** From `cyclecity/`:
   ```bash
   aws login --profile cyclecity-login
   export AWS_PROFILE=cyclecity
   cd aws/infra
   terraform workspace select default
   terraform destroy
   ```
   The last line is `Destroy complete! Resources: N destroyed.` If it stops with `BucketNotEmpty`, set `force_destroy = true` on both buckets, run `terraform apply`, then `terraform destroy` again.
3. **Delete what Terraform did not create.** Glue writes its own log groups:
   ```bash
   aws logs describe-log-groups --query "logGroups[].logGroupName" --output table
   aws logs delete-log-group --log-group-name /aws-glue/jobs/output
   aws logs delete-log-group --log-group-name /aws-glue/jobs/error
   aws logs delete-log-group --log-group-name /aws-glue/crawlers
   ```
   Also delete `/aws/lambda/cyclecity-<your-id>-ingest` if it is still listed. A Glue database left behind goes with its tables (`raw_status`, `raw_trips`, `trips_parquet` and `trips`): `aws glue delete-database --name cyclecity_<your_id>`. A secret still listed, such as `cyclecity-<your-id>-alert-webhook`: `aws secretsmanager delete-secret --secret-id <name> --force-delete-without-recovery`.
4. **Prove it is empty.** Paste each command and its output:
   ```bash
   aws s3 ls
   aws lambda list-functions --query "Functions[].FunctionName" --output table
   aws glue get-databases --query "DatabaseList[].Name" --output table
   aws stepfunctions list-state-machines --output table
   aws secretsmanager list-secrets --output table
   aws events list-rules --output table
   aws logs describe-log-groups --query "logGroups[].logGroupName" --output table
   aws iam list-roles --query "Roles[?contains(RoleName, 'cyclecity')].RoleName" --output table
   aws athena list-work-groups --query "WorkGroups[].Name" --output table
   ```
   **Empty looks like this:**
   - `aws s3 ls` prints nothing.
   - The Lambda, Step Functions, rules, roles and log-group listings print nothing, or a table with no CycleCity name in it.
   - Glue lists no `cyclecity_<your_id>`. A database named `default` may remain; it is empty and free.
   - Secrets Manager lists no `cyclecity-<your-id>-alert-webhook`.
   - Athena lists only `primary`.
5. **The cost so far:**
   ```bash
   aws freetier get-account-plan-state --output table
   ```
   It shows `accountPlanType` `FREE`, `accountPlanStatus` `ACTIVE` and the credit left in `USD`. Add the `aws ce get-cost-and-usage` call from P11 task 26 for the module's dates. Each Cost Explorer call costs USD 0.01 of credit: run it once.
6. **The emulator.** Task 24 stopped it, so start the `storage` profile again first. Then, still in `cyclecity/aws/infra/`:
   ```bash
   (cd ~/de-kit/datalab && docker compose --profile storage up -d)
   export AWS_PROFILE=emulator
   terraform workspace select emulator
   terraform destroy
   aws s3 ls
   cd ~/de-kit/datalab && docker compose --profile storage down
   ```
7. **Sign out, and remove keys if you made any:** `aws logout --profile cyclecity-login`. If you created access keys (the fallback in [`aws/README.md`](aws/README.md)), delete them in **IAM**, **Users**, `<your-id>-admin`, **Security credentials**, and remove the `[cyclecity]` lines from `~/.aws/credentials`.

**When to close the account.** You may need it in the capstone (weeks 28 to 30). The Free plan closes the account by itself six months after sign-up, and you are never charged on the Free plan. To close it earlier, sign in as root, choose your account name, **Account**, and **Close account**.

## BigQuery (P12 task 12)

1. **Record the demo first.**
2. **Delete the scheduled query before the dataset.** Otherwise it keeps running, and fails, every day:
   ```bash
   bq ls --transfer_config --transfer_location=us
   bq rm -f --transfer_config <resource name>
   ```
   The resource name has the form `projects/<number>/locations/us/transferConfigs/<id>`.
3. **Delete the datasets.** This also deletes their tables and the materialised view:
   ```bash
   bq rm -r -f -d gitpulse
   bq rm -r -f -d scratch
   ```
4. **Prove it is empty:**
   ```bash
   bq ls
   bq ls --transfer_config --transfer_location=us
   ```
   **Empty looks like this:** both commands print nothing.
5. **The bytes you used this week:**
   ```sql
   SELECT DATE(creation_time) AS day, SUM(total_bytes_billed) AS bytes_billed
   FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_USER
   WHERE job_type = 'QUERY'
     AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
   GROUP BY day
   ORDER BY day;
   ```
   All of it falls inside the free 1 TiB a month.
6. **The trial credit used:** in the console, **Billing**, then **Credits** (or **Reports**). It shows the USD 300 Welcome credit and what is left.
7. **Leave the Free Trial to expire.** It ends after 90 days with no automatic charge. Do not upgrade it. Optional: unlink billing with `gcloud billing projects unlink gitpulse-<your-id>`, or delete the project with `gcloud projects delete gitpulse-<your-id>` (it can be restored for 30 days). Keep the project if you plan to use BigQuery in the capstone.

## At the end of the course (week 30)

| Platform | Check | Then |
|---|---|---|
| Databricks Free Edition | No job on an active schedule | Nothing: it never bills |
| Snowflake | Trial suspended since week 21 | Nothing |
| Azure | `az resource list -o table` prints nothing; Cost analysis shows no new cost | Cancel the subscription, or keep it empty with the budget on |
| Fabric | Trial ended in week 28 | Optional: delete your own directory |
| AWS | The P11 listings are still empty; no capstone resource left | Close the account, or let the Free plan close it |
| BigQuery | `bq ls --transfer_config --transfer_location=us` prints nothing | Leave the trial to expire |

## Sources, checked 13 November 2026

- GET_DDL (Snowflake docs): https://docs.snowflake.com/en/sql-reference/functions/get_ddl
- WAREHOUSE_METERING_HISTORY view (Snowflake docs): https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history
- Trial accounts (Snowflake docs): https://docs.snowflake.com/en/user-guide/admin-trial-account
- Pricing guide, AWS Mumbai prices (Snowflake): https://www.snowflake.com/pricing/pricing-guide/
- Command reference for terraform destroy (HashiCorp Developer): https://developer.hashicorp.com/terraform/cli/commands/destroy
- Start using Cost analysis (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis
- Understand Cost Management data, data delays (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data
- Key Vault soft-delete overview (Microsoft Learn): https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview
- Cancel and delete your Azure subscription (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/cancel-azure-subscription
- Delete a Microsoft Entra tenant (Microsoft Learn): https://learn.microsoft.com/en-us/entra/identity/users/directory-delete-howto
- Fabric trial capacity, end of trial (Microsoft Learn): https://learn.microsoft.com/en-us/fabric/fundamentals/fabric-trial
- Understanding unexpected charges (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/checklistforunwantedcharges.html
- Choosing a plan, when the Free plan ends (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- get-account-plan-state (AWS CLI reference): https://docs.aws.amazon.com/cli/latest/reference/freetier/get-account-plan-state.html
- AWS Cost Explorer pricing (AWS): https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/
- Close an AWS account (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-closing.html
- Manage transfers, delete a transfer configuration (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/working-with-transfers
- bq command-line tool reference (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference
- JOBS_BY_USER view (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-user
- Free Trial, end of trial and grace period (Google Cloud docs): https://docs.cloud.google.com/free/docs/free-cloud-features
- Shutting down (deleting) projects (Google Cloud docs): https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects
- Free Edition limitations, inactive accounts (Databricks docs): https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
