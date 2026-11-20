# Research Pulse: which journals publish more, and how fast are new papers cited?

One of the four capstone briefs. Read the [capstone README](../README.md) first. It explains the four weeks, the seven required parts and the AI rules.

## The users and their question

A university library pays for 20 research journals. Each year it must decide which subscriptions to renew. Prices rise every year, and the budget does not. The library wants numbers: how much each journal publishes, and how quickly its new papers are cited by other papers.

- **User:** the library's journal-subscriptions manager. Once a year they choose the renewals, and once a month they review the numbers with the faculty. They need data at most a week old.
- **Second user (optional):** a head of department, who reads the monthly summary for the journals in their field.

**The question:** for 20 journals the library pays for, how many new research articles does each journal publish each month, and how many citations do those articles gather in their first 12 months?

Example answers, as the manager reads them:

- "Journal A published 31 articles a month on average this year, 4 more than last year."
- "Articles in Journal B gathered a median of 6 citations in their first 12 months; Journal C's gathered 1."

(The numbers above are made up. Your report shows the real ones.)

## The data source

**The Crossref REST API.** Crossref registers DOIs (digital object identifiers, the permanent id of a paper) for most publishers, with their metadata.

| Item | What we found (checked on 13 November 2026) |
|---|---|
| Address | `https://api.crossref.org/works`, and for one journal `https://api.crossref.org/journals/{ISSN}/works` |
| Documentation | `https://www.crossref.org/documentation/retrieve-metadata/rest-api/` |
| Licence | Crossref's REST API page says: "almost none of the metadata is subject to copyright, and you may use it for any purpose." It also says: "Some abstracts contained in the metadata may be subject to copyright by publishers or authors." So you never store abstracts. Credit "Metadata from Crossref". |
| Key | None, and no sign-up |
| Format | JSON |
| Rate limits | The public pool allows 5 requests a second, 1 at a time (the response headers say `x-rate-limit-limit: 5`, `x-rate-limit-interval: 1s`, `x-concurrency-limit: 1`). Add `mailto=<your email>` to join the polite pool: 10 requests a second, 3 at a time. On HTTP 429, wait and retry more slowly. |

What a request looks like, and what we measured:

| Request | Result |
|---|---|
| `works?filter=from-index-date:2026-11-10,until-index-date:2026-11-10&rows=0` | 2,238,748 works were indexed (added or updated) on that one day, across all publishers. You must narrow by journal. |
| `journals/0028-0836/works?filter=from-pub-date:2024-11-01,until-pub-date:2025-10-31,type:journal-article&rows=0` | 4,623 articles in one year for one large journal (ISSN `0028-0836`) |
| The same journal, `filter=from-index-date:2026-11-01,until-index-date:2026-11-07,from-pub-date:2024-11-01,type:journal-article` | 960 of its recent articles were indexed again in one week, mostly because their citation counts changed |
| 400 articles with `select=DOI,title,type,issued,published,ISSN,container-title,publisher,is-referenced-by-count,indexed` | 187,124 bytes: about 470 bytes an article |

Useful parameters: `filter` (one or more, separated by commas), `select` (the fields you want), `rows` (up to 1,000 a page), and deep paging with `cursor=*`: each answer holds a `next-cursor` for the next page, until a page comes back empty.

**Size:** most journals publish far fewer articles than the large one above. For 20 journals, plan for 10,000 to 30,000 articles a year, so 5 to 15 MB of raw JSON a year. Re-indexing adds the same articles again as their citations change: plan for up to 5,000 rows a week. A warehouse handles this size.

**What changes after publication:** `is-referenced-by-count` (how many registered works cite this one) grows over time, and `indexed` changes each time Crossref updates the record. So the same DOI is loaded again and again. **The hard part:** an incremental load by index date with cursor paging, an upsert by DOI, a weekly snapshot of each article's citation count, and nested JSON: `ISSN`, `title` and `issued.date-parts` are arrays (you met nested data with `FLATTEN` in P9 and `UNNEST` in P12).

**A field you cannot use:** `subject` is in the API, but it was empty for 20 of 20 articles we checked. Group by journal, not by topic.

## What you must build

| Required part | Research Pulse |
|---|---|
| A question and a named user | The question above, and the subscriptions manager who reviews monthly and decides yearly |
| Ingestion that is safe to re-run | A loader that, for each ISSN on your list, pages through `from-index-date` and `until-index-date` for one day, with `from-pub-date` 24 months back and `type:journal-article`, and saves each page unchanged as raw JSON keyed by ISSN, date and page. A backfill loads 24 months by publication date. |
| A warehouse or lakehouse with a documented model | A star: `fact_article` (one row per DOI: journal, published date), `fact_citation_snapshot` (one row per DOI per week: the citation count), `dim_journal` (ISSN, title, publisher) and `dim_date` |
| Orchestration with retries and a backfill | Airflow (P6) or Step Functions (P11): a daily run, retries with backoff on HTTP 429 and 5xx, an alert, and a backfill by day |
| Data tests that block bad data, and a data contract | Blocking: DOI unique in `fact_article`, ISSN in the form `1234-567X` and on your list, published date not in the future. Warning: a citation count lower than last week's. A contract for `fact_article`. |
| One real cloud, built with Terraform, with a cost note and a teardown | Raw and clean layers on S3, queried with Athena as Iceberg tables, built with Terraform on the AWS free plan (P11), with a cost note and `terraform destroy`. BigQuery inside its free allowance suits the nested data too (P12), with Terraform for Google Cloud as an untaught idea. |
| Something a person can open | A monthly Markdown report per journal: articles a month, and the median citations at 12 months for articles published 12 to 24 months ago. Power BI (P14) is a Stretch route. |

**The cloud route.** The AWS free plan you opened in week 21 is still open in weeks 28 to 30, and every AWS part above was taught in P11. If you choose BigQuery, note that the no-card sandbox has no `MERGE` and deletes tables after 60 days: load each day into its own partition with a load job that replaces it. Databricks Free Edition is possible too, but its compute reaches only a limited list of websites, so your laptop calls the API.

## Out of scope

- Abstracts and full texts: never store them.
- Author names, affiliations and emails: leave `author` out of `select`, so no personal data enters the pipeline.
- Journal prices: the library has them; you do not.
- Citation sources other than Crossref, and citation counts per citing paper.
- More than 20 journals.

## On an 8 GB laptop

The data is small: tens of MB. Run Airflow with its `lite` profile and nothing else. The limit is the API, not the laptop: one request at a time in the public pool, so a 24-month backfill of 20 journals takes minutes, not hours, if you use `select` and `rows=1000`.

## Cost

**₹0 on the AWS free plan.** Its credits cover this product many times over.

At normal prices, a month costs well under $1:

| Service | Size | Price (Mumbai, `ap-south-1`) | A month |
|---|---|---|---|
| S3 storage | 0.1 GB (24 months of raw JSON plus clean tables) | $0.025 per GB a month | $0.003 |
| Athena | 2 runs a day, 10 queries a run, 10 MB each: 6 GB a month | $5 per TB scanned | $0.03 |
| **Total** | | | **about $0.03 (₹3)** |

Prices: the AWS price list for `ap-south-1`, read on 13 November 2026. Rupees at ₹94.04 to the dollar (European Central Bank reference rate, 12 November 2026). Work out your own numbers in CP1 task 14, and set the budget alarm first.

## Stretch ideas

1. Add the citation count at 6 months as well as 12, from the weekly snapshots, and show which journals are cited fastest.
2. Add `references-count` (how many works each article cites) and test whether it is linked to citations received.
3. Build the report as a Power BI page with a journal slicer and a monthly trend (P14), and keep the Markdown report as the text version.

## What the demo must show

In about 10 minutes:

1. The question, and the manager who uses the answer.
2. One daily run from the orchestrator, with the pages fetched, the rows in each layer and the cursor paging in the log.
3. The same day run again, with the same row counts: the upsert by DOI adds nothing new.
4. One data test blocking a bad record, for example an ISSN that is not on your list.
5. The report: articles a month and the median citations at 12 months for 3 journals.
6. The cost so far, and the teardown command.

## Data and privacy

With `author` and `abstract` left out of `select`, the pipeline holds no personal data and no copyrighted text. Credit "Metadata from Crossref" in your report and README. If you add `mailto=` for the polite pool, put the address in `.env`, not in your code.
