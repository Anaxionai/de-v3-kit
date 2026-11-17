# Azure: free account, CLI, and the Databricks week

In P10 (weeks 19 and 20) you build CycleCity on your own Azure account. This guide opens the free account, installs the Azure CLI and Terraform, signs you in, and upgrades the account to pay-as-you-go for Azure Databricks in week 20. It also shows what that week costs and how to stop paying.

Run every command in Git Bash inside VS Code. Where PowerShell is different, the guide says so.

| When | What | Task |
|---|---|---|
| Week 19, day 1 | Open the free account, install the tools, sign in, set the budget alarm | P10 task 8 |
| Week 20, day 1 | Upgrade to pay-as-you-go, check the vCPU quota | P10 task 20 |
| Week 20, last day | Tear everything down and read the cost | P10 task 26 |

## Before you start

- **A credit card or a debit card that is not prepaid.** Microsoft may place a temporary authorisation of USD 1 on it and reverses it after the check.
- **A mobile phone**, for the identity check.
- **A personal email address.** The sign-up creates a Microsoft account with it if you have none.

No card by week 17? Tell your mentor.

## 1. Open the free account

1. Open `https://azure.microsoft.com/en-in/pricing/purchase-options/azure-account` and choose **Try Azure for free**.
2. Sign in with your Microsoft account, or create one with your personal email.
3. Verify your phone, add your card, and accept the agreement.
4. The Azure portal opens at `https://portal.azure.com`.

What you get, as Microsoft states it:

- **USD 200 of credit to use within 30 days** of sign-up. Microsoft gives it "in your billing currency".
- Free monthly amounts of 20 or more services **for 12 months**.
- A **spending limit** equal to the credit: when the credit is used up, Azure stops your resources instead of charging your card.
- "We'll never charge you unless you decide to move to pay-as-you-go pricing."

The sign-up also creates a **Microsoft Entra directory** (a tenant: the list of users for your account). The Fabric guide uses it: [`../fabric/README.md`](../fabric/README.md).

## 2. Install the Azure CLI

```bash
winget install --exact --id Microsoft.AzureCLI
```

It works in Git Bash and in PowerShell. Close VS Code and open it again, so the terminal finds `az`. Then:

```bash
az version
```

It prints `"azure-cli"` and the version. The course version is in the kit's `VERSIONS.md`.

The CLI installs an extension the first time you use a command that needs one (`az datafactory`, `az databricks`). Answer `Y` when it asks.

## 3. Install Terraform

HashiCorp publishes Terraform for Windows as a zip file with one program inside. Put it in `~/bin`, which Git Bash searches for programs. Use the version in the kit's `VERSIONS.md` (1.17.2 in November 2026):

```bash
TF_VERSION=1.17.2
mkdir -p ~/bin && cd ~/bin
curl -LO "https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_windows_amd64.zip"
uv run --no-project --python 3.12 python -m zipfile -e "terraform_${TF_VERSION}_windows_amd64.zip" .
rm "terraform_${TF_VERSION}_windows_amd64.zip"
grep -q 'HOME/bin' ~/.bashrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
cd ~
```

Close the terminal, open a new one, and check:

```bash
terraform -version
```

It prints `Terraform v1.17.2` and `on windows_amd64`. PowerShell does not read `~/.bashrc`: run Terraform from Git Bash.

## 4. Sign in

```bash
az login
```

On Windows, the CLI signs in through Windows' own sign-in window (Web Account Manager), not a browser tab. Choose your account. If you have more than one subscription, the CLI lists them: type the number of yours.

Check the result:

```bash
az account show -o table
```

It shows your subscription's name, `State` `Enabled` and `IsDefault` `True`. If another subscription is the default:

```bash
az account set --subscription "<subscription name or ID>"
```

If the sign-in window does not open, or shows an error such as `User cancelled the Accounts Control Operation`, switch the CLI to the browser and sign in again:

```bash
az config set core.enable_broker_on_windows=false
az login
```

`az login --use-device-code` may be refused: new Microsoft Entra directories block the device-code sign-in since 1 July 2026. Use the browser instead.

## 5. Set the budget alarm

Before you create anything, set the monthly budget of ₹2,000 in the Azure section of [`../budget.md`](../budget.md). It stays on until you close the account.

## 6. Register the resource providers

A new subscription must register each Azure service before it can create its resources. P10 task 8 registers the five that CycleCity uses:

```bash
for ns in Microsoft.Storage Microsoft.DataFactory Microsoft.KeyVault Microsoft.Databricks Microsoft.Insights; do az provider register -n $ns; done
az provider show -n Microsoft.Storage --query registrationState -o tsv
```

The last command prints `Registered` after a minute or two. Check the other four the same way.

## 7. Terraform working rules

- **State stays on your laptop.** `terraform.tfstate` records what Terraform created. It is never committed: `cyclecity/.gitignore` lists `.terraform/`, `*.tfstate` and `*.tfstate.*`.
- **Copy the product folder forward with `cp -r`**, so `infra/terraform.tfstate` comes along to the next task's folder.
- **Run Terraform only in the newest copy.** An older copy has an old state file. A `plan` there would try to recreate or destroy what the newer copy built.
- Optional: to download providers only once, add `export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"` to `~/.bashrc` and run `mkdir -p ~/.terraform.d/plugin-cache`.

## Git Bash and Windows notes

- Git Bash rewrites an argument that starts with `/` into a Windows path. Put `MSYS_NO_PATHCONV=1` before an `az` command whose argument starts with `/`, for example `--scope /subscriptions/...`.
- Pass JSON to `az` from a file: `--parameters @params.json`. Quoting JSON on the command line differs between Git Bash and PowerShell.
- The key vault secret in P10 task 11 is typed with `read -rs` so it never appears on screen or in your shell history.

## 8. The upgrade to pay-as-you-go (week 20, day 1)

Azure Databricks does not run on a free subscription. Microsoft's Databricks page says you need a subscription that is not a **Free Trial Subscription**: change it to pay-as-you-go, remove the spending limit, and request vCPU quota.

**Upgrade:**

1. In the portal, search for **Subscriptions** and select the subscription from your sign-up.
2. Select **Upgrade subscription** in the command bar. If you do not see it, select the upgrade banner at the top of the page.
3. Confirm your card and phone if asked, keep the subscription name, choose the free **Basic** support plan, and select **Upgrade**.

**What changes:**

- You keep the rest of your credit **until day 30 after sign-up**. Microsoft's example: sign up on 1 November, upgrade on 5 November, and unused credit stays until 30 November.
- The 12 months of free amounts continue.
- The **spending limit is gone**. Pay-as-you-go subscriptions cannot have one. When the credit runs out or day 30 passes, your card pays.
- Your budget alarm stays, and keeps sending emails.

Check that the upgrade finished: the subscription's **Overview** page shows the offer **Pay-As-You-Go**. A Databricks workspace created too early fails with an error about the subscription: wait 15 minutes and try again.

**Check the vCPU quota** (a vCPU is one virtual processor core; Azure caps how many you can run per region):

```bash
az vm list-usage --location centralindia -o table | grep -i -E "total regional|ddsv5"
```

The cluster in P10 task 20 needs **4 free vCPUs** in both lines, **Total Regional vCPUs** and **Standard DDSv5 Family vCPUs**. Free means `Limit` minus `CurrentValue`. If either has fewer than 4 free:

1. In the portal, search for **Quotas**, then choose **Compute**.
2. Filter on region **Central India** and find the family the error or the table names.
3. Request a new limit of at least 4 more than today.

A request can take hours. Check the quota on the first morning of week 20, before task 20.

## 9. What the Databricks week costs

Week 19 runs on the free credit and costs well under ₹200: storage, Data Factory and Key Vault.

In week 20, the Databricks workspace lives from task 20 to task 26, about **5 days (120 hours)**. Azure Databricks creates a **NAT gateway** (a network device for outbound internet traffic) in its managed resource group. Microsoft states that it "incurs additional cost". It bills every hour, used or not, until the workspace is deleted.

Prices are Microsoft's pay-as-you-go list prices for **Central India**, read from the Azure retail prices API on 13 November 2026. Microsoft publishes them in rupees and in US dollars; its rupee list uses about ₹95.23 to the dollar.

| Item | Quantity (if you follow the steps) | Price | Cost |
|---|---|---|---|
| NAT gateway | 120 hours | ₹4.2853 ($0.045) an hour | ₹514.24 |
| NAT gateway's public IP address (Standard, static) | 120 hours | ₹0.4761 ($0.005) an hour | ₹57.13 |
| Data through the NAT gateway | about 2 GB (estimate) | ₹4.2853 ($0.045) a GB | ₹8.57 |
| Cluster VM `Standard_D4ds_v5`, Linux | about 10 hours: 2 hours a day, with 20-minute automatic termination | ₹23.2358 ($0.244) an hour | ₹232.36 |
| Databricks DBUs (Databricks units: its software charge per hour of compute) | about 10 DBU-hours | ₹0 on the 14-day trial tier | ₹0 |
| Data Factory | about 300 activity runs, 2 DIU-hours of copying, 5 hours of pipeline and 5 of external activity | ₹95.2288 per 1,000 runs; ₹23.8072 per DIU-hour; ₹0.4761 and ₹0.0238 an hour | ₹78.68 |
| Disks, storage, Key Vault, transactions | small (estimate) | — | about ₹60 |
| **Total for week 20** | | | **about ₹950 (about USD 10)** |

**Who pays.** The credit is still yours until day 30 after sign-up. If you opened the account on the first day of week 19, day 30 is in week 23. USD 200 is about ₹19,046 at Microsoft's rate, and weeks 19 and 20 use about ₹1,150 of it. So if you follow the steps, the credit pays and **you pay ₹0 from your card**. If your credit has run out or day 30 has passed, your card pays about ₹950.

**What makes it cost more:**

| Mistake | Extra cost |
|---|---|
| The workspace lives one more day | ₹114.27 a day (NAT gateway and its IP address) |
| The workspace is forgotten for 30 days | ₹3,428 |
| A cluster without automatic termination | ₹23.24 an hour for the VM, plus ₹52.38 a DBU-hour after the 14-day trial |
| The same 10 cluster hours without the trial tier | ₹523.76 more for DBUs |

The budget alarm (₹2,000, emails at ₹1,000 and ₹2,000) catches these. It warns; it does not stop anything.

## 10. How to stop paying

1. **Tear down in P10 task 26**, as [`../teardown.md`](../teardown.md) shows: `terraform destroy`, then the empty listings.
2. **Then choose one:**
   - **Keep the subscription, empty.** An empty subscription costs nothing. Keep the budget alarm on, and check the cost once a week until the course ends.
   - **Cancel the subscription.** In **Subscriptions**, select it, then **Cancel subscription**. Billing stops at once; resources still running are switched off. Microsoft sends a final invoice for usage before the cancellation. You can delete the subscription 3 days later.
3. Do not delete your Microsoft Entra directory while you still use Fabric through it. That optional step is in [`../teardown.md`](../teardown.md).

## Troubleshooting

- **`az` or `terraform` not found:** close VS Code and open it again. For Terraform, check that `~/bin/terraform.exe` exists.
- **`The subscription is not registered to use namespace`:** run step 6 and wait 2 minutes.
- **`az consumption budget list` prints nothing:** a new subscription needs time. Wait 10 minutes, then try again. Microsoft says Cost Management features can take up to 48 hours on a new subscription.
- **Databricks says the subscription type is not supported:** the upgrade in step 8 is not finished.
- **`QuotaExceeded` when the cluster starts:** request more vCPUs for the family the error names (step 8).

## Sources, checked 13 November 2026

- Azure free account, India (Microsoft Azure): https://azure.microsoft.com/en-in/pricing/purchase-options/azure-account
- Free Trial offer MS-AZR-0044P (Microsoft Azure): https://azure.microsoft.com/en-in/pricing/offers/ms-azr-0044p
- Upgrade your Azure account (Microsoft Learn, 25 June 2026): https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/upgrade-azure-subscription
- Azure spending limit (Microsoft Learn, 29 April 2026): https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit
- Sign up for Azure Databricks for free (Microsoft Learn, 15 October 2026): https://learn.microsoft.com/en-us/azure/databricks/getting-started/free-trial
- Enable secure cluster connectivity, egress and the NAT gateway (Microsoft Learn, 8 October 2026): https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/secure-cluster-connectivity
- Azure retail prices API, Central India, USD and INR (Microsoft): https://prices.azure.com/api/retail/prices
- Install the Azure CLI on Windows (Microsoft Learn, 1 September 2026): https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows
- Sign in interactively with the Azure CLI (Microsoft Learn, 1 September 2026): https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli-interactively
- Security defaults, device code flow (Microsoft Learn): https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults
- Install Terraform (HashiCorp Developer): https://developer.hashicorp.com/terraform/install
- View quotas (Microsoft Learn): https://learn.microsoft.com/en-us/azure/quotas/view-quotas
- Cancel and delete your Azure subscription (Microsoft Learn, 7 June 2026): https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/cancel-azure-subscription
- Understand Cost Management data (Microsoft Learn): https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data
