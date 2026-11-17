# Microsoft Fabric: signing in and the trial

You use Microsoft Fabric in P10: card 17 tries a lakehouse, and task 25 serves CycleCity's gold tables from one (week 20). In P14 (week 25), publishing a Power BI report is a Stretch goal. Fabric costs you nothing on either route below.

Fabric does not accept a personal email account such as Gmail or Outlook.com directly. You sign in with a work account in a Microsoft Entra directory (a tenant: an organisation's list of users). There are two ways to get one:

| Route | Account | Status |
|---|---|---|
| **A. A user in your own Azure directory** (use this first) | a user you create in the directory of your Azure free account from week 19 | **Confirmed**: Microsoft documents it (page dated 27 February 2026). Not yet tried by the course team |
| **B. Your centre's account** (fallback) | a work account your centre creates for you | The centre's set-up |

If route A does not give you a trial, use route B. Your mentor tells you which route your cohort uses.

## Route A: with a user in your own Azure directory

Status: **confirmed** on Microsoft's page "Start a Microsoft Fabric free trial with a personal email" (checked 13 November 2026). The steps below follow that page.

### A1. Create the Fabric user

You need the Azure free account from [`../azure/README.md`](../azure/README.md). Its sign-up created a directory, and you are its owner.

1. In the Azure portal, search for and open **Microsoft Entra ID**.
2. In the left menu, expand **Manage** and select **Users**.
3. Select **New user**, then **Create new user**.
4. **User principal name** (the sign-in name): type `fabric`. The domain after `@` is your directory's, ending in `.onmicrosoft.com`. Keep it.
5. **Display name**: `<your-id> Fabric`. Let Azure generate the password, and copy it into your password manager. Never put it in a file in a repository.
6. Leave roles and other properties as they are. Select **Review + create**, then **Create**.
7. Open **Users** again and copy the new user's **user principal name**, for example `fabric@yourname123.onmicrosoft.com`.

### A2. Sign in and set up multi-factor sign-in

1. Open a private browser window and go to `https://app.fabric.microsoft.com`.
2. Sign in with the user principal name and the password. Set a new password when asked.
3. Your new directory has **security defaults** switched on, so Microsoft asks you to register multi-factor authentication (MFA: a second proof after the password) at this first sign-in. There is no 14-day delay any more.
   - **Microsoft Authenticator** on your phone: you register it by approving a notification. Later sign-ins can use its notification or its 6-digit code.
   - Any other authenticator app that makes 6-digit codes (an OATH TOTP app) can also give the codes.
4. Complete any other prompts.

### A3. Start your trial

1. In the Fabric portal, select your profile picture at the top right (the **Account manager**).
2. Select **Free trial** (it may say **Start trial**).
3. Choose the capacity region **Central India**, agree to the terms, and select **Activate**.

What you get:

- A **60-day** trial capacity (shared compute for Fabric): either **F4** or **F64**, Microsoft decides which.
- A **Power BI Individual Trial** with it, if you have no paid Power BI licence.
- Up to **1 TB** of data in OneLake (Fabric's storage).

Check the days left in the Account manager, under **Trial status**.

### A4. Create your workspace

1. Select **Workspaces**, then **New workspace**.
2. Name it `cyclecity-<your-id>`.
3. Under the advanced settings, choose the trial licence mode (shown as **Trial** or **Fabric Trial**), and select **Apply**.

### If "Free trial" does not appear

Two tenant settings (switches for the whole directory) control trials. Their defaults are not published. As the directory's owner you can switch them on:

1. Give your Fabric user the right to change them. In the Azure portal, open **Microsoft Entra ID**, then **Roles and administrators**. Select **Fabric Administrator**, then **Add assignments**, and choose your `fabric` user.
2. Sign out of Fabric, and sign in again as the `fabric` user.
3. Open **OneLake catalog**, then **Govern**, then **Configurations**, then **Tenant settings**. (The **Settings** gear, then **Admin portal**, opens the same page.)
4. Turn on **Users can create Fabric items**.
5. Under **Help and support settings**, turn on **Users can try Microsoft Fabric paid features**.
6. Try A3 again.

Still no trial? Microsoft writes that it "determines trial availability by region and tenant". Tell your mentor, and use route B or your mentor's demonstration.

## Route B: with your centre's account

Your centre creates a work account for you and runs **one shared trial** for the whole cohort.

1. If your own trial does not appear, your mentor gives you a user name and a temporary password in week 20.
2. Sign in at `https://app.fabric.microsoft.com`. Set a new password, then register multi-factor sign-in with Microsoft Authenticator, as in A2.
3. **Do not select Start trial.** Microsoft limits the number of trial capacities in one directory. If every student starts one, the cohort runs out. Use the shared trial.
4. Open the workspace your mentor names, normally `cyclecity-<your-id>` on the centre's trial capacity.

Never sign in to a centre account with a device code (a short code typed on another device). New directories block it.

If the sign-in says your account cannot use Fabric, or you see no workspace, tell your mentor before you start P10 task 25.

## Using Fabric in P10

- Lakehouse names allow letters, digits and underscores only: `try_lh` and `cyclecity_lh`, not `cyclecity-lh`.
- **Files** hold uploaded files. **Load to Tables** turns a CSV or Parquet file or folder into a Delta table under **Tables**.
- The **SQL analytics endpoint** of a lakehouse runs read-only T-SQL. Write your queries in `cyclecity/fabric/queries.sql` too, so they are in Git when the trial ends.
- Central India runs every Fabric workload.

## Power BI in P14

With the free Fabric licence, you can publish a report to **My workspace**. Creating Power BI items in any other workspace, or sharing, needs a Pro licence or the trial. Publishing is a P14 Stretch goal; nothing in a Core task depends on it.

## When the trial ends

A trial started on the first day of week 20 ends **60 days later, in week 28**.

- Workspaces on the trial capacity change back to the Pro type. Fabric items that are not Power BI items (lakehouses, notebooks, pipelines) become inactive.
- Their content stays in OneLake for **7 days**, then may be deleted.
- Another trial is not guaranteed: Microsoft "might restrict repeated or successive trial usage".
- Your SQL and your evidence are already in your repository. Nothing else needs saving.

## Cost

- The trial and the free Fabric licence cost nothing. Fabric does not charge your Azure card.
- The `fabric` user needs no paid licence.
- Optional clean-up after week 28 (deleting the directory) is in [`../teardown.md`](../teardown.md).

## Sources, checked 13 November 2026

- Start a Microsoft Fabric free trial with a personal email (Microsoft Learn, 27 February 2026): https://learn.microsoft.com/en-us/fabric/fundamentals/free-trial-account-personal-email
- Fabric trial capacity (Microsoft Learn, 12 August 2026): https://learn.microsoft.com/en-us/fabric/fundamentals/fabric-trial
- Fabric administration roles (Microsoft Learn, 21 April 2026): https://learn.microsoft.com/en-us/fabric/admin/roles
- Fabric region availability (Microsoft Learn, 3 November 2026): https://learn.microsoft.com/en-us/fabric/admin/region-availability
- Microsoft Fabric licences (Microsoft Learn, 15 June 2026): https://learn.microsoft.com/en-us/fabric/enterprise/licenses
- Sign up for the Power BI service as an individual, "You can't use consumer email accounts" (Microsoft Learn, 23 March 2026): https://learn.microsoft.com/en-us/power-bi/fundamentals/service-self-service-signup-for-power-bi
- Security defaults in Microsoft Entra ID (Microsoft Learn): https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults
- Create, invite and delete users (Microsoft Learn): https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users
