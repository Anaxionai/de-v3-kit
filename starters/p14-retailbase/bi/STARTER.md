# Guided starter: P14 RetailBase part 2 (Power BI)

This starter is an **add-on** to your own `retailbase/` folder from P3. It adds one new folder, `retailbase/bi/`, for the Power BI report, and changes nothing you built in P3. It saves you the set-up: the folder layout, the SQL check files with their headers, the `.dax` query templates with the measure names, and the documents with their headings. Every query, every DAX formula and every answer is still yours to write.

## What is included

| Path inside `retailbase/` | What it is |
|---|---|
| `bi/STARTER.md` | This file |
| `bi/.gitignore` | Keeps `*.pbix` out of Git: a `.pbix` holds a copy of all the data |
| `bi/report/` | Empty. You save `RetailBase.pbix` and `directquery-test.pbix` here (never committed) |
| `bi/sql/row_counts.sql` | Header and TODO: the row count of the four star tables |
| `bi/sql/check_<measure>.sql` | Headers and TODOs for the SQL checks of your measures, and `check_rls.sql` for the role |
| `bi/measures/base.dax`, `bi/measures/time.dax` | DAX queries with the measure names and empty formulas |
| `bi/measures/ai_check.dax`, `bi/measures/model.dax` | A header and a TODO each |
| `bi/docs/model.md`, `report.md`, `rls.md`, `ai-check.md`, `definitions.md` | The headings the briefs ask for, with a TODO under each |
| `bi/exports/` | Empty. You save `overview.csv`, `countries.csv` and `products.csv` here |

There is no `.pbix` file: you make it yourself in Power BI Desktop. `evidence.md` and `AI_LOG.md` live in the task folder, next to `retailbase/`.

## Copy it in

In task 8 (Connect Power BI Desktop to the RetailBase star), first copy your `retailbase/` folder forward from P3, as the brief says. Then, in step 1, run this in Git Bash inside the task folder, instead of creating `bi/` and its folders by hand:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p14-retailbase/bi retailbase/bi
ls -A retailbase/bi    # .gitignore  STARTER.md  docs  exports  measures  report  sql
```

Run the `cp` before you make `retailbase/bi/` yourself. If that folder already exists, `cp -r` puts the copy inside it, as `retailbase/bi/bi/`. From task 9 on, copy your `retailbase/` folder forward as each brief says. Your `.pbix` file comes with it. Copy the starter only once.

## How to run it

The SQL files run against your RetailBase warehouse in the data lab. Start PostgreSQL first, then run each file from `retailbase/`, the same place you ran your P3 SQL:

```bash
(cd ~/de-kit/datalab && docker compose --profile core up -d)
cd retailbase
docker exec -i datalab-postgres-1 psql -U de -d retailbase < bi/sql/row_counts.sql
```

A file that still holds only its TODO has no statement in it, so `psql` prints nothing. The `.dax` files run in Power BI Desktop's DAX query view: paste the file, write the formulas, then select Run. They do not run until every formula after `=` is written. On an 8 GB laptop, never run Docker and Power BI Desktop together: each brief says the order.

## Your TODOs

Find them with `grep -rn "TODO(task" retailbase/bi`.

| Task | File in `bi/` | What you write |
|---|---|---|
| 8 | `sql/row_counts.sql` | The row counts of `dw.fact_sales`, `dw.dim_date`, `dw.dim_customer`, `dw.dim_product` in one result |
| 8 | `docs/model.md` | `## Storage mode`: your choice, three reasons, the DirectQuery test |
| 9 | `docs/model.md` | `## Relationships` (Mermaid diagram) and `## Filter path` |
| 10 | `sql/check_revenue.sql`, `check_units.sql`, `check_orders.sql`, `check_customers.sql`, `check_average_order_value.sql` | One number per year for each measure |
| 10 | `measures/base.dax` | The five base measures and the query by year |
| 11 | `sql/check_revenue_ytd.sql`, `sql/check_revenue_ly.sql` | Running total by month; 2011 against 2010 |
| 11 | `measures/time.dax` | `Revenue YTD`, `Revenue LY`, `Revenue YoY %` |
| 12 | `docs/report.md` | The three pages: visuals, chart reasons, answers with numbers |
| 13 | `sql/check_rls.sql` | The revenue check for France and Germany |
| 13 | `docs/rls.md` | The role, the tests, the Unknown sales, a manager's move, a customer who moved, the limits |
| 14 | `measures/ai_check.dax` | Three DAX queries for the AI's three questions |
| 14 | `docs/ai-check.md` | The comparison table and the cause of each mismatch |
| 15 | `measures/model.dax` | Every measure, with a `///` description |
| 15 | `docs/definitions.md` | One definition per measure, the numbers on the report, the known limits |

Not in this starter, on purpose:

- `retailbase/sql/05_country_manager.sql`: you write it yourself in task 13. It is warehouse SQL, next to your P3 files `01` to `04`, and this add-on holds only new `bi/` files.
- `bi/sql/ai_q1.sql` to `ai_q3.sql`: in task 14 the AI writes those queries and you save them exactly as it wrote them.
- Task 16 (the wrap-up) has no TODO: it is your README, your demo and your answers.

## Names the briefs rely on

Keep these exactly, so that your files, the briefs and the reviews agree:

- Power BI tables: `fact_sales`, `dim_date`, `dim_customer`, `dim_product`, `country_manager`.
- Measures, all on `fact_sales`: `Revenue`, `Units`, `Orders`, `Customers`, `Average Order Value`, `Revenue YTD`, `Revenue LY`, `Revenue YoY %`.
- Role `Country manager`. Pages `Overview`, `Countries`, `Products`, `Security test`.
- The report file is `bi/report/RetailBase.pbix`. Screenshots go in `retailbase/docs/screenshots/`, the folder you made in P3.

## What you still write yourself

- Every SQL query, every DAX formula and every document's content.
- The `.pbix` file, its relationships, pages, role and descriptions.
- `retailbase/sql/05_country_manager.sql` (task 13), and the update of `retailbase/README.md` for both parts (task 16).
- `evidence.md` and `AI_LOG.md` in each task folder, and the screenshots.
- Step 12 of task 8 asks you to add `*.pbix` to `bi/.gitignore`: it is already there. Check it with `git check-ignore -v retailbase/bi/report/RetailBase.pbix` once the file exists.

## Data and licence

This starter holds no data. Your report reads your own RetailBase warehouse, built from the Online Retail II data set (UCI Machine Learning Repository, CC BY 4.0); `~/de-kit/data/retail/README.md` has the credit.
