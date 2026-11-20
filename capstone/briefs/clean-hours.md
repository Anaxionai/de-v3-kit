# Clean Hours: when is grid electricity cleanest?

One of the four capstone briefs. Read the [capstone README](../README.md) first. It explains the four weeks, the seven required parts and the AI rules.

## The users and their question

An electric-van depot charges 40 vans every night. Grid electricity is cleaner in the hours with more wind and solar, and less gas. The depot wants to charge in the cleanest hours, without missing the morning rounds.

- **User:** the depot's operations planner. Every afternoon at about 15:00 they decide when tonight's charging runs. They need tomorrow's forecast, ready by 14:30.
- **Second user (optional):** the depot manager. Once a month they check whether the forecasts were good enough to plan with.

**The question:** in each of the 14 regions of Great Britain, which 3-hour window in the next 48 hours has the lowest forecast carbon intensity, and how far was the national forecast from the actual value over the last 30 days?

Example answers, as the planner reads them:

- "South West England: the cleanest window tomorrow is 01:00 to 04:00, at 62 gCO2/kWh (very low)."
- "Last month the national forecast was within 20 gCO2/kWh of the actual value in 91% of half-hours."

Carbon intensity is grams of CO2 for each kilowatt-hour of electricity (gCO2/kWh). The source gives it as a number and as an index: very low, low, moderate, high or very high.

## The data source

**The Carbon Intensity API** from the National Energy System Operator (NESO), Great Britain's electricity system operator.

| Item | What we found (checked on 13 November 2026) |
|---|---|
| Address | `https://api.carbonintensity.org.uk/` |
| Documentation | `https://carbon-intensity.github.io/api-definitions/` |
| Licence | CC BY 4.0, in the terms of use at `https://github.com/carbon-intensity/terms`. Credit "Carbon Intensity API, National Energy System Operator". |
| What the terms forbid | Selling access to the API, replacing NESO's own apps, and heavy use: "National Energy System Operator applies a rate limit". The number is not published. |
| Key | None |
| Format | JSON |

The three calls you need:

| Call | What it returns | Size we measured |
|---|---|---|
| `GET /regional/intensity/{from}/fw48h` | The forecast for the next 48 hours, every half-hour, for 18 regions: the 14 distribution regions (`regionid` 1 to 14) and the totals for England, Scotland, Wales and GB (15 to 18). Each row has a forecast, an index and the fuel mix in percent for 9 fuels. | 659,495 bytes |
| `GET /regional/intensity/{from}/{to}` | The same for past days. Full days go back to at least 1 January 2020. A range of 14 days or more is refused with HTTP 400. | 340,687 bytes for 1 November 2026 |
| `GET /intensity/{from}/{to}` | The national forecast **and the actual value** for each half-hour. A range over 31 days is refused with HTTP 400. | 160,173 bytes for 30 days |

Two facts shape the design:

- **The regional rows have no actual value.** Only the national rows have one. So forecast error is measured nationally, not per region.
- **A one-day call returns 49 half-hours, not 48.** The first row is the half-hour that ends at `{from}`. Your load must not count it twice.

**Size:** 14 regions x 48 half-hours = 672 rows a day, or about 245,000 rows a year. The fuel mix adds 9 rows to each: about 6,000 rows a day and 2.2 million a year. The raw JSON is about 340 KB a day, so a year is about 124 MB. A warehouse handles this size; no cluster is needed.

**What changes after publication:** the forecast for a half-hour is published up to 48 hours ahead and replaced as the time comes closer. The national actual value arrives after the half-hour ends. So you load the same half-hour more than once: in two or three daily forecasts, then in the history. **The hard part:** an idempotent upsert (an insert-or-update that gives the same rows however often it runs) keyed on region and half-hour start, which keeps the latest forecast.

## What you must build

Every capstone has the seven required parts. For Clean Hours they could look like this:

| Required part | Clean Hours |
|---|---|
| A question and a named user | The question above, and the depot planner who decides at 15:00 |
| Ingestion that is safe to re-run | A loader that saves each API response unchanged as raw JSON, keyed by the run time, and an incremental load by time window. A backfill of a year runs in 7-day chunks (regional) and 30-day chunks (national). |
| A warehouse or lakehouse with a documented model | A star: `fact_intensity` (one row per region per half-hour: forecast, index), `fact_generation_mix` (one row per region per half-hour per fuel), `fact_national` (one row per half-hour: forecast and actual), with `dim_region`, `dim_date` and `dim_time` |
| Orchestration with retries and a backfill | Airflow (P6) or Step Functions (P11): a run every afternoon before 14:30, with retries, a failure alert and a backfill of missed days |
| Data tests that block bad data, and a data contract | Blocking: 48 half-hours per region per day, one row per region and half-hour, intensity not negative. Warning: fuel percentages add up to between 98 and 102. A contract for `fact_intensity`. |
| One real cloud, built with Terraform, with a cost note and a teardown | The raw and clean layers on S3, queried with Athena as Iceberg tables, all built with Terraform on the AWS free plan (P11), with a cost note and `terraform destroy` |
| Something a person can open | A Markdown report written by each run: the cleanest 3-hour window per region for tomorrow, and last month's national forecast error. Power BI (P14) is a Stretch route. |

**The cloud route.** The AWS free plan you opened in week 21 is still open in weeks 28 to 30. S3, the Glue Data Catalog and Athena are taught in P11, Iceberg with `MERGE INTO` in P11, and Terraform on AWS in P11. Two other routes are possible, each with an idea the course has not taught: BigQuery inside its free allowance (Terraform for Google Cloud is untaught, and the no-card sandbox has no `MERGE`), or Databricks Free Edition (Terraform for Databricks is untaught, and its compute reaches only a limited list of websites, so your laptop must call the API).

## Out of scope

- Control of real chargers, or any connection to a real depot.
- Live streaming: a run every afternoon meets the 14:30 freshness target.
- Your own forecast model. You report NESO's forecast and measure its error.
- Electricity prices or tariffs.
- Regions outside Great Britain.

## On an 8 GB laptop

The data is small, so the laptop is not the limit. Run Airflow with its `lite` profile (one container) and nothing else. Athena does the heavy queries in the cloud. If Docker is slow, stop Airflow while you write SQL, and start it again only to run the DAG.

## Cost

**₹0 on the AWS free plan.** Its credits cover this product many times over.

At normal prices, a month costs well under $1:

| Service | Size | Price (Mumbai, `ap-south-1`) | A month |
|---|---|---|---|
| S3 storage | 0.2 GB (a year of raw JSON plus clean tables) | $0.025 per GB a month | $0.005 |
| Athena | 4 runs a day (the daily run, re-runs and backfills), 10 queries a run, 20 MB each: 24 GB a month | $5 per TB scanned | $0.12 |
| **Total** | | | **about $0.13 (₹12)** |

Prices: the AWS price list for `ap-south-1`, read on 13 November 2026. Rupees at ₹94.04 to the dollar (European Central Bank reference rate, 12 November 2026). Work out your own numbers in CP1 task 14, and set the budget alarm first.

## Stretch ideas

1. Add the fuel mix to the report: the share of wind and solar in each cleanest window, from `fact_generation_mix`.
2. Score each region's forecast against the "index" band the next day, and report which regions change band most often.
3. Build the report as a Power BI page with a region map and a 48-hour chart (P14), and keep the Markdown report as the text version.

## What the demo must show

In about 10 minutes:

1. The question, and the planner who uses the answer.
2. One run of the pipeline from the orchestrator, with the row counts in each layer.
3. A second run for the same afternoon, with the same row counts: the load is safe to re-run.
4. One data test blocking a bad file, for example a day with 47 half-hours for one region.
5. The report: tomorrow's cleanest 3-hour window for 3 regions, and last month's forecast error.
6. The cost so far, from the AWS billing console or `aws ce get-cost-and-usage`, and the teardown command.

## Data and privacy

The data has no personal data. Credit the source in your report and README: "Carbon intensity data: Carbon Intensity API, National Energy System Operator, CC BY 4.0." Call the API at most once a minute in normal runs. A backfill waits 2 seconds between calls.
