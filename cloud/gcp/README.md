# Google Cloud: BigQuery at no cost

In P12 (week 23), GitPulse part 2, you answer GitPulse's questions again in BigQuery. This guide covers the route the module uses, the `gcloud` and `bq` tools on Windows, and the limit on every query.

## The route P12 uses

| Tasks | Route | Card? | Cost to you |
|---|---|---|---|
| Cards 1 to 5, tasks 6 to 10 and 12 | **BigQuery sandbox** | No | ₹0 |
| Task 11 only (the scheduled query) | **Google Cloud Free Trial**, linked to the same project | Yes | ₹0: "You will not be billed for any Google Cloud usage during your Free Trial" |

Why the switch in task 11: a scheduled query runs on the BigQuery Data Transfer Service, which the sandbox does not support, and transfers need billing on the project.

On both routes, BigQuery's **free monthly allowance** applies: **1 TiB of query processing and 10 GiB of storage a month**. P12's queries are designed to stay far inside it.

## 1. Open the sandbox (card 1)

1. Open `https://console.cloud.google.com/bigquery` and sign in with your Google account.
2. Choose your country, accept the terms, and click **Create project**.
3. Name the project `gitpulse-<your-id>`. Leave the organisation as **No organisation**. No card is asked for.
4. Note the **project ID** and the **project number**. A sandbox notice appears on the BigQuery page.

**Project ID rules:** 6 to 30 characters; lower-case letters, digits and hyphens; it starts with a letter and cannot end with a hyphen. It must be unique across all of Google Cloud, and it can never be changed. If your GitHub id makes it too long, shorten the id. If the ID is taken, add two digits.

If the console asks for a card, you opened the Free Trial page by mistake. Go back to `https://console.cloud.google.com/bigquery`.

### What the sandbox allows

| Sandbox rule | What it means for P12 |
|---|---|
| No card, no billing account | Nothing can be charged |
| 1 TiB of query processing a month | The same as the free allowance |
| **10 GiB of storage, a lifetime limit.** "This quota is not refunded upon data deletion" | Build each table once. Deleting a table does not give the space back |
| Tables, views and partitions **expire after 60 days** | A date partition older than 60 days expires at once, so task 9 partitions by year with integer ranges |
| No streaming, no DML (`INSERT`, `UPDATE`, `DELETE`, `MERGE`), no Data Transfer Service | Task 11 needs the Free Trial |

Datasets built from public data must be in the **`US`** multi-region, where the public datasets live.

## 2. Install the Google Cloud CLI

The Google Cloud CLI gives you `gcloud` and `bq`. In **PowerShell**, download and run Google's installer:

```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

In the installer, keep **Install Bundled Python** ticked. The CLI then brings its own Python and does not use yours. The course version is in the kit's `VERSIONS.md`.

Close VS Code and open it again. In Git Bash:

```bash
gcloud --version
bq version
```

The first prints `Google Cloud SDK` and its version; the second prints the `bq` version.

If Git Bash says `command not found`, or prints a Python error, call the Windows versions of the commands. Add these lines to `~/.bashrc`, then open a new terminal:

```bash
alias gcloud='gcloud.cmd'
alias bq='bq.cmd'
```

## 3. Sign in and choose the project

```bash
gcloud auth login
gcloud config set project gitpulse-<your-id>
gcloud config get-value project
```

The first command opens your browser: sign in with the same Google account and allow access. The last command prints `gitpulse-<your-id>`. `bq` uses the same sign-in and project.

## 4. The limit on every query (P12 task 7)

`--maximum_bytes_billed` makes BigQuery refuse any query that would bill more bytes than the limit. A refused query is not charged. Put the limit in `~/.bigqueryrc`, the `bq` settings file, so every `bq query` has it.

Create the file with exactly three lines:

```bash
printf '[query]\n--use_legacy_sql=false\n--maximum_bytes_billed=2000000000\n' > ~/.bigqueryrc
cat ~/.bigqueryrc
```

The `cat` shows:

```ini
[query]
--use_legacy_sql=false
--maximum_bytes_billed=2000000000
```

- 2,000,000,000 bytes is 2 GB per query.
- `bq` reads `$HOME/.bigqueryrc`, or the file named in the `BIGQUERYRC` environment variable.
- Write `--use_legacy_sql=false`. The short form `--nouse_legacy_sql` does not work inside `.bigqueryrc`.
- The file must not end in `.txt`. If you make it in Notepad, check the name with `ls -a ~ | grep bigqueryrc`.

Test it with a query that reads far more than 2 GB:

```bash
bq query 'SELECT body FROM `bigquery-public-data.stackoverflow.posts_questions`'
```

It must fail with an error that starts `Query exceeded limit for bytes billed: 2000000000.` and names the bytes required. That failure is your evidence that the limit works.

**The same limit in the console:** in the query editor, open **More** (or **Edit**), then **Query settings**, then **Advanced options**, and set **Maximum bytes billed** to `2000000000`. The console does not read `~/.bigqueryrc`, so set it there too if you run queries in the console.

**Estimate before you run:** a dry run prints the bytes a query would read and runs nothing:

```bash
bq query --dry_run < gitpulse/bigquery/sql/q01_events_per_type.sql
```

The 2 GB limit and the 10 GB ledger in `gitpulse/bigquery/docs/budget.md` are P12's budget alarm. See the GCP section of [`../budget.md`](../budget.md).

## 5. Cloud Shell, if `bq` will not run on your laptop

Cloud Shell is a terminal in the browser with `gcloud` and `bq` ready.

1. In the console, click the **Activate Cloud Shell** button (a `>_` icon) at the top right.
2. Create `~/.bigqueryrc` there with the same `printf` command. Cloud Shell has its own home folder.
3. Upload your `sql/` files with the **More** menu, then **Upload**, and copy the outputs back into `evidence.md`.

Cloud Shell has a default quota of **50 hours a week**.

## 6. The Free Trial for task 11

1. Open `https://console.cloud.google.com/freetrial`.
2. Enter a credit or debit card (Visa, Mastercard or American Express) or another payment method Google accepts. Depending on your country, Google may also ask you to verify a bank account.
3. Google places a temporary authorisation on the card. It is not a charge.
4. The trial creates a Free Trial billing account named **My Billing Account**, with **USD 300 of credit for 90 days**.

**Link it to your project:**

```bash
gcloud billing accounts list
gcloud billing projects link gitpulse-<your-id> --billing-account=<ACCOUNT_ID>
gcloud billing projects describe gitpulse-<your-id>
```

The first command shows your billing account's ID (the form `XXXXXX-XXXXXX-XXXXXX`). The last shows `billingEnabled: true`. Then set the ₹100 alerts-only budget: GCP section of [`../budget.md`](../budget.md).

What the trial means:

- **You are not billed during the trial.** The credit pays for usage, and the free allowance still applies first.
- The project leaves the sandbox. Your `gitpulse` dataset keeps its 60-day default expiry; P12 does not change it.
- The first `bq query --schedule` may print a sign-in link to authorise the Data Transfer Service. Open it, allow access, and paste the code back. The console route is **File**, then **Schedule**.
- For customers in India, Google warns that banks may decline automatic card charges over ₹15,000 because of RBI rules. P12 never comes near that.

**When the trial ends** (90 days, about week 36, or when USD 300 is used): Google closes the Free Trial billing account and stops its projects. There is **no automatic charge**. A 30-day grace period follows; if you do not upgrade, the trial's resources are deleted. Do not upgrade to a paid billing account.

## What a query costs after the free allowance

You will not pass the free 1 TiB a month in P12. For your cost comparison in task 12:

- On-demand queries cost **USD 6.25 per TiB** after the first free TiB each month (about ₹594 at ₹95 to the dollar). Google bills other currencies at the prices on its SKU list.
- A query refused by the 2 GB limit costs nothing. A query that bills the full 2 GB would cost about ₹1.08 after the free TiB.
- The 10 GB ledger for task 8's five queries is worth about ₹5.40 at that price.

## Sources, checked 13 November 2026

- Try BigQuery using the sandbox (Google Cloud docs, updated 10 November 2026): https://docs.cloud.google.com/bigquery/docs/sandbox
- Free cloud features and Free Trial (Google Cloud docs, updated 10 November 2026): https://docs.cloud.google.com/free/docs/free-cloud-features
- Payment methods, India notes (Google Cloud docs, updated 10 November 2026): https://docs.cloud.google.com/billing/docs/how-to/payment-methods
- BigQuery pricing (Google Cloud): https://cloud.google.com/bigquery/pricing
- bq command-line tool reference, `.bigqueryrc` (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference
- Estimate and control costs, maximum bytes billed (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/best-practices-costs
- Install the Google Cloud CLI (Google Cloud docs, updated 10 November 2026): https://docs.cloud.google.com/sdk/docs/install-sdk
- Cloud Shell quotas and limits (Google Cloud docs, updated 10 November 2026): https://docs.cloud.google.com/shell/docs/quotas-limits
- Scheduling queries (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/scheduling-queries
- Enable the Data Transfer Service (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/enable-transfer-service
- Creating and managing projects (Google Cloud docs): https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects
- gcloud billing projects link (Google Cloud SDK reference): https://docs.cloud.google.com/sdk/gcloud/reference/billing/projects/link
