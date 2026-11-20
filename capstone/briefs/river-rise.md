# River Rise: which rivers rise fastest after heavy rain?

One of the four capstone briefs. Read the [capstone README](../README.md) first. It explains the four weeks, the seven required parts and the AI rules.

## The users and their question

When heavy rain is forecast, a local council puts temporary flood barriers where rivers rise fastest. It has 6 barrier sets and about 30 places it could send them. Today the choice rests on memory. River Rise gives the council numbers from the river gauges themselves.

- **User:** a flood-response planner at the council. When heavy rain is forecast, they decide by 16:00 where tomorrow's barriers go. They need yesterday's readings, ready by 07:00.
- **Second user (optional):** the council's resilience manager, who reviews each quarter which stations came closest to flooding.

**The question:** for the river stations in one catchment (the area that drains into one river), how many hours after the heaviest rain at the nearest rain gauge does each station's level peak, and which stations came closest to their typical high level in the last 90 days?

Example answers, as the planner reads them:

- "Bourton Dickler peaks a median of 7 hours after heavy rain at the nearest gauge."
- "In the last 90 days, 4 of 36 stations went above their typical high level; the highest went 0.21 m over."

(The numbers above are made up, except the station name. Your report shows the real ones.)

## The data source

**The Environment Agency's real-time flood-monitoring API** for England. It publishes river levels, flows and rainfall every 15 minutes.

| Item | What we found (checked on 13 November 2026) |
|---|---|
| Address | `https://environment.data.gov.uk/flood-monitoring/` |
| Documentation | `https://environment.data.gov.uk/flood-monitoring/doc/reference` |
| Licence | Open Government Licence v3.0, named in every response (`meta.licence`). The documentation asks for this credit: "this uses Environment Agency flood and river level data from the real-time data API (Beta)". |
| Status | The API calls itself a "Beta service". |
| Key | None |
| Format | JSON for stations; CSV for the daily archive |

The calls you need:

| Call | What it returns | Size we measured |
|---|---|---|
| `GET id/stations` | Every station: `label`, `riverName`, `catchmentName`, `lat`, `long`, `easting`, `northing`, `dateOpened`, `status` and its measures | 5,541 stations in 112 catchments; 4.7 MB |
| `GET id/stations/{id}` | One station, with `stageScale.typicalRangeHigh` and `typicalRangeLow`: the normal range of its level | about 3 KB |
| `GET id/stations?parameter=rainfall` | The rain gauges. Most have no `catchmentName`, so you match a gauge to a river station by distance, from `easting` and `northing` (metres). | 1,044 gauges |
| `GET archive/readings-YYYY-MM-DD.csv` | Every reading of one day, columns `dateTime,measure,value` | 62,498,847 bytes for 11 November 2026 |

**The daily archive.** Files exist from 31 October 2025 (30 October 2025 returned 404) to yesterday. One day holds about 505,000 rows: we counted 124 bytes a row in the first 2 MB. In those rows, 75% were river levels, 19% rainfall and 6% flow. Each measure has 96 readings a day, one every 15 minutes. The server sends the file uncompressed, but it compresses about 13 times with gzip, to about 4.6 MB a day.

**The readings API** (`id/stations/{id}/readings?startdate=...&enddate=...`) returns at most 10,000 items a call, and only 500 with `_sorted` and no `_limit`. The documentation asks for one call every 15 minutes, not one call per station. Use the archive files for history.

**Size:** a whole year of archive files is about 23 GB of CSV and 185 million rows. Your catchment is a small part of it. One catchment is small. Cotswolds has 36 stations with 70 measures (65 levels, 4 flows, 1 rainfall): 70 x 96 = 6,720 rows a day, or about 600,000 rows in 90 days. Add the measures of the rain gauges you match to it.

**What changes after publication:** stations open, close and change their typical range, so the station dimension keeps its history (a type 2 slowly changing dimension, P3). Readings arrive late or are missing for a few measures. **The hard part:** the volume. You read a 62 MB file a day, keep only your catchment's measures, partition by date, and check completeness: 96 readings per measure per day.

## What you must build

| Required part | River Rise |
|---|---|
| A question and a named user | The question above, and the planner who decides by 16:00 |
| Ingestion that is safe to re-run | A loader that downloads one day's archive file, stores it gzipped and unchanged in the raw layer under `date=YYYY-MM-DD`, and replaces that one date partition on a re-run (P5). The stations list is loaded daily. A backfill loads 90 days. |
| A warehouse or lakehouse with a documented model | Lakehouse layers as partitioned Parquet or Iceberg: `fact_reading` (one row per measure per 15 minutes), `dim_station` (type 2, with `typicalRangeHigh`), `dim_measure` and `dim_date`; a gold table of rain-to-peak hours per station |
| Orchestration with retries and a backfill | Airflow (P6) or Step Functions (P11): a daily run at 05:00 for yesterday's file, retries for the download, an alert, and a backfill by date |
| Data tests that block bad data, and a data contract | Blocking: one row per measure per 15 minutes, a known measure, a date inside the file's day. Warning: fewer than 96 readings for a measure, and a level far outside the station's range. A contract for `fact_reading`. |
| One real cloud, built with Terraform, with a cost note and a teardown | Raw and clean layers on S3, queried with Athena as Iceberg tables, built with Terraform on the AWS free plan (P11), with a cost note and `terraform destroy` |
| Something a person can open | A Markdown report after each run: the hours from rain to peak per station, and the stations nearest their typical high level. Power BI (P14) is a Stretch route. |

**The cloud route.** The AWS free plan you opened in week 21 is still open in weeks 28 to 30, and every AWS part above was taught in P11. Databricks Free Edition (P7) is the other natural route, with Delta tables and Spark. Its compute reaches only a limited list of websites, so your laptop downloads the files and uploads them, and Terraform for Databricks is an idea the course has not taught. BigQuery inside its free allowance is possible too, with Terraform for Google Cloud as the untaught idea.

## Out of scope

- All of England: one catchment only. More catchments are a Stretch idea.
- Flood warnings, alerts to the public and any forecast of future levels.
- Tidal and groundwater stations.
- Maps. A table of stations with their river names is enough.
- Readings older than the archive: it starts on 31 October 2025.

## On an 8 GB laptop

Never load a whole day into pandas. Read each file with DuckDB (MAP weeks, P5) and keep only your catchment's measures as you read: `SELECT ... FROM read_csv('readings-2026-11-11.csv') WHERE measure IN (SELECT measure FROM catchment_measures)`. One day then takes seconds and little memory. Process one day at a time, run Airflow with its `lite` profile, and start nothing else. A 90-day backfill downloads about 5.6 GB, so run it overnight or in 3 parts. Spark is not needed at this size; if your plan uses it, use the Spark `lite` profile or Databricks Free Edition.

## Cost

**₹0 on the AWS free plan.** Its credits cover this product many times over.

At normal prices, a month costs well under $1:

| Service | Size | Price (Mumbai, `ap-south-1`) | A month |
|---|---|---|---|
| S3 storage | 0.6 GB (90 days of gzipped raw files plus the clean catchment tables) | $0.025 per GB a month | $0.015 |
| S3 requests | 30 uploads and 3,000 reads a month | $0.005 per 1,000 uploads, $0.0004 per 1,000 reads | $0.002 |
| Athena | 1 run a day plus re-runs, 10 queries a run, 50 MB each: 30 GB a month | $5 per TB scanned | $0.15 |
| **Total** | | | **about $0.17 (₹16)** |

Prices: the AWS price list for `ap-south-1`, read on 13 November 2026. Rupees at ₹94.04 to the dollar (European Central Bank reference rate, 12 November 2026). Work out your own numbers in CP1 task 14, and set the budget alarm first. The trap here is scanning raw CSV with Athena: always query the partitioned clean tables.

## Stretch ideas

1. Add a second catchment, and show that the run time grows with the number of measures, not with the size of the file.
2. Add the flow measures, and report how many hours after rain each station's flow peaks compared with its level.
3. Build the report as a Power BI page with one chart per station (P14), and keep the Markdown report as the text version.

## What the demo must show

In about 10 minutes:

1. The question, and the planner who uses the answer.
2. One daily run from the orchestrator: the file's size, the rows kept for your catchment, and the rows in each layer.
3. The same day run again, with the same row counts: the date partition is replaced, not added to.
4. The completeness test on a day with missing readings: what it found and what the run did.
5. The report: rain-to-peak hours for 3 stations, and the stations nearest their typical high level.
6. The cost so far, and the teardown command.

## Data and privacy

The data has no personal data. Show the credit line from the documentation in your report and README, with "Contains public sector information licensed under the Open Government Licence v3.0." Download each archive file once and keep it: never fetch the same day twice in a backfill.
