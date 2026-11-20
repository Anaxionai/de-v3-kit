# Snowflake: the trial, the CLI and key-pair sign-in

In P9 (weeks 17 and 18) you build GitPulse on your own Snowflake trial. You open it in card 1, on the first day of week 17. P9 task 8 sets the spending limit (the resource monitor in [`../budget.md`](../budget.md)), installs the Snowflake CLI and signs it in with a key pair. Until task 8, use only the steps in the cards.

Run every command in Git Bash inside VS Code.

## 1. Open the trial

1. Open `https://signup.snowflake.com`.
2. Enter your name, your email, and the other details the form asks for.
3. Choose these three, exactly:
   - **Edition: Standard.** Its credits cost less, and one day of Time Travel is enough for the course.
   - **Cloud provider: Amazon Web Services (AWS).**
   - **Region: Asia Pacific (Mumbai)**, which is `ap-south-1`.
4. Snowflake asks for **no card and no payment details**.
5. Open the activation email, choose your user name and password, and sign in. Snowsight (Snowflake's web interface) opens.
6. If Snowsight offers multi-factor authentication (MFA: a second proof after the password), set it up with an authenticator app or a passkey. Snowflake's MFA rollout phases do not apply to trial accounts, and Duo MFA is not available in trials.

**The trial gives you USD 400 of free usage for 30 days**, whichever runs out first. At the Standard price on AWS Mumbai (USD 2.20 a credit, [`../budget.md`](../budget.md)), USD 400 is about 181 credits. P9 is designed to use under 20.

## 2. Your identifiers

In a Snowsight SQL worksheet with the role `ACCOUNTADMIN`, run:

```sql
SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME() AS account_identifier,
       CURRENT_USER() AS user_name;
SHOW DATABASES LIKE 'SNOWFLAKE_SAMPLE_DATA';
```

- `account_identifier` has the form `orgname-accountname`. The CLI and dbt use it.
- `user_name` is your user, in upper case.
- The second statement shows one row. If it shows none, card 1's Stuck line adds the sample database.

Keep the identifier and the user name in your notes. They are not secret, but they still go in `.env` files, never in committed code.

## 3. Install the Snowflake CLI

The Snowflake CLI (`snow`) needs Python 3.11 or later. Install it with uv, at the version in the kit's `VERSIONS.md` (3.33.0 in November 2026):

```bash
uv tool install --python 3.12 snowflake-cli==3.33.0
snow --version
```

The second command prints the version, 3.33.0. Always pass `--python 3.12`: Windows laptops with Smart App Control on block uv's newest Python (see the kit's `setup/windows.md`).

### Where its settings live

On Windows, `snow` keeps its connections in `%USERPROFILE%\AppData\Local\snowflake\config.toml`, unless a folder `~/.snowflake` exists. If `~/.snowflake` exists, it uses that folder instead. Do not create `~/.snowflake` by accident. To see which file is in use:

```bash
snow --info
```

The file holds account names and key paths. It holds no password and no key, and it is outside every repository.

## 4. Make a key pair

A key pair is two linked files: a private key that stays on your laptop, and a public key you give Snowflake. The CLI proves who you are with the private key, so no password is typed or stored.

```bash
mkdir -p ~/snowflake-keys
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/snowflake-keys/gitpulse_key.p8 -nocrypt
openssl rsa -in ~/snowflake-keys/gitpulse_key.p8 -pubout -out ~/snowflake-keys/gitpulse_key.pub
```

`openssl` comes with Git for Windows.

**Why an unencrypted private key is acceptable here:** it lives in `~/snowflake-keys/`, outside every repository, and it opens only your trial account. Never copy it into a project folder, a `.env` file, a chat or an issue. If you prefer an encrypted key, leave out `-nocrypt`; `openssl` asks for a passphrase, and you set it in the `PRIVATE_KEY_PASSPHRASE` environment variable before each `snow` session.

## 5. Give Snowflake the public key

Print the public key as one line, without its first and last lines:

```bash
grep -v "PUBLIC KEY" ~/snowflake-keys/gitpulse_key.pub | tr -d '\n'
```

In a Snowsight worksheet as `ACCOUNTADMIN`, paste it between the quotes:

```sql
ALTER USER <your user name> SET RSA_PUBLIC_KEY = 'MIIBIjANBgkqh...';
DESC USER <your user name>;
```

In the `DESC USER` result, find `RSA_PUBLIC_KEY_FP`. It starts with `SHA256:`. Compare it with your file's fingerprint:

```bash
openssl rsa -pubin -in ~/snowflake-keys/gitpulse_key.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64
```

The text after `SHA256:` and this output must be the same.

## 6. Add the `gitpulse` connection

The connection needs the private key's full Windows path. Print it:

```bash
cygpath -m ~/snowflake-keys/gitpulse_key.p8
```

It prints a path such as `C:/Users/<you>/snowflake-keys/gitpulse_key.p8`. Then run:

```bash
snow connection add
```

Answer the questions like this. Press Enter to skip any question not in the table.

| Question | Answer |
|---|---|
| Name for this connection | `gitpulse` |
| Account | your `orgname-accountname` |
| User | your user name |
| Password | leave empty |
| Role | `GITPULSE_LOADER` |
| Warehouse | `GITPULSE_WH` |
| Database | `GITPULSE` |
| Schema | `RAW` |
| Authenticator | `SNOWFLAKE_JWT` |
| Private key file | the path from `cygpath -m` |

Make it the default and test it:

```bash
snow connection set-default gitpulse
snow connection test
```

The test prints a table with the connection's account, user and role. An error instead of the table means the sign-in failed: see Troubleshooting.

## 7. Using `snow`

| Command | What it does |
|---|---|
| `snow sql -q "SELECT CURRENT_ROLE()"` | runs one statement |
| `snow sql -f snowflake/04_raw_events.sql` | runs a file; one result table per statement |
| `snow sql --role ACCOUNTADMIN -q "SHOW RESOURCE MONITORS"` | runs with another role you hold |
| `snow sql --format json -q "..."` | prints JSON instead of a table |
| `snow stage copy "data/gharchive/*.json.gz" @GITPULSE.RAW.GHARCHIVE_STAGE` | uploads files to the stage; run it from `gitpulse/` |

Keep the quotes around the file pattern, so `snow` reads it instead of Git Bash. In the `stage copy` output, `UPLOADED` means the file was sent. `SKIPPED` means a file with that name is already on the stage; `stage copy` does not overwrite unless you ask it to.

## 8. The CI key (P9 task 26)

The GitHub Actions workflow signs in as a separate service user, `GITPULSE_CI`, with its own key pair. Make it the same way:

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/snowflake-keys/gitpulse_ci_key.p8 -nocrypt
openssl rsa -in ~/snowflake-keys/gitpulse_ci_key.p8 -pubout -out ~/snowflake-keys/gitpulse_ci_key.pub
```

Task 26 sets the public key on `GITPULSE_CI` and stores the private key text in the repository's Actions secret `SNOWFLAKE_CI_PRIVATE_KEY`. It is never in a file in the repository. The teardown deletes both key files and both secrets.

## 9. When the trial ends

- The trial runs **30 days from sign-up, or until the USD 400 is used**, whichever comes first. Opened on the first day of week 17, it ends in week 21. P9 ends in week 18.
- At the end, Snowflake **suspends** the account. You can still sign in, but you cannot run warehouses, load data or query. Unused free usage expires.
- **No charge** follows: you gave no payment details. Adding a card does not upgrade a trial on its own; upgrading is a separate step. Do not upgrade.
- A trial cannot be cancelled in Snowsight. Only Snowflake Support can cancel it. You do not need to: tear down in P9 task 27 ([`../teardown.md`](../teardown.md)) and let the trial end.
- Users with `ACCOUNTADMIN` see the free balance left on a tile in Snowsight's left navigation bar.
- Not available in trials: external network access, hybrid tables, outbound private connectivity, Snowflake Openflow, Duo MFA. AI features stay off until a card is added. P9 uses none of them.

## Troubleshooting

- **`snow: command not found`:** run `uv tool update-shell`, then close VS Code and open it again. uv puts tool programs in `~/.local/bin`.
- **`JWT token is invalid`:** the public key in `ALTER USER` must be one line, without the `BEGIN` and `END` lines, and the user name must match. Compare the fingerprints (step 5).
- **`snow` uses the wrong settings:** run `snow --info` and check which `config.toml` it reads.
- **The private key file is not found:** use the `C:/Users/...` path from `cygpath -m`, not a path that starts with `~`.

## Sources, checked 13 November 2026

- Trial accounts (Snowflake docs): https://docs.snowflake.com/en/user-guide/admin-trial-account
- Start your free trial, "Receive $400 worth of free usage" (Snowflake): https://info.snowflake.net/start-your-free-trial.html
- Pricing guide, AWS Mumbai prices (Snowflake): https://www.snowflake.com/pricing/pricing-guide/
- Supported cloud regions (Snowflake docs): https://docs.snowflake.com/en/user-guide/intro-regions
- MFA rollout, phases and trial accounts (Snowflake docs): https://docs.snowflake.com/en/user-guide/security-mfa-rollout
- Account identifiers (Snowflake docs): https://docs.snowflake.com/en/user-guide/admin-account-identifier
- Installing Snowflake CLI (Snowflake docs): https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation
- Configuring Snowflake CLI and connections (Snowflake docs): https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections
- Key-pair authentication (Snowflake docs): https://docs.snowflake.com/en/user-guide/key-pair-auth
- snow stage copy (Snowflake docs): https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/stage-commands/copy
- snowflake-cli on PyPI: https://pypi.org/project/snowflake-cli/
