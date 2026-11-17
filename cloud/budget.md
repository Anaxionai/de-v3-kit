# Budget alarms and spending limits

Set the alarm **before you create anything** on a platform. The first cloud task of each project asks you to paste the evidence command's output.

## The rules

- **A budget alarm only warns.** On Azure, AWS and Google Cloud, a budget sends emails. It does not stop, pause or delete anything. The only way to stop paying is to delete what you made ([`teardown.md`](teardown.md)).
- **Alerts come late.** Azure checks budgets every 24 hours. AWS updates budget data up to three times a day. Google and Snowflake also lag. A mistake can cost money before the email arrives.
- **Count usage before credits.** On free credit, a budget that subtracts credits stays at zero while the credit drains, so it never warns you. The steps below exclude credits wherever the platform counts them.
- **Confirm the email.** AWS and Snowflake send nothing until you verify the address that receives alerts.
- **Snowflake is different:** its resource monitor really does suspend the warehouses at 100%.

## At a glance

| Platform (project) | Alarm | Amount | Evidence you paste |
|---|---|---|---|
| Databricks Free Edition (P7) | None: no bill. The daily quota and a paused schedule stand in for it | — | the paused schedule (P7 task 26) |
| Snowflake (P9) | Account-level resource monitor `GITPULSE_MONITOR` | 20 credits a month: NOTIFY at 50% and 80%, SUSPEND_IMMEDIATE at 100% | `snow sql --role ACCOUNTADMIN -q "SHOW RESOURCE MONITORS"` |
| Azure (P10) | Monthly cost budget on your subscription | ₹2,000: emails at 50% and 100% of actual cost | `az consumption budget list -o table` |
| AWS (P11) | Monthly cost budget, credits excluded | USD 5 (about ₹475): emails at 80% actual and 100% forecasted | `aws budgets describe-budgets --account-id <id> --output table` |
| BigQuery sandbox (P12) | Query-size limit and a scan ledger | 2 GB per query; 10 GB for task 8's five queries | the failing limit test and `cat ~/.bigqueryrc` |
| Google Cloud Free Trial (P12 task 11) | Alerts-only budget on the billing account, credits excluded | ₹100: emails at 50%, 90% and 100% | `gcloud billing budgets list --billing-account=<id>` |

Rupee figures use about **₹95 to the US dollar**: the RBI reference rate was ₹95.25 on 6 November 2026, and Microsoft's rupee price list uses about ₹95.23. Write the rate and the date whenever you convert.

## Snowflake: the resource monitor (P9 task 8)

A resource monitor counts the credits that warehouses use, including the cloud services those warehouses need. At its limit it can suspend them. It cannot track serverless features (Snowpipe, serverless tasks) or AI services. GitPulse uses only warehouses, and its stream task runs on `GITPULSE_WH`, so the monitor covers it.

- **Only `ACCOUNTADMIN` can create a resource monitor.**
- An **account-level** monitor covers every warehouse in the account, including `COMPUTE_WH`. An account can have only one. A **warehouse-level** monitor covers only the warehouses assigned to it. GitPulse uses one account-level monitor.
- `SUSPEND` lets running statements finish, then suspends. `SUSPEND_IMMEDIATE` cancels running statements and suspends at once.
- The quota resets at the start of each calendar month, at 00:00 UTC.

**The monitor the course uses** (`gitpulse/snowflake/01_monitor.sql`, run as `ACCOUNTADMIN`):

```sql
CREATE RESOURCE MONITOR GITPULSE_MONITOR WITH
  CREDIT_QUOTA = 20
  TRIGGERS ON 50 PERCENT DO NOTIFY
           ON 80 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND_IMMEDIATE;
ALTER ACCOUNT SET RESOURCE_MONITOR = GITPULSE_MONITOR;
```

**Turn on the emails.** Notifications are off by default. In Snowsight, open your profile (your name at the bottom left), verify your email address, and switch on resource monitor notifications. As an account administrator you receive alerts for the account-level monitor.

**Check it:**

```bash
snow sql --role ACCOUNTADMIN -q "SHOW RESOURCE MONITORS"
```

The row for `GITPULSE_MONITOR` shows `credit_quota` 20, `used_credits`, `remaining_credits` and `level` `ACCOUNT`.

**Read what you used.** `SHOW RESOURCE MONITORS` gives the credits used this month. For credits per warehouse:

```sql
SELECT warehouse_name, SUM(credits_used) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
GROUP BY warehouse_name
ORDER BY credits DESC;
```

This view can be up to 3 hours behind.

**What a credit is worth:**

| Item | Price | In rupees (₹95 to the dollar) |
|---|---|---|
| Trial free usage | **USD 400, for 30 days** | about ₹38,000 |
| One credit, **Standard edition, AWS Mumbai**, on demand | **USD 2.20** | **₹209** |
| One credit, Enterprise edition, AWS Mumbai (for comparison) | USD 3.30 | ₹313.50 |
| Storage, AWS Mumbai | USD 25 per TB a month | ₹2,375 per TB a month |
| The monitor's 20 credits on Standard | USD 44 | ₹4,180 |

Snowflake publishes its prices in US dollars only. USD 400 buys about 181 credits on Standard in Mumbai.

**How warehouses are billed:** an X-Small warehouse uses **1 credit an hour**. Billing is per second, with a **60-second minimum** each time the warehouse starts or resumes. With `AUTO_SUSPEND = 60`, a 5-second query on a suspended warehouse bills 60 seconds: 1/60 of a credit, about ₹3.48.

**Where the trial balance shows:** with the role `ACCOUNTADMIN`, Snowsight shows the free balance left on a tile in the left navigation bar. P9 task 27 records it.

**When the trial ends** (30 days or USD 400, whichever comes first), Snowflake suspends the account and unused free usage expires. Without payment details there is no charge. See [`snowflake/README.md`](snowflake/README.md).

## Azure: the monthly budget (P10 task 8)

Create it in the portal on the day you open the account. It is made outside Terraform on purpose, so `terraform destroy` never removes it.

1. In the portal, search for **Subscriptions** and select yours.
2. In the menu, select **Budgets** (under **Cost Management**), then **Add**.
3. Check that the scope is your subscription. Name: `monthly-2000`. Reset period: **Monthly**. Expiration date: at least six months away.
4. Amount: **2000**. The amount is in your billing currency; if the portal shows US dollars, enter **21**.
5. Select **Next**. Under **Alert conditions**, add type **Actual** at **50** % of budget and type **Actual** at **100** % of budget.
6. Under **Alert recipients (email)**, type your email. Select **Create**.
7. Add `azure-noreply@microsoft.com` to your email's safe senders, so alerts do not land in junk mail.

**Check it:**

```bash
az consumption budget list -o table
```

The table shows `monthly-2000`, its amount, `Monthly` and the cost so far. The `consumption` commands are in preview.

What to know:

- Microsoft: "Resources aren't affected, and your consumption isn't stopped."
- Cost data usually arrives within 8 to 24 hours; for pay-as-you-go subscriptions it can take up to 72 hours. Budgets are checked every 24 hours.
- Cost Management shows costs **without** credits, so the budget counts what you use even while the free credit pays.
- On a new subscription, Microsoft says Cost Management features can take up to 48 hours. If **Budgets** is not offered yet, try again later that day. If the list is empty but the portal shows the budget, wait 10 minutes and run it again.
- The budget stays after the teardown, and after the upgrade to pay-as-you-go.

The CLI can create a budget (`az consumption budget create`), but it cannot add the email alerts in the same simple command. Use the portal.

## AWS: the monthly cost budget (P11 task 8)

Create it as your IAM admin user, after step 5 of [`aws/README.md`](aws/README.md), before anything else on AWS. Setting up a cost budget is one of the Free plan activities: it earns you USD 20 of credit.

**Two files** in a folder outside your course repository, for example `~/aws-budget/`:

`budget.json`: a monthly cost budget of USD 5 that counts usage before credits.

```json
{
  "BudgetName": "cyclecity-5usd",
  "BudgetLimit": {"Amount": "5", "Unit": "USD"},
  "BudgetType": "COST",
  "TimeUnit": "MONTHLY",
  "CostTypes": {"IncludeCredit": false}
}
```

`notifications.json`: an email at 80% of actual cost and at 100% of forecasted cost. Put your own email in both places.

```json
[
  {
    "Notification": {"NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": 80, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "you@example.com"}]
  },
  {
    "Notification": {"NotificationType": "FORECASTED", "ComparisonOperator": "GREATER_THAN", "Threshold": 100, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "you@example.com"}]
  }
]
```

**Create it and check it:**

```bash
export AWS_PROFILE=cyclecity
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "$ACCOUNT_ID"
cd ~/aws-budget
aws budgets create-budget --account-id "$ACCOUNT_ID" --budget file://budget.json --notifications-with-subscribers file://notifications.json
aws budgets describe-budgets --account-id "$ACCOUNT_ID" --output table
```

- `create-budget` prints nothing when it works.
- `describe-budgets` shows `cyclecity-5usd`, `Amount` `5.0`, `Unit` `USD`, `TimeUnit` `MONTHLY` and `IncludeCredit` `False`. Paste this output.
- Your account ID is the `Account` field of `aws sts get-caller-identity`.
- AWS Budgets is a global service; the command works whatever your Region is.

**Verify your email.** AWS sends a message to the address in `notifications.json`. Email recipients must verify their address before they receive budget notifications.

**Console route instead:** **Billing and Cost Management**, **Budgets**, **Create budget**, **Customize (advanced)**, **Cost budget**. Name it, period **Monthly**, budgeted amount `5.00`. Under **Budget scope**, exclude credits (the option sits in the filters or the advanced options, depending on the console version). Add the two alert thresholds above with your email, then **Create budget**.

What to know:

- Monitoring and email alerts are free. AWS charges only for action-enabled budgets beyond the first two, and the course uses none.
- Budget data is updated up to three times a day, usually 8 to 12 hours apart.
- On the Free plan you are never charged; the budget guards your **credit**. USD 5 is far above P11's expected USD 1 to 2. An alert means something is still running: check it the same day.
- Your invoices from AWS India are in rupees; the budget and the credits are counted in US dollars.

## Google Cloud: the BigQuery limit and the trial budget (P12)

### In the sandbox (P12 task 7)

The sandbox has no billing account, so it cannot have a Cloud Billing budget. Nothing can be charged. The alarm protects your free monthly 1 TiB and teaches the habit:

- **A 2 GB limit on every query** in `~/.bigqueryrc`: `--maximum_bytes_billed=2000000000`. A query over the limit fails and costs nothing. [`gcp/README.md`](gcp/README.md) shows the file and the test.
- **A 10 GB ledger** in `gitpulse/bigquery/docs/budget.md`: the dry-run estimate and the real bytes of every query, with the five queries of task 8 totalling under 10 GB.

Evidence: the failing limit test and `cat ~/.bigqueryrc`.

### With the Free Trial (P12 task 11)

When task 11 links the Free Trial billing account to your project, add an alerts-only budget of ₹100.

You need the role **Billing Account Administrator** or **Billing Account Costs Manager** on the billing account. You have the first: you created the trial.

**Console:**

1. Open **Billing**, then **Budgets & alerts**, then **Create budget**.
2. Name: `gitpulse-100`. Scope: **Projects**, select `gitpulse-<your-id>`.
3. Under **Savings** (credits), **clear every option**. Google counts spend after credits by default; with the trial's USD 300 credit, the budget would stay at zero.
4. Amount: **Specified amount**, **100**. The amount is in your billing account's currency.
5. Thresholds: **50**, **90** and **100** % of **Actual**. Email alerts go to billing administrators, which includes you.
6. Select **Finish**.

**Command line, instead of the console:**

```bash
gcloud services enable billingbudgets.googleapis.com
gcloud billing budgets create --billing-account=<ACCOUNT_ID> \
  --display-name="gitpulse-100" \
  --budget-amount=100 \
  --filter-projects=projects/gitpulse-<your-id> \
  --credit-types-treatment=exclude-all-credits \
  --threshold-rule=percent=0.5 --threshold-rule=percent=0.9 --threshold-rule=percent=1.0
```

Without a currency code, `--budget-amount` uses your billing account's currency. If your billing account is in US dollars, use `--budget-amount=1.05USD` (about ₹100).

**Check it:**

```bash
gcloud billing budgets list --billing-account=<ACCOUNT_ID>
```

It shows `displayName: gitpulse-100`, the amount and the threshold rules.

Google: "Setting an alerts-only budget doesn't automatically cap Google Cloud or Google Maps Platform usage or spending." During the Free Trial you are not billed; the budget tells you when usage starts.

## Databricks Free Edition (P7)

Free Edition sends no bill and asks for no card, so there is no budget alarm. Instead:

- The **daily quota** stops compute for the rest of the day when you use too much. Your data is kept.
- P7 task 21 records the quota in place of a budget, and task 26 **pauses** the schedule after one successful run.

See [`databricks/README.md`](databricks/README.md).

## Sources, checked 13 November 2026

- Working with resource monitors (Snowflake docs): https://docs.snowflake.com/en/user-guide/resource-monitors
- Pricing guide, AWS Mumbai prices (Snowflake): https://www.snowflake.com/pricing/pricing-guide/
- Start your free trial, USD 400 (Snowflake): https://info.snowflake.net/start-your-free-trial.html
- Trial accounts (Snowflake docs): https://docs.snowflake.com/en/user-guide/admin-trial-account
- Warehouse considerations, per-second billing (Snowflake docs): https://docs.snowflake.com/en/user-guide/warehouses-considerations
- WAREHOUSE_METERING_HISTORY view (Snowflake docs): https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history
- Create and manage budgets (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets
- Understand Cost Management data (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data
- az consumption budget (Microsoft Learn): https://learn.microsoft.com/en-us/cli/azure/consumption/budget
- Managing your costs with AWS Budgets (AWS Cost Management): https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- Creating a cost budget (AWS Cost Management): https://docs.aws.amazon.com/cost-management/latest/userguide/create-cost-budget.html
- Best practices for AWS Budgets (AWS Cost Management): https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html
- AWS Budgets pricing (AWS): https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/
- Earning additional credits (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans-activities.html
- Create, edit or delete budgets and budget alerts (Google Cloud docs, updated 10 November 2026): https://docs.cloud.google.com/billing/docs/how-to/budgets
- gcloud billing budgets create (Google Cloud SDK reference): https://docs.cloud.google.com/sdk/gcloud/reference/billing/budgets/create
- Try BigQuery using the sandbox (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/sandbox
- bq command-line tool reference, `.bigqueryrc` (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference
- Free Edition limitations (Databricks docs): https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- Microsoft's INR price list: Azure retail prices API (Microsoft): https://prices.azure.com/api/retail/prices
