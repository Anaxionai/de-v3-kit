# Your personal capstone

In the last four weeks of the course you build your own data product: a pipeline that answers one real question for one named user, from a public source that changes over time. You plan it in week 27, and your mentor approves the plan. Your own tasks for weeks 28 to 30 are then created from that plan. You build with your own code from the course projects, and from week 29 a coding agent may help.

## The four weeks

| Week | Module | What happens | Gate |
|---|---|---|---|
| 27 | CP1: plan and design | Five learn cards, then your plan, one part per task. A plan review with your mentor at the end of the week. | |
| 28 | CP2: build (milestone M1) | Your own tasks, about 18 hours: setup with tests on every push, ingestion that is safe to re-run, the storage layers, the core model and the data tests. Chat AI may help. **No coding agent.** Friday demo. | |
| 29 | CP2: build (milestone M2) | Your own tasks, about 17 hours: the tables that answer your question, orchestration, the serving part, the cost note and the teardown script. **A coding agent may help**, only in the tasks that say so, after the card "Working with a coding agent". Demo. | G8 at the end of week 29 |
| 30 | CP3: ship and defend (milestone M3) | Your own tasks, about 5 hours: fixes after the Gate 8 review, and one full run from empty on the real cloud. Then the course tasks: README, architecture page, demo video, portfolio, resume, interview stories. | G9, the final defence |

The milestone hours (about 18, 17 and 5) leave room for each week's course tasks, demos, mock interviews and the SQL drill.

## How it works, step by step

### 1. Choose a brief, or pitch your own product

Read the four briefs in [`briefs/`](briefs/README.md) and choose one:

| Brief | The product |
|---|---|
| [Clean Hours](briefs/clean-hours.md) | When is grid electricity cleanest? For a depot that charges electric vans at night |
| [City Fix](briefs/city-fix.md) | How fast does a city close residents' requests? For the analyst who reports to borough managers |
| [River Rise](briefs/river-rise.md) | Which rivers rise fastest after heavy rain? For a council's flood-response planner |
| [Research Pulse](briefs/research-pulse.md) | Which journals publish more, and how fast are new papers cited? For a library's subscriptions manager |

#### Pitch your own product

You may pitch your own data product instead, if it passes these four tests:

1. It fits about 40 hours across weeks 28 to 30 (M1 about 18 hours, M2 about 17 hours, M3 about 5 hours) with one or two sources.
2. It covers all seven required parts (below).
3. Its main source is real, public, reachable, changes over time, and its licence allows use in a paid course. A "non-commercial only" licence fails this test.
4. It needs no real personal data (or masks it after the raw layer, as in P13), and at most three ideas the course has not taught.

[`briefs/README.md`](briefs/README.md) shows how to check a source by hand before you pitch, and what makes a pitch too big. Show your `## Product` to your mentor on the day you pitch.

### 2. Fill in your plan

In CP1 task 7, copy [`plan-template/PLAN.md`](plan-template/PLAN.md) to `capstone/PLAN.md` in your task folder. Each later CP1 task copies your `capstone/` folder forward and fills the next part:

| CP1 task | What it fills |
|---|---|
| 7. Choose a brief or pitch your own data product | The top lines, `## Product`, and the first draft of `## Required parts` |
| 8. Write the question, the users and five success measures | `## Question and users`, with `### Users` and `### Success measures` |
| 9. Find and vet your data sources | `## Sources`, one `###` per source, and `evidence.md` |
| 10. Draw the architecture and the data model | `## Architecture` (`### Context`, `### Pipeline`) and `## Data model` |
| 11. Write the data contract for your main table | `capstone/contracts/<table>.yaml` and `## Data contract` |
| 12. Write three decision records | `capstone/docs/decisions/0001-<short-name>.md` to `0003-...`, and `## Decisions` |
| 13. Design for ten times the load, on paper | `## Load and failure` (`### Today`, `### Ten times the load`, `### Failures`) |
| 14. Estimate the monthly cost on two clouds and choose one | `## Cost` |
| 15. Split the work into milestones and submit the plan | `## Milestones` (`### Backlog`, `### M1 (week 28)`, `### M2 (week 29)`, `### M3 (week 30)`), `## Risks`, and the Milestone column of `## Required parts` |
| 16. Plan review with your mentor | `capstone/PLAN-REVIEW.md`, `EXPLAIN.md`, and the changes the review asks for |

Keep every heading of `PLAN.md` exactly as it is. The script that creates your tasks finds each part by its heading.

### 3. Your mentor reviews the plan

At the end of week 27 you have a plan review with your mentor. Find it on Calendar and answer Going. You walk through your plan in 5 minutes, then your mentor gives numbered notes. Your mentor checks, among other things, that:

- the milestones fit their hours, and each one ends with something that runs;
- all seven required parts are there, each with a Must item in the backlog;
- your source's licence allows the use, and `evidence.md` shows it answering;
- your cloud account is still open in weeks 28 to 30, with a budget alarm and a teardown plan;
- you have a route for an 8 GB laptop, if yours has 8 GB;
- every proof you plan is text that AxReview can read.

Write every note in `capstone/PLAN-REVIEW.md`, change the plan to match, and record the outcome: approved, or sent back with the date of a second review.

### 4. Your own tasks are created from the approved plan

After approval, your tasks for weeks 28 to 30 are created from the `capstone/PLAN.md` **in the folder of CP1 task 16**, the plan review. Keep the plan up to date there until your mentor approves it.

- Each backlog item of 1 to 3 hours becomes one task. If your plan names an idea the course never taught, a 1-hour learn card comes before the task that needs it.
- Each task has a brief and a "What AxReview checks" list, like every other task in the course, and AxReview grades it the same way.
- For now, staff create your tasks with a script, until the portal can do it itself. The portal sends you one notification and one email for each task: about 15 at once. Your mentor tells you before it happens.

## Your board

Your own tasks appear in the portal under Module, **after the module's course tasks**. Each one says "Assigned to you", and its title starts with its week: `Week 28: ...`, `Week 29: ...` or `Week 30: ...`.

**Board order is not week order.** Read the board with this table:

| Module on the board | In this order | When you do them |
|---|---|---|
| CP2 | 1. "How your capstone tasks work: the board, reviews and re-planning" | Monday of week 28, first |
| | 2. "Working with a coding agent: briefs, review and the AGENT_LOG" and 3. its concept check | Monday of week 29. Leave them until then. |
| | Your `Week 28: ...` tasks | Week 28, in board order |
| | Your `Week 29: ...` tasks | Week 29, in board order |
| | "Friday demos to your mentor, weeks 28 and 29" | Notes after each demo; submit at the end of week 29 |
| CP3 | Course tasks 1 to 8: portfolio, interviews, README, profile, resume, stories, mock feedback | Week 30. Do task 4, the README and architecture page, after your own run from empty. |
| | Your `Week 30: ...` tasks | Week 30, first: final fixes, then the run from empty |
| | "Final defence: present, answer questions and share your record" | The last task of the course |

## How your tasks are reviewed

- **AxReview reads only the files committed in that task's folder, and never runs your code.** So the proof is text: row counts, test output, query results and logs, pasted into `evidence.md` in the task folder, beside the code. A screenshot is welcome for people, but it never counts as proof.
- **Read "What AxReview checks" before you build.** Under "Files to hand in" are the files AxReview opens. Under "Needed to pass" are the checks; at least one usually needs pasted output.
- **Your product lives in a `capstone/` folder inside each task folder.** Each task starts by copying `capstone/` forward from the task before it, and says which task that is. Your first own task copies it from the folder of CP1 task 16. Leave out `.venv/` and `data/` when you copy: data stays out of Git.
- **Fix "Changes requested" before you go on.** Later tasks copy that task's `capstone/` folder, so a fault you leave travels with it.
- **Show working software every week.** Each Friday in weeks 28 and 29 you show your mentor what runs, at a demo that is on Calendar: answer Going. In week 29 the demo may move to Wednesday, because Gate 8 takes the end of the week. Bring the row counts before and after one re-run of your ingestion.
- **Gate 8** at the end of week 29 checks the build. Your mentor asks you to draw your pipeline from memory, run the ingestion twice, break an input file, give the cost so far, show one change the coding agent made that you rejected, and add one column end to end while they watch.

## Re-planning

Plans change. If a task is too big or a source stops working, talk to your mentor, usually at the Friday demo. When you agree a change:

1. You update `capstone/PLAN.md` in your current task folder to match. Raise `Plan version` by one.
2. Only tasks you have not started are swapped or removed. Tasks you have started stay on your record, with your work and their reviews.
3. A change may not remove one of the seven required parts, and each week must still fit its hours.
4. If a new task needs an idea the course never taught, your mentor adds a learn card before it.

Staff then create the new tasks with the same script.

## The seven required parts

Every approved plan has all seven, each with at least one Must item in the backlog:

| Required part | What it means | Where you learnt it |
|---|---|---|
| 1. A question and a named user | One question a user decides with, and success measures with numbers | CP1 |
| 2. Ingestion that is safe to re-run | Loading from a source that changes over time: a second run, or a backfill, gives the same rows | ClearAir (P4), PageLake (P5) |
| 3. A warehouse or lakehouse with a documented model | Layers (raw, clean, ready to use) and a star schema with a stated grain | RetailBase (P3), PageLake (P5), TaxiScale (P7), GitPulse (P9) |
| 4. Orchestration with retries and a backfill | A scheduler that runs the steps, retries a failed step, alerts someone and runs past days | PageLake part 2 (P6); also Data Factory (P10) and Step Functions (P11) |
| 5. Data tests that block bad data, and a data contract | Checks that stop a bad load, checks that warn, and a contract for the main table | GitPulse dbt tests (P9), CareLine (P13) |
| 6. One real cloud, built with Terraform, with a cost note and a teardown | At least one part of the product on a real cloud account, built from Terraform files, with what it cost and the command that deletes it | Terraform in CycleCity on Azure (P10) and on AWS (P11); teardowns in P9 to P11 |
| 7. Something a person can open: a report or a dashboard | A Markdown report the pipeline writes, or a Power BI report | Week 1 findings (LP), RetailBase part 2 (P14) |

An HTTP API as the serving part is possible, but the course never taught you to build one: it counts as one untaught idea, with a learn card before it.

Reuse your own code from the course projects: it is your parts bin. Copying another student's code is not reuse.

## Your cloud in weeks 28 to 30

By week 28 the Snowflake trial and the Azure free credit have ended. These are still open:

| Account | What it gives you | What to watch |
|---|---|---|
| AWS free plan (opened in week 21) | S3, the Glue Data Catalog, Athena with Iceberg tables, Lambda, Step Functions. Terraform was taught on AWS in P11. | The account closes 6 months after you opened it, or when its credits run out, whichever comes first. |
| BigQuery's free allowance (P12) | 1 TiB of queries a month and 10 GiB of storage | The no-card sandbox has no `MERGE` or other DML, and deletes tables after 60 days. Terraform for Google Cloud is an untaught idea. |
| Databricks Free Edition (P7) | Serverless compute, Delta tables and jobs | A daily compute limit; its compute reaches only a limited list of websites. Terraform for Databricks is an untaught idea. |
| The laptop lab | PostgreSQL, the S3 emulator, Airflow and Spark, with `lite` profiles | Free, but it is not a real cloud: it does not meet required part 6 on its own. |

Most plans use the AWS free plan, because every part of it was taught. Whatever you choose, the rules of [`cloud/README.md`](../cloud/README.md) apply: a budget alarm before the first resource ([`cloud/budget.md`](../cloud/budget.md)), the smallest size of everything, nothing that bills while idle, and a teardown with proof at the end ([`cloud/teardown.md`](../cloud/teardown.md)).

**On an 8 GB laptop**, start one product stack at a time with its `lite` profile, let the cloud do the heavy queries, and work on one day or one month of data at a time. Your plan names this route, and your mentor checks it at the review.

## The AI rules

| Tool | When | What you record |
|---|---|---|
| AxTutor | Every week | Nothing. It teaches and quizzes; it does not write your product. |
| Chat AI, such as ChatGPT, Claude or Gemini | Every week of the capstone, to explain, review or suggest | Each use in `AI_LOG.md` in the task folder: what you asked, what it said, what you kept, what you changed, and what was wrong |
| A coding agent (an AI tool that edits your files and runs commands), the one your centre provides | **From week 29 only**, after the card "Working with a coding agent", and only in the tasks that say so | Each use in `capstone/AGENT_LOG.md`, in six parts (below) |

**Why no agent in week 28?** In week 28 you build the core yourself: ingestion, storage, the model and the tests. At Gate 8 you must explain every line of it, so you write it.

Each `AGENT_LOG.md` entry has six parts, as the card "Working with a coding agent" teaches. The log lives in `capstone/` and is copied forward with it, so it grows from task to task:

```
## 2026-12-02 · Fuel mix in the report
Brief:    capstone/docs/agent-briefs/fuel-mix.md: add the wind and solar share to each cleanest window
Plan:     the agent's plan in three lines, and the one thing I changed in it
Diff:     the files it changed, from git diff --stat
Kept:     the new SQL in sql/gold/fuel_share.sql and its test
Rejected: a new package for dates; I kept the standard library
Tested:   uv run pytest -q, 23 passed; the DAG run twice, row counts the same
```

Four rules have no exceptions:

- No coding agent before week 29.
- The agent never reads a key or `.env` file, never runs `terraform apply` or `terraform destroy`, and never deletes data. You do those yourself.
- No AI for Explain-it answers, gate answers or your defence answers.
- You must be able to explain every line of your product. Gate 8 and the final defence may ask about any line.

## Where your files go

Inside `capstone/`, copied forward from task to task:

- `PLAN.md`, `PLAN-REVIEW.md`, `contracts/<table>.yaml` and `docs/decisions/0001-<short-name>.md` onwards, from CP1;
- your product's code, SQL, tests, Terraform files and orchestration files, in the folders your plan names;
- `AGENT_LOG.md`, from week 29;
- `README.md` and `docs/architecture.md`, finished in week 30.

In each task folder, outside `capstone/`:

- `evidence.md`: pasted command output, one `##` heading per item;
- `AI_LOG.md`, when you used chat AI in that task;
- the files a task names, such as `EXPLAIN.md`, `concept-check.md`, `demo.md` or `DEFENCE.md`.

Never commit data, a key, a token, a `.env` file or a Terraform state file.

## What "done" means

Your capstone is done when:

1. every one of your own tasks has passed its review;
2. your product answers your question from a run that started from an empty cloud account, recorded in `evidence.md`;
3. a second run of your ingestion leaves the row counts the same, and a data test stops a bad file;
4. your cloud resources are torn down, with the empty listing and the cost so far pasted as proof;
5. `capstone/README.md`, `capstone/docs/architecture.md` and a demo video of at most 3 minutes let a stranger follow your product;
6. every coding-agent change is in `capstone/AGENT_LOG.md`;
7. you have passed Gate 8 and the final defence, Gate 9, by explaining your own product without AI.

## Help

- Each task's "Stuck?" lines, and AxTutor.
- Your mentor, at the Friday demo or in office hours. Raise a task that runs over its hours early, not on the last day.
