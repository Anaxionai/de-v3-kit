# The cloud calendar

From week 14 you work on real cloud platforms, each on its own free trial or free plan. This page says which account you open in which week, how long each one lasts, and when you close it. It also gives the rules that keep your bill at zero.

If you follow the steps, **you pay nothing**, with one stated exception: the Azure Databricks week (week 20) costs about **₹950**. Your Azure free credit normally pays it, so your card pays ₹0. See [`azure/README.md`](azure/README.md).

## The accounts, week by week

Weeks count from the first day of the course. "Day 1" is the first day of that week.

| Week | Project | Account | Card? | How long it lasts | What is free | Close or stop it |
|---|---|---|---|---|---|---|
| 14 | P7 TaxiScale | **Databricks Free Edition**, your own ([guide](databricks/README.md)) | No | No end date | Everything, within a daily quota | Week 15: schedule paused (P7 task 26) |
| 17, day 1 | P9 GitPulse | **Snowflake trial**, your own ([guide](snowflake/README.md)) | No | **30 days**, or until USD 400 of usage is spent: ends in **week 21** | USD 400 of usage | Week 18: P9 task 27 |
| 19, day 1 | P10 CycleCity | **Azure free account**, your own ([guide](azure/README.md)) | Yes | Credit: **30 days**, ends in **week 23**. Free services: 12 months | USD 200 credit; monthly free amounts of 20+ services | Week 20: P10 task 26 |
| 20, day 1 | P10 CycleCity | **The same Azure account, upgraded to pay-as-you-go** for Azure Databricks | Yes (same card) | Until you cancel it | The leftover credit, until day 30 of the account; the workspace's DBUs for 14 days | Week 20: P10 task 26; then cancel or keep empty |
| 20 | P10 (and P14 in week 25) | **Microsoft Fabric**: a user in your own Azure directory, or your centre's account ([guide](fabric/README.md)) | No | **60 days**: ends in **week 28** | The trial capacity and a Power BI trial | Nothing to close |
| 21, day 1 | P11 CycleCity part 2 | **AWS, Free plan**, your own ([guide](aws/README.md)) | Yes, and an identity document | **6 months**, or until the credit is used: about week 47 | USD 100 credit, plus up to USD 100 earned | Week 22: P11 task 27 |
| 23 | P12 GitPulse part 2 | **BigQuery sandbox**, your own Google account ([guide](gcp/README.md)) | No | No end date; tables expire 60 days after you make them | 1 TiB of queries a month; 10 GiB of storage in total | Week 23: P12 task 12 |
| 23 | P12 task 11 only | **Google Cloud Free Trial**, linked to the same project | Yes | **90 days**: about week 36 | USD 300 credit; nothing is billed during the trial | Week 23: P12 task 12; let it expire |

## Does each trial last until its project ends?

Yes. Every trial or plan outlasts the project that uses it:

| Account | Project ends | Trial ends | Spare time |
|---|---|---|---|
| Databricks Free Edition | week 15 | no end | — |
| Snowflake trial | week 18 | week 21 | about 2.5 weeks |
| Azure credit (30 days) | week 20 | week 23 | about 2.5 weeks |
| Azure Databricks trial tier (14 days of free DBUs) | week 20 | week 22 | about 1.5 weeks |
| Fabric trial (60 days) | week 20 (P10); week 25 (P14 Stretch) | week 28 | about 2.5 weeks after P14 |
| AWS Free plan (6 months) | week 22 | about week 47 | after the course ends |
| BigQuery sandbox | week 23 | no end | — |
| Google Cloud Free Trial (90 days) | week 23 | about week 36 | after the course ends |

Points to know:

- **Open each account in its week, not earlier.** Trial clocks start at sign-up. A Snowflake trial opened a week early ends a week early. The one exception is AWS: you may open it in week 20 (see below).
- **The Snowflake trial ends in week 21**, before P12 (week 23). P12 task 12 compares Snowflake using the numbers you saved in P9; it never runs Snowflake again.
- **The Azure credit ends in week 23.** After that, anything left in your Azure subscription is paid by your card. Tear down in week 20.
- **The Fabric trial ends in week 28**, at the start of the capstone. Do not plan capstone work on Fabric.
- **AWS checks your identity after sign-up** (Indian CERT-In rules) and gives no time for it. Opening the account during week 20 is fine: six months is long enough.
- **Databricks may delete Free Edition accounts** that stay inactive for a long time. Weeks 16 to 27 are quiet. Keep every notebook as a `.py` file in Git.

## In the capstone (weeks 28 to 30)

Still open, and still free if you follow the rules:

- **Databricks Free Edition**, with its daily quota.
- **AWS Free plan**, with what is left of your credit.
- **BigQuery**: the sandbox, or your Free Trial until about week 36.

Closed by then: the Snowflake trial (week 21), the Azure credit (week 23; your subscription is pay-as-you-go), and the Fabric trial (week 28). Your capstone plan's cost section says which of the open ones you use.

## What you need, and when

| By | You need | For |
|---|---|---|
| Week 14 | A personal email address | Databricks Free Edition, Snowflake |
| Week 17 | Your own **credit card, or a debit card that is not prepaid**, that works for online payments | Azure (week 19), AWS (week 21), Google Cloud Free Trial (week 23) |
| Week 19 | A mobile phone for SMS and an **authenticator app** on it | Azure, Fabric, AWS sign-ins |
| Week 20 | A **PAN card, voter ID card or driving licence**, with your name exactly as on it | AWS identity check |

No card or no document? Tell your mentor by week 17. The course has no card-free route for Azure and AWS.

## The rules that keep the bill at zero

1. **Alarm first.** Before you create anything on a platform, set its budget alarm or resource monitor: [`budget.md`](budget.md). The first cloud task of each project asks for the proof.
2. **Smallest size, and make it stop by itself.** X-Small Snowflake warehouses with `AUTO_SUSPEND = 60`. A single-node Azure Databricks cluster with 20-minute automatic termination. Databricks schedules paused after one run. A 2 GB limit on every BigQuery query.
3. **Delete it the same week.** The last build task of each cloud project is the teardown, with empty listings and the cost so far: [`teardown.md`](teardown.md).
4. **Upgrade nothing**, except the Azure upgrade in week 20 that [`azure/README.md`](azure/README.md) describes. Never upgrade a Snowflake trial, the AWS Free plan or the Google Cloud Free Trial. Never buy from a marketplace.
5. **AWS: never use AWS Organizations or IAM Identity Center**, and never accept an invitation to an organization. Joining one upgrades your Free plan to the Paid plan.
6. **No secret in a committed file.** No password, key, token or connection string with a password. Keys live in `~/snowflake-keys/` and `~/.aws/`, CI secrets in GitHub Actions secrets, and settings in a `.env` file that Git ignores.
7. **An alarm email means stop.** List what is running, delete it, and tell your mentor the same day.
8. **Check every Friday until week 30.** Open each platform's cost page that is still open and read the number.

Rupee amounts in these guides use about **₹95 to the US dollar** (RBI reference rate ₹95.25 on 6 November 2026; Microsoft's rupee prices use about ₹95.23). Prices change: each guide gives the date it was checked.

## The guides

| Guide | What it covers |
|---|---|
| [`budget.md`](budget.md) | Budget alarms on Azure, AWS and Google Cloud, and the Snowflake resource monitor |
| [`teardown.md`](teardown.md) | The teardown checklist per platform, the listings that prove nothing is left, and how to read the cost |
| [`databricks/README.md`](databricks/README.md) | Databricks Free Edition: sign-up, limits, uploads, exporting notebooks |
| [`snowflake/README.md`](snowflake/README.md) | The Snowflake trial, the Snowflake CLI, key-pair sign-in |
| [`azure/README.md`](azure/README.md) | The Azure free account, CLI, Terraform, the pay-as-you-go week and its cost |
| [`fabric/README.md`](fabric/README.md) | Signing in to Microsoft Fabric and the trial |
| [`aws/README.md`](aws/README.md) | The AWS account on the Free plan, the admin user, the CLI profile |
| [`gcp/README.md`](gcp/README.md) | BigQuery in the sandbox, the `bq` tool, the query-size limit, the Free Trial |

## Sources, checked 13 November 2026

Each guide lists the provider pages behind its numbers. The trial terms on this page come from:

- Free Edition limitations (Databricks docs): https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- Trial accounts (Snowflake docs): https://docs.snowflake.com/en/user-guide/admin-trial-account
- Start your free trial, USD 400 (Snowflake): https://info.snowflake.net/start-your-free-trial.html
- Azure free account, India (Microsoft Azure): https://azure.microsoft.com/en-in/pricing/purchase-options/azure-account
- Upgrade your Azure account (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/upgrade-azure-subscription
- Sign up for Azure Databricks for free (Microsoft Learn): https://learn.microsoft.com/en-us/azure/databricks/getting-started/free-trial
- Fabric trial capacity (Microsoft Learn): https://learn.microsoft.com/en-us/fabric/fundamentals/fabric-trial
- Choosing a plan (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- Manage accounts in India (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/managing-accounts-india.html
- Try BigQuery using the sandbox (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/sandbox
- Free cloud features and Free Trial (Google Cloud docs): https://docs.cloud.google.com/free/docs/free-cloud-features
- RBI reference rate archive (Metropolitan Stock Exchange of India): https://www.msei.in/markets/Currency/Historical-Data/RBIReferenceRateArchives.aspx
