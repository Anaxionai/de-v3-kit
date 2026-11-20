# City Fix: how fast does a city close residents' requests?

One of the four capstone briefs. Read the [capstone README](../README.md) first. It explains the four weeks, the seven required parts and the AI rules.

## The users and their question

Residents of a large city report problems by phone, app or website: a broken street light, a pothole, a missing street sign. Each report is a service request. A city agency must close it, and the city publishes every request with the time it was created and the time it was closed.

City Fix follows one agency: the city's Department of Transportation (DOT), which handles streets, signs, lights and traffic signals.

- **User:** an operations analyst at the agency. On the first working day of each month they prepare a performance report for the five borough managers. They need last month's data complete by 08:00 on that day.
- **Second user (optional):** a borough manager, who reads the report and decides where to send crews next month.

**The question:** for the transport agency's service requests, which complaint types take longest to close in each of the five boroughs, and is the median time to close getting shorter month by month over the last 12 months?

Example answers, as the analyst reads them:

- "In Queens, 'Street Light Condition' requests took a median of 9.5 days to close in October, down from 12.1 days in September."
- "Across the city, 81% of October's requests were closed within 30 days."

(The numbers above are made up. Your report shows the real ones.)

## The data source

**311 Service Requests from 2020 to Present**, NYC Open Data, dataset id `erm2-nwe9`.

| Item | What we found (checked on 13 November 2026) |
|---|---|
| Dataset page | `https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9` |
| API address | `https://data.cityofnewyork.us/resource/erm2-nwe9.json` (the Socrata SODA API) |
| API documentation | `https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9` |
| Licence | The dataset names no licence. The NYC Open Data FAQ (`https://www.nyc.gov/opendata/get-started/FAQs`) says: "There are no restrictions on the use of Open Data." Credit "NYC Open Data, 311 Service Requests". |
| Key | Not required. An app token is strongly advised (see Limits). |
| Format | JSON (CSV is also offered) |
| Rows | 23,115,363 in all, created from 1 January 2020 to 11 November 2026. The transport agency (`agency = 'DOT'`) has 286,126 requests created from 1 November 2025 to 31 October 2026. |
| Columns | 44 data columns and 4 computed region columns, including `unique_key`, `created_date`, `closed_date`, `agency`, `complaint_type`, `descriptor`, `status`, `borough`, `incident_zip`, `community_board`, `resolution_action_updated_date`, the incident address and its latitude and longitude |
| Updated | Daily. The last update was 12 November 2026 at 02:36 UTC. |

The API uses query parameters: `$select` (the columns), `$where` (a filter), `$order` (the sort), `$limit` (the page size) and `$offset` (where the page starts). The system field `:updated_at` can be selected, filtered and sorted on. For example, this returns 3 rows of the newest changes:

```
https://data.cityofnewyork.us/resource/erm2-nwe9.json?$select=unique_key,status,:updated_at&$order=:updated_at DESC&$limit=3
```

**Size:** 1,000 rows with 12 chosen columns came to 386,714 bytes of JSON, about 390 bytes a row. A year of the transport agency's requests is about 286,000 x 390 bytes = 112 MB of raw JSON. About 790 requests a day on average.

**What changes after publication:** a request moves from Open to Assigned, In Progress or Pending, and then to Closed. `closed_date` and the resolution are filled in later. In the update of 11 to 12 November 2026, 21,091 of the agency's rows changed. **The hard part:** an incremental load by `:updated_at`, with paging, and an upsert by `unique_key` into a fact table with one row per request that is updated as the request moves on (an accumulating snapshot).

**Faults to plan for.** These are real, in the published data:

- 45,353 of the agency's requests have a `closed_date` before their `created_date`.
- `borough` holds `Unspecified` as well as the five borough names (144 of 22,072 requests in October 2026).
- The API is slow. Our count queries took 7 to 56 seconds, and one page of 1,000 rows took 4.7 seconds.

**Limits:** without an app token, all requests from one internet address share one pool, and the documentation says such addresses "may be subject to throttling". A classroom shares one address. With an app token, requests are not throttled unless they are abusive. Get a token by registering on the NYC Open Data portal. Keep it in `.env` and send it in the `X-App-Token` header. Never commit it.

## What you must build

| Required part | City Fix |
|---|---|
| A question and a named user | The question above, and the analyst who reports on the first working day of each month |
| Ingestion that is safe to re-run | A loader that pages through `$where=agency='DOT' AND :updated_at > '<watermark>'`, ordered by `:updated_at` and `unique_key`, saves each page unchanged as raw JSON, and moves the watermark only after a page is stored. A backfill loads 12 months, one month at a time, by `created_date`. |
| A warehouse or lakehouse with a documented model | A star: `fact_request` (one row per request: created, closed, hours to close, status), with `dim_complaint_type`, `dim_location` (borough, ZIP, community board) and `dim_date` |
| Orchestration with retries and a backfill | Airflow (P6) or Step Functions (P11): a daily run at 06:00, retries with backoff for the slow API, an alert, and a backfill by month |
| Data tests that block bad data, and a data contract | Blocking: `unique_key` unique, `created_date` present, borough in the allowed list. Warning: `closed_date` before `created_date` (count and keep apart, do not drop silently). A contract for `fact_request`. |
| One real cloud, built with Terraform, with a cost note and a teardown | Raw and clean layers on S3, partitioned by created month, queried with Athena as Iceberg tables, built with Terraform on the AWS free plan (P11), with a cost note and `terraform destroy` |
| Something a person can open | A monthly Markdown report: the five slowest complaint types per borough, the median days to close by month, and the share closed within 30 days. Power BI (P14) is a Stretch route. |

**The cloud route.** The AWS free plan you opened in week 21 is still open in weeks 28 to 30, and every AWS part above was taught in P11. Two other routes need an untaught idea each: BigQuery inside its free allowance (Terraform for Google Cloud, and the no-card sandbox has no `MERGE`), or Databricks Free Edition (Terraform for Databricks, and its compute reaches only a limited list of websites, so your laptop calls the API and uploads the files).

## Out of scope

- Agencies other than the transport agency (a Stretch idea).
- Years before 2020: they are a separate dataset, `76ig-c548`.
- Maps and street-level detail.
- Predicting how long a new request will take.
- Live updates: the source changes once a day.

## On an 8 GB laptop

Load and transform one month at a time. A month of the agency's requests is about 24,000 rows and 9 MB of JSON. Run Airflow with its `lite` profile and nothing else, and let Athena do the heavy queries. Never load the 23 million rows of the whole city.

## Cost

**₹0 on the AWS free plan.** Its credits cover this product many times over.

At normal prices, a month costs well under $1:

| Service | Size | Price (Mumbai, `ap-south-1`) | A month |
|---|---|---|---|
| S3 storage | 0.3 GB (12 months of raw JSON plus clean tables) | $0.025 per GB a month | $0.008 |
| Athena | 2 runs a day, 10 queries a run, 30 MB each: 18 GB a month | $5 per TB scanned | $0.09 |
| **Total** | | | **about $0.10 (₹9)** |

Prices: the AWS price list for `ap-south-1`, read on 13 November 2026. Rupees at ₹94.04 to the dollar (European Central Bank reference rate, 12 November 2026). Work out your own numbers in CP1 task 14, and set the budget alarm first.

## Stretch ideas

1. Add a second agency, such as the sanitation department (`DSNY`, 361,659 requests in the same 12 months), and compare the two.
2. Keep the history of each request's status in a second fact, one row per request per status change, from the daily loads.
3. Build the report as a Power BI page with a borough slicer and a monthly trend (P14), and keep the Markdown report as the text version.

## What the demo must show

In about 10 minutes:

1. The question, and the analyst who uses the answer.
2. One daily run from the orchestrator, with the row counts in each layer and the new watermark.
3. A second run straight after, with the same row counts: the load is safe to re-run.
4. The data test on `closed_date` before `created_date`: how many rows it found, and where they went.
5. The report: the slowest complaint types in two boroughs, and the trend over 12 months.
6. The cost so far, and the teardown command.

## Data and privacy

The dataset holds no caller details. Its description says: "the data does not reveal any personally identifying information about the customer who made the request." It does hold the address and the coordinates of each incident. Keep borough, ZIP code and community board, and drop the street-level columns (`incident_address`, the street names, `bbl`, `latitude`, `longitude`, `location` and the two state-plane coordinates) after the raw layer, as you did in P13. Never publish rows with addresses in your report or your sample.
