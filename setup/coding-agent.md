# Coding agents: set one up and use it safely (capstone, from week 29)

A **coding agent** is an AI tool that reads your project, edits files and runs commands for you.
The course allows one **only from week 29**, in the capstone, after the card "Working with a coding agent". Before that, chat AI may help you learn, but you write the code.

Three rules come with it:

- You must be able to explain **every line** the agent wrote, at your demo and at Gate 8. If you cannot explain a line, do not keep it.
- **Never give an agent a secret.** Do not paste a key, a token, a password or the contents of `.env` into it, and do not ask it to read `.env`.
- Log every agent change in `capstone/AGENT_LOG.md` (see the end of this page).

Your mentor tells you which agent your centre uses. This page covers two that install on Windows without Node.js, checked on 13 November 2026.

## Which agent, and what it costs

| Agent | Where it runs | Cost for you | Good to know |
|---|---|---|---|
| **GitHub Copilot, agent mode** | Inside VS Code | **Copilot Free** includes agent mode, with a monthly allowance of "GitHub AI Credits". Verified students get **Copilot Student** free, through GitHub Education. Copilot Pro costs $10 a month; you do not need it | The easiest start: it is built into VS Code |
| **Claude Code** | Git Bash, PowerShell or VS Code | Needs a paid Claude plan (Pro, Max, Team or Enterprise) or an Anthropic Console (API) account. The free Claude plan does not include it | Use it when your centre gives you a seat |

Other agents exist, but most install with `npm`, and the course does not install Node.js. Use another agent only if your mentor names it and it installs without Node.js.

### Copilot Student

1. Sign in to GitHub and open https://github.com/settings/education/benefits.
2. Select **Start an application** and apply as a student. GitHub asks for proof that you study, such as your college email address or your student identity card.
3. When GitHub approves you (approval can take a few days), activate **Copilot Student** from the benefits page. GitHub checks every month that you are still a student.

Until you are approved, Copilot Free works, with a smaller allowance. Do not buy a paid plan.

## Install and sign in

### GitHub Copilot in VS Code

1. In VS Code, select the **Accounts** icon (bottom left) and sign in with GitHub.
2. Open the Chat view with Ctrl+Alt+I. VS Code sets up Copilot when you first open it.
3. In the Chat view, choose the **Agent** mode.

Check it: ask "Which files are in this folder?" The agent lists them.

### Claude Code

Install it in **PowerShell** with Anthropic's native installer (no Node.js, no administrator rights):

```powershell
irm https://claude.ai/install.ps1 | iex
```

Or with winget: `winget install Anthropic.ClaudeCode` (this copy does not update itself: run `winget upgrade Anthropic.ClaudeCode` now and then).

Open a new Git Bash terminal in your course repository and start it with `claude`. It opens your browser to sign in the first time. Claude Code runs its commands in Git Bash, because Git for Windows is installed.

Check it: `claude --version` prints a version number.

## The safe loop: brief, plan, small diff, review, test

Follow these steps for every change you ask an agent to make.

1. **Commit first.** Start from a clean `git status`, so you can always go back.
2. **Write a brief** in `capstone/agent-brief.md`: one change, the test that proves it works, and the files the agent may change. Add "no new packages", unless you need one. For example:
   - "Add a dbt model `marts/fct_daily_events.sql` that counts events per day and repository from `stg_events`. Add `not_null` and `unique` tests on its key in `marts/schema.yml`. Change only those two files."
   - "In `dags/careline_daily.py`, give the task `load_raw` 3 retries with a 5-minute delay. Change nothing else."
   - "Add a quality check that blocks the run when more than 1 % of `appointments.patient_id` values are empty. Add a test with a bad sample of 5 rows."
3. **Ask for a plan only:** "Read capstone/agent-brief.md and reply with a plan. Do not change any files yet."
   - Copilot: choose the **Plan** agent in the Chat view, then switch to **Agent** to carry it out.
   - Claude Code: switch to plan mode with Shift+Tab, or start it with `claude --permission-mode plan`.
4. **Check the plan.** It must name the files you expect and a test. Change what is wrong before you approve it.
5. **Let the agent make the change.** Keep each change small enough to read in one sitting.
6. **Read the diff:** run `git diff --stat`, then `git diff`, and read every changed line. Explain each line to yourself; look up what you cannot explain.
7. **Run the checks yourself**, for example:
   - `uv run python -m pytest -q` for Python code and quality checks;
   - `uv run dbt build --select fct_daily_events` for a dbt model and its tests;
   - `docker compose exec airflow airflow dags test careline_daily 2026-11-10` for a DAG.

   Never trust the agent's own report that the tests pass.
8. **Keep or undo.** Commit what you keep. Undo the rest with `git restore .` and delete any new files you do not want.
9. **Log it** in `capstone/AGENT_LOG.md` (see below).

## Rules that keep you safe

- **Approve each command.** Keep the agent in its default mode, where it asks before it runs a command or edits a file. Do not switch on any mode that approves everything. A data pipeline can delete a table or a bucket in one command.
- **Keep secrets out.** Keys stay in `.env`, which Git ignores. The agent never needs to see them: if a step needs a key, run that step yourself.
- **Keep real data out.** Do not paste rows of personal data (names, phone numbers, patient details) into an agent. Use the generated sample data or made-up rows.
- **Check every new package.** Agents sometimes invent package names, and attackers publish look-alike names. Before you accept a new package, find it on pypi.org under that exact name and check who maintains it.
- **Watch for weaker tests.** If the agent changed a test or a data check so that it passes, compare it with your brief. Restore the real check, and reject the change if the behaviour is wrong.
- **Stay in scope.** If the agent changes files outside your brief, reject the change and add "change only these files" to the brief.
- **Mind your data on free plans.** Your prompts and code may be used to train AI models. On GitHub, open **Settings**, then **Copilot**, and turn off "Allow GitHub to use my data for AI model training".
- **Undoing has limits.** Undo in the editor puts files back, but a command the agent already ran (a `DROP TABLE`, a `terraform apply`, an `rm`) stays done. That is why you commit first and approve each command.

## `capstone/AGENT_LOG.md`: one entry for each agent change

Keep one log in `capstone/AGENT_LOG.md`, and add an entry for every change an agent made. Each entry has six parts:

| Part | What you write |
|---|---|
| **Brief** | The change you asked for, or a link to `agent-brief.md` |
| **Plan** | The agent's plan in two or three lines, and what you changed in it |
| **Diff** | The `git diff --stat` output: which files changed, and how many lines |
| **Kept** | The parts you accepted, and why |
| **Rejected** | The parts you undid or asked the agent to redo, and why |
| **Tested** | The check you ran yourself, and its last lines |

An example entry:

```markdown
## 2026-12-09: daily events mart with tests

- **Brief:** capstone/agent-brief.md: add `models/marts/fct_daily_events.sql` (events per day and repository from `stg_events`) with `not_null` and `unique` tests on `(event_day, repo_id)`; change only the model and `marts/schema.yml`; no new packages.
- **Plan:** one model with a GROUP BY on `event_day` and `repo_id`, and a `unique_combination_of_columns` test. I changed the test to two `not_null` tests and a `unique` test on a surrogate key, because the project has no dbt_utils.
- **Diff:** 2 files changed, 31 insertions(+).
- **Kept:** the model and the three tests; I checked the GROUP BY against the grain in PLAN.md.
- **Rejected:** the agent also changed `stg_events.sql` to drop bot events; outside the brief, so I undid it and noted it as a later task.
- **Tested:** `uv run dbt build --select fct_daily_events`: PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4 (I ran it myself).
```

A log where nothing was ever rejected usually means the diffs were not read. Your mentor asks about your log at each Friday demo and at Gate 8.

## Official guides

- Plans for GitHub Copilot (GitHub Docs): https://docs.github.com/en/copilot/get-started/plans
- Free access with Copilot Student (GitHub Docs): https://docs.github.com/en/copilot/how-tos/manage-your-account/free-access-with-copilot-student
- Agents in VS Code (Visual Studio Code docs): https://code.visualstudio.com/docs/agents/overview
- Set up Claude Code (Anthropic): https://code.claude.com/docs/en/setup
- Best practices for Claude Code (Anthropic): https://code.claude.com/docs/en/best-practices
