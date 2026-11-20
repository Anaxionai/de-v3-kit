# AWS: your account on the free plan

In P11 (weeks 21 and 22), CycleCity part 2, you rebuild the bike pipeline from P10 on your own AWS account. This guide opens the account on the **Free plan**, in region **`ap-south-1`** (Asia Pacific (Mumbai)). It secures the account, makes an admin user for daily work, and sets up the `cyclecity` profile for the AWS CLI.

Run every command in Git Bash inside VS Code. Where PowerShell is different, the guide says so.

Create the budget alarm in [`../budget.md`](../budget.md) right after step 5, before you build anything.

## Before you start

You need all of these on the day you sign up:

- **A credit or debit card** that you can use online. AWS India asks for the card's CVV and may send you to your bank for a one-time password. It charges ₹2 and refunds it after the check.
- **An identity document.** Indian rules (CERT-In) make AWS check your identity before you can use any service. A personal account accepts a **PAN card**, a **voter ID card (EPIC)** or a **driving licence**. The name you type must match the document exactly.
- **A mobile phone** that receives SMS or calls, for a PIN.
- **An email address you will keep.** It becomes the sign-in name of the root user (the owner of the account).
- **An authenticator app** on your phone, for multi-factor authentication (MFA: a second proof of identity after the password).

The identity check finishes after sign-up, by email. AWS gives no time for it. Open the account on the first day of week 21, or during week 20, so the check is done before you need the account. No card or no document by week 20? Tell your mentor.

## Two sign-up pages: use "advanced"

AWS now has two ways to sign up. They give different accounts, and only one fits the course.

| | Sign up for AWS (new) | Sign up for AWS (advanced) |
|---|---|---|
| Page | `https://signin.aws.amazon.com/signup?request_type=builderId` | `https://signin.aws.amazon.com/signup?request_type=register` |
| How you sign in | Google, GitHub, Apple or Amazon login, through an AWS Builder ID | An email and password: the root user |
| Region | Chosen by AWS from your address. **India goes to Asia Pacific (Sydney), `ap-southeast-2`**, and it cannot be changed | You choose. `ap-south-1` is enabled from the start |
| IAM users | Allowed for programs only, not for the console | Allowed, with console sign-in |
| AWS Organizations and IAM Identity Center | Switched on for you | Not used |
| Payment method | Sometimes asked | Always asked |
| Services on the Free plan | A fixed list; Redshift, Kinesis, Data Firehose, EMR and MSK need the Paid plan | AWS's Free plan rules (see "What the free plan covers") |

The course uses **Sign up for AWS (advanced)** with the **Free plan**. Every P11 brief assumes `ap-south-1`, an IAM user and a root user.

Signed up with Google or GitHub by mistake? You are on the new page if the console talks about "projects" and "AWS Settings", or if your resource ARNs contain `ap-southeast-2`. Stop and tell your mentor. On the new page, choosing another Region needs "advanced features", and AWS says to upgrade to the Paid plan before you turn those on. Do not upgrade.

## 1. Open the account

1. Open `https://signin.aws.amazon.com/signup?request_type=register`. (On `aws.amazon.com`, **Create account** shows a banner with both options. Choose the **advanced** one.)
2. Enter your email and an account name, for example `<your-id>-de-course`. Choose **Verify email address** and type the code from the email.
3. Choose a strong password for the root user: 8 to 128 characters, with at least three of upper case, lower case, digits and symbols. Keep it in a password manager, never in a file.
4. Choose the **Free plan**. Do not choose the Paid plan.
5. Choose **Personal**, enter your contact details with your Indian address, and accept the AWS Customer Agreement.
6. On **Billing information**, enter your card and its CVV. Under **Do you have a PAN?**, choose **Yes** and type it if you want it on your tax invoices, or **No**. Choose **Verify and continue**. AWS India charges ₹2 and refunds it.
7. On **Confirm your identity**, choose the purpose of the account, the ownership type for an individual, and your document type and number. Choose the name that matches the document.
8. Verify your phone by SMS or voice call, and type the 4-digit PIN.
9. Choose the free **Basic support** plan, then **Complete sign up**.
10. Wait for two emails: account activation (minutes, at most 24 hours) and the result of the identity check. You can see the check under your account name, **Account**, **Customer verification**.

### Who you have the account with

With an Indian address, your agreement is with **Amazon Web Services India Private Limited (AWS India)**, a local seller. AWS's pages today use only this name. The addresses of those pages still contain `aispl`, the short form of the older name, Amazon Internet Services Private Limited (AISPL). What it changes:

- Your invoices are in **rupees (INR)**. Tax settings hold your PAN and GST numbers.
- The Free plan's **credits are counted in US dollars**: `aws freetier get-account-plan-state` reports them only in `USD`.
- AWS lists no Free plan exception for India. The only exception on its Free Tier page is the China regions.
- You can use every Region. `ap-south-1` is a default Region, enabled from the start.

## 2. Check the plan and the Region

1. Sign in at `https://console.aws.amazon.com` as the root user.
2. In the Region menu at the top right, choose **Asia Pacific (Mumbai) ap-south-1**. The console remembers it.
3. On **Console Home**, the **Cost and usage** widget shows your credit balance and the days left on the Free plan.

## 3. Protect the root user with MFA

AWS requires MFA on every root user. You must register it within 14 days of your first sign-in, so do it now.

1. Choose your account name at the top right, then **Security credentials**.
2. Under **Multi-factor authentication (MFA)**, choose **Assign MFA device**.
3. Choose a **passkey or security key** or an **authenticator app**, and follow the steps.

Never create access keys for the root user. After step 5, use the root user only for account and billing settings.

## 4. Let IAM users see billing

IAM users cannot open the billing pages until the root user allows it. Still signed in as root:

1. Choose your account name, then **Account**.
2. Scroll to **IAM user and role access to Billing information**, choose **Edit**.
3. Tick **Activate IAM Access** and choose **Update**.

## 5. Create your admin user

You work as an IAM user (a person's sign-in inside your account), not as the root user.

**Do not use IAM Identity Center.** It needs AWS Organizations, and a Free plan account that joins AWS Organizations is upgraded to the Paid plan automatically. For the same reason, never create or join an organization.

1. Open the **IAM** console, then **Users**, then **Create user**.
2. User name: `<your-id>-admin`. Tick **Provide user access to the AWS Management Console**, choose **I want to create an IAM user**, and set a custom password.
3. Choose **Attach policies directly**. Tick **AdministratorAccess** and **SignInLocalDevelopmentAccess** (the second one lets `aws login` work in step 7).
4. Choose **Create user**. Copy the **Console sign-in URL**: it contains your 12-digit account ID.
5. Sign out. Sign in again with that URL as `<your-id>-admin`.
6. Add MFA to this user too: **IAM**, **Users**, `<your-id>-admin`, **Security credentials**, **Assign MFA device**.

Now create the budget alarm: AWS section of [`../budget.md`](../budget.md). Setting up a cost budget also earns you USD 20 of extra credit.

## 6. Install or update the AWS CLI

You installed the AWS CLI version 2 for the laptop S3 emulator in P5. `aws login` needs version **2.32.0 or later**; the course version is in the kit's `VERSIONS.md`.

```bash
aws --version
```

It prints `aws-cli/2.` and the version. If it is older than 2.32.0, or `aws` is not found, update it:

```bash
winget upgrade -e --id Amazon.AWSCLI
```

If `winget` says it is not installed, use `winget install -e --id Amazon.AWSCLI`. AWS's own installer works too. In **PowerShell** (not Git Bash):

```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

Close VS Code and open it again, so Git Bash finds the new `aws`. Run `aws --version` again.

## 7. The `cyclecity` profile, with `aws login`

A profile is a named set of settings in `~/.aws/config`. The course uses two profiles for your real account:

- **`cyclecity-login`** holds your sign-in session from `aws login`.
- **`cyclecity`** is the one every brief uses. It asks `cyclecity-login` for short-lived keys, so the AWS CLI, Terraform and `boto3` all work.

Why two? `aws login` writes a session that the AWS CLI reads. AWS's table of tools says the Go SDK v2 cannot read it, and `boto3` reads it only with an extra package. The second profile hands the keys to every tool in the standard way.

**Sign in:**

```bash
aws login --profile cyclecity-login
```

1. It asks for a Region: type `ap-south-1`.
2. Your browser opens. Sign in as `<your-id>-admin` (not root), and choose that session.
3. Back in Git Bash, the command ends with a message that the profile is ready.

**Add the `cyclecity` profile.** Open the config file in VS Code:

```bash
code ~/.aws/config
```

Add this block at the end, and save:

```ini
[profile cyclecity]
credential_process = aws configure export-credentials --profile cyclecity-login --format process
region = ap-south-1
output = table
```

The file now also holds a `[profile cyclecity-login]` block with a `login_session` line (your user's ARN) and `region = ap-south-1`. It holds no key. The short-lived keys sit in `%USERPROFILE%\.aws\login\cache`, outside every repository.

**Check it:**

```bash
export AWS_PROFILE=cyclecity
aws sts get-caller-identity
```

The `Arn` ends with `user/<your-id>-admin`. The `Account` is your 12-digit account ID. If the `Arn` ends with `root`, you signed in as root in step 2: run `aws logout --profile cyclecity-login` and sign in again.

**Every working day:** run `aws login --profile cyclecity-login` once. A session lasts at most 12 hours. Then `export AWS_PROFILE=cyclecity` in each new terminal. The laptop emulator has its own profile, `emulator` ([`../../datalab/storage/README.md`](../../datalab/storage/README.md)); always check which profile is active with `echo $AWS_PROFILE`.

### If `aws login` does not work for you

Use access keys for the IAM user only if `aws login` fails after you updated the CLI:

1. **IAM**, **Users**, `<your-id>-admin`, **Security credentials**, **Create access key**, use case **Command Line Interface (CLI)**.
2. Run `aws configure --profile cyclecity` and paste the key ID and the secret when it asks. Region `ap-south-1`, output `table`.
3. The keys go to `~/.aws/credentials`, outside every repository. Never copy them into a project, a `.env` file or a chat.
4. Delete the access key in the teardown ([`../teardown.md`](../teardown.md)). A key works from anywhere until you delete it.

## What the free plan covers

**Credits.** A new account gets **USD 100** of credit. It can earn **up to USD 100 more**, USD 20 per activity in the **Explore AWS** widget on Console Home. The six activities:

- launch an EC2 instance;
- use a model in the Amazon Bedrock playground;
- **set up a cost budget** (this one costs nothing, and you do it anyway);
- create a web app with Lambda;
- create an RDS database;
- create a DynamoDB table.

The other five create resources that use credit. If you do them, delete what they made the same day.

**Services.** The Free plan leaves out services "that would rapidly consume the entire AWS Free Tier credit amount", and Savings Plans, Reserved Instances and hardware. AWS's Free plan page lists the allowed services only inside the browser. AWS's documented list for its new sign-up shows the picture:

| CycleCity uses on AWS | On the free plan? |
|---|---|
| Amazon S3, IAM, AWS Lambda, Amazon EventBridge | Yes |
| AWS Glue (Data Catalog, crawlers, Spark jobs), Amazon Athena | Yes |
| AWS Step Functions, AWS Secrets Manager, Amazon CloudWatch Logs | Yes |
| AWS Budgets, AWS Cost Explorer, the Free Tier API | Yes |
| Amazon Redshift, Amazon Kinesis Data Streams, Amazon Data Firehose, Amazon EMR, Amazon MSK | **No: Paid plan only** on AWS's list for the new sign-up |

CycleCity runs Kinesis and Redshift only on the laptop emulator, so the Free plan is enough. If a console page offers to upgrade your plan to use a service, stop and ask your mentor. Do not upgrade.

**The operator's trip files need no AWS permission.** They sit in the operator's public bucket in `us-east-1`, and CycleCity downloads them over HTTPS (`https://s3.amazonaws.com/tripdata/<file>`), not through the S3 API, so no policy in your account mentions that bucket. See [`../../data/bikes/README.md`](../../data/bikes/README.md).

**Expected use.** P11 uses about USD 1 to 2 of credit, mostly Glue crawls and job runs.

## When the credit or the six months run out

- The Free plan ends **after six months or when the credit is used up**, whichever comes first. For an account opened in week 21, six months is long after the course ends in week 30.
- You are never charged on the Free plan. When it ends, the account **closes automatically** and you lose access to your resources.
- AWS keeps your content for **90 days**, then deletes the account and everything in it. To keep the account, you would upgrade to the Paid plan within those 90 days; unused credit then pays future bills.
- These actions upgrade a Free plan to the Paid plan automatically. Do none of them:
  - joining AWS Organizations;
  - setting up an AWS Control Tower landing zone;
  - joining the AWS Partner Network;
  - a Professional Services contract or an Enterprise Agreement;
  - an AWS Skill Builder Team subscription;
  - marking the account HIPAA or SEC compliant.

Check the plan at any time:

```bash
aws freetier get-account-plan-state --output table
```

| Field | What you should see |
|---|---|
| `accountPlanType` | `FREE` |
| `accountPlanStatus` | `ACTIVE` (later `EXPIRED`) |
| `accountPlanRemainingCredits` | `amount` and `unit` `USD` |
| `accountPlanExpirationDate` | the day the Free plan ends |

## Reading the cost

- Open **Billing and Cost Management**, then **Cost Explorer**, on your first day. AWS shows the current month about **24 hours** after Cost Explorer is first opened.
- The console is free to look at. Each **Cost Explorer API** call, such as `aws ce get-cost-and-usage`, costs **USD 0.01**. On the Free plan it comes out of your credit. Run it once per task that asks for it.

## Troubleshooting

- **The identity check failed:** the name must match the document exactly. Edit it under **Account**, **Customer verification**, and submit again.
- **`aws: error: argument command: Invalid choice` for `login`:** the CLI is older than 2.32.0. Update it (step 6).
- **`Unable to locate credentials`, or an expired-token error:** your 12-hour session ended. Run `aws login --profile cyclecity-login`.
- **Terraform says `No valid credential sources found`:** use `export AWS_PROFILE=cyclecity`, not `cyclecity-login`.
- **`AccessDenied` on billing pages as the IAM user:** step 4 is missing. Do it as root.
- **An ARN or error shows `ap-southeast-2` or another Region:** check `aws configure get region --profile cyclecity`. It must print `ap-south-1`.

## Sources, checked 13 November 2026

- Compare sign-up options (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/sign-up-for-aws.html
- Sign up for AWS (advanced) (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html
- Sign up for AWS (new) (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html
- AWS Regions for your projects, with the India row (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/project-regions.html
- Supported AWS services for Sign up for AWS (new) (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html
- Activate advanced AWS features (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/activate-advanced-features.html
- Manage accounts in India (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/managing-accounts-india.html
- Setting up your India billing (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-account-payment-aispl.html
- Enable or disable AWS Regions, default Regions (AWS Account Management): https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html
- Choosing a plan (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- Explore AWS services with AWS Free Tier (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html
- Earning additional credits (AWS Billing): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans-activities.html
- AWS Free Tier FAQs (AWS): https://aws.amazon.com/free/free-tier-faqs/
- MFA for the root user (IAM docs): https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-mfa-for-root.html
- Grant access to your billing information (IAM docs): https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_billing.html
- Login for AWS local development using console credentials (AWS CLI docs): https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html
- Login credentials provider, support by SDKs and tools (AWS SDKs and Tools reference): https://docs.aws.amazon.com/sdkref/latest/guide/feature-login-credentials.html
- Installing the AWS CLI (AWS CLI docs): https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- get-account-plan-state (AWS CLI 2.40.1 reference): https://docs.aws.amazon.com/cli/latest/reference/freetier/get-account-plan-state.html
- Enabling Cost Explorer (AWS Cost Management): https://docs.aws.amazon.com/cost-management/latest/userguide/ce-enable.html
- AWS Cost Explorer pricing (AWS): https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/
