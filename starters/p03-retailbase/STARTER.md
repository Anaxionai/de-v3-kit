# RetailBase Guided starter (P3)

This folder is the start of your `retailbase/` product folder. It saves you the set-up
work: the folders, one SQL file for each statement or question the tasks grade, each with
its heading, and the headings of your two documents. It holds no solutions: no column
types, no keys, no load and no query.

## What is included

| Path | What it is |
|---|---|
| `.python-version`, `.gitignore` | Python 3.12 for uv, and `data/` kept out of Git. |
| `profile_raw.py` | The profile script for task 7, with `main()` to write. |
| `sql/01_staging.sql` | The `staging` schema, and the ten column names of `staging.sales_raw`. |
| `sql/02_dimensions.sql`, `sql/03_fact_sales.sql`, `sql/04_scd2_customer.sql` | Section headings for tasks 9, 10 and 11. |
| `sql/queries/` | One file per question, each with its question as a comment. |
| `docs/profile.md` | The table header for your findings. |
| `docs/model.md` | The five headings, and two empty Mermaid diagrams. |
| `docs/screenshots/` | An empty folder for the wrap-up's screenshots. |

There is no `pyproject.toml`: task 7, step 1 makes one with `uv init`, which stops if the
file already exists. No data is included: task 7, step 2 downloads it into `data/`.

## How to copy it in

In task 7, step 1, run these in Git Bash inside the task 7 folder, instead of creating
`retailbase/` yourself. Then run the rest of step 1 inside it, as the brief says:

```bash
cp -r ~/de-kit/starters/p03-retailbase retailbase
cd retailbase
uv init --bare --python 3.12
uv add pandas
```

Then carry on with step 2. From task 8 on, copy your `retailbase/` folder forward as each
brief says (without `.venv/`).

## How to run it

With the data lab's `core` profile running, every `.sql` file runs as shipped. Each one
holds only comments until you write it, except `01_staging.sql`, which creates the
`staging` schema, and `04_scd2_customer.sql`, which runs an empty transaction. From
`retailbase/`:

```bash
docker exec -i datalab-postgres-1 psql -U de -d retailbase < sql/01_staging.sql
uv run python profile_raw.py      # TODO(task 7) until you write main()
```

## Every TODO

| Task | File | What you write |
|---|---|---|
| 7 | `profile_raw.py` | `main()`: the shape, the missing values and each sheet's dates |
| 7 | `sql/01_staging.sql` | `staging.sales_raw` with its ten typed columns |
| 7 | `sql/queries/p1_overlap.sql` to `p5_grain.sql` | The five profile queries |
| 7 | `docs/profile.md` | Each finding, its number and what the model must do |
| 8 | `docs/model.md` | Both diagrams, the grain, the measures and the decisions |
| 9 | `sql/02_dimensions.sql` | The three dimensions, their loads and the unknown members |
| 9 | `sql/queries/check_dimensions.sql` | The five checks |
| 10 | `sql/03_fact_sales.sql` | `dw.fact_sales` and its load |
| 10 | `sql/queries/reconcile.sql` | The three reconcile queries |
| 11 | `sql/04_scd2_customer.sql` | The new columns, the batch table, the view `staging.latest_changes`, the `UPDATE` and the `INSERT` |
| 11 | `sql/03_fact_sales.sql` | The customer lookup by date |
| 11 | `sql/queries/classify_changes.sql`, `one_customer.sql` | The two queries |
| 12 | `sql/queries/sales_by_country_at_sale.sql`, `_today.sql`, `_compare.sql` | The three queries |

Run `grep -rn "TODO(task" .` to see what is left. Task 12 also adds `## Two answers` to
`docs/model.md`. Task 13 (the wrap-up) has no TODO: it is your README, your demo and your
answers. Save its screenshots in `docs/screenshots/`.

## What you still write yourself

- Every column type and key, every load, every query and every rule you choose (one
  description per product, one country per customer).
- Both Mermaid diagrams, the grain statement and your reasons.
- In the task folder: `evidence.md`, `AI_LOG.md` and `EXPLAIN.md`.
- `retailbase/README.md`, in task 13.
