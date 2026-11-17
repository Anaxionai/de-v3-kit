# BigQuery public tables for GitPulse part 2 (P12)

In P12 you ask GitPulse's questions again, this time on BigQuery: the same GitHub events you loaded into Snowflake in P9, from GH Archive's public tables in BigQuery.
You download nothing. The tables live in Google's projects; Google pays for their storage, and you pay only for the bytes your queries read: "You pay only for the queries that you perform on the data" (BigQuery docs).
In the BigQuery sandbox, those bytes come out of a free allowance. This page lists the tables, what is known about their sizes, the answer each planned query should give, and the scan budget that keeps you inside the allowance.

> **How sure are these numbers?** The kit builders had no Google Cloud account, so **no size on this page comes from BigQuery**. Each number is marked:
> - **counted**: counted from GH Archive's hourly files (the same events as the BigQuery tables), on 13 November 2026;
> - **checked**: from Google's or GH Archive's documentation, fetched on 13 November 2026;
> - **estimate**: worked out from the files with Google's data-type sizes, **not confirmed with a dry run**;
> - **not measured**.
>
> The free commands in "Measure it yourself" give the true values. Mentors: after the first cohort's task 7, replace the estimates with real dry runs and real `bq show` output.

Sizes are decimal, like the 2 GB limit: 1 MB is 1,000,000 bytes and 1 GB is 1,000,000,000 bytes. BigQuery's billing minimum is the exception: 10 MB there means 10,485,760 bytes.

## The tables

| Table | Used in | What it holds |
|---|---|---|
| `githubarchive.day.YYYYMMDD` | tasks 7 to 11 | one table per UTC day of GitHub's public events, for example `githubarchive.day.20180101`. The course reads 2018-01-01 to 2018-01-08 |
| `githubarchive.day.201801*` | card 3; tasks 7, 9 and 11 | a **wildcard table** over every January 2018 day table. Pick days with `_TABLE_SUFFIX`, for example `WHERE _TABLE_SUFFIX BETWEEN '01' AND '07'` |
| `bigquery-public-data.samples.shakespeare` | cards 2, 3 and 5 | "a word index of the works of Shakespeare, giving the number of times each word appears in each corpus" (BigQuery docs, **checked**) |

GH Archive's page (**checked**) says the BigQuery dataset is "automatically updated every hour", names the year, month and day datasets (for example `day.20150101`), and recommends `_TABLE_SUFFIX` wildcards to pick days.

**Location.** "The BigQuery sample tables are stored in the `US` multi-region" (BigQuery docs, **checked**). The `githubarchive` datasets are expected in `US` too (**not measured**: GH Archive does not say). Make your own dataset in `US` (`bq --location=US mk --dataset gitpulse`), because a query cannot read tables from two locations.

**Shakespeare's sample** has the columns `word` (STRING), `word_count` (INT64), `corpus` (STRING, the play or poem) and `corpus_date` (INT64, the year it was written). Its row count and size are **not measured**; it is small, a few MB, so any query on it is billed the 10 MB minimum. `bq show bigquery-public-data:samples.shakespeare` gives the real numbers.

## GH Archive's columns

The day tables follow GH Archive's schema file, `bigquery/schema.js` in the `igrigorik/gharchive.org` repository (**checked**):

| Column | Type | Note |
|---|---|---|
| `type` | STRING | the event type, such as `PushEvent`. A star is a `WatchEvent` |
| `public` | BOOLEAN | |
| `payload` | STRING | the event's details as **a JSON string**. Read it with `JSON_VALUE` (one value, returned as text) and `JSON_QUERY_ARRAY` (a list). It holds most of each table's bytes |
| `repo` | RECORD | `repo.id`, `repo.name` (`owner/repository`), `repo.url` |
| `actor` | RECORD | `actor.id`, `actor.login`, `actor.gravatar_id`, `actor.avatar_url`, `actor.url` |
| `org` | RECORD | the organisation, when there is one |
| `created_at` | TIMESTAMP | when the event happened, UTC |
| `id` | STRING | the event id |
| `other` | STRING | |

BigQuery bills by column: it reads only the columns you name, whole, for every row of every table in the query. A `WHERE` filter does not reduce the bytes of a day table, and neither does `LIMIT`. Google's data-type sizes (**checked**, BigQuery data types page): STRING is 2 bytes plus the length of the text in UTF-8; INT64 and TIMESTAMP are 8 bytes; BOOL is 1 byte; NULL is 0 bytes.

## The day tables: rows and bytes

Rows are **counted** from the 48 hourly files of the two days. Bytes are **estimates**: Google's type sizes applied to every row, with `payload` as compact JSON.

| Day table | Rows | Whole table | `payload` | `type` | `id` | `created_at` | `repo.name` | `actor.login` |
|---|---|---|---|---|---|---|---|---|
| `githubarchive.day.20180101` | 687,304 | ~1.41 GB | ~1,196.6 MB (85%) | 8.5 MB | 8.2 MB | 5.5 MB | 17.8 MB | 8.1 MB |
| `githubarchive.day.20180102` | 1,199,910 | ~3.03 GB | ~2,657.2 MB (88%) | 15.4 MB | 14.4 MB | 9.6 MB | 30.6 MB | 14.0 MB |

**The fact that shapes the week:** the `payload` of 2018-01-01 (about 1.2 GB) fits under the 2 GB limit, and the `payload` of 2018-01-02 (about 2.66 GB, 33% over) does not. So every question that reads `payload` uses 2018-01-01 only. The first mentor with an account should confirm both with dry runs (below), because task 7's planning step depends on them.

Days 3 to 8 January 2018 were not downloaded. Their hourly files total 497.8, 515.9, 501.5, 307.2, 306.1 and 534.0 MB gzipped (**counted** from the file sizes). Their table sizes are **not measured**; going by the first two days, each is roughly 2 to 3.5 GB, almost all of it `payload`.

`gitpulse.events` (task 9) keeps no `payload`: seven days of `id`, `type`, `created_at`, `repo.id`, `repo.name` and `actor.id` come to about 7.6 million rows and about 0.63 GB (**estimate**), well inside the sandbox's 10 GiB.

## The scan budget

| Limit | Value | Where it comes from |
|---|---|---|
| Largest single query | **2 GB** (2,000,000,000 bytes) | `--maximum_bytes_billed=2000000000` in `~/.bigqueryrc` (task 7). A query that would bill more fails and costs nothing |
| Task 8's five final queries together | **10 GB** (10,000,000,000 bytes) | the course's scan ledger, `gitpulse/bigquery/docs/budget.md` |
| Free query processing | **1 TiB a month** | BigQuery pricing page (**checked**); the same in the sandbox |
| Price after the free TiB | USD 6.25 per TiB, on demand | BigQuery pricing page (**checked**); task 12 turns it into rupees |
| Smallest bill | **10 MB per table** a query reads, and per query, rounded up to the MB | BigQuery pricing page (**checked**). A small query shows `10485760` bytes billed |
| Sandbox storage | **10 GiB for the life of the project**; deleting a table does not give it back | the sandbox page (**checked**, see `cloud/gcp/README.md`). Build each table once |

Your `~/.bigqueryrc` has exactly three lines:

```text
[query]
--use_legacy_sql=false
--maximum_bytes_billed=2000000000
```

The limit test in task 7, ``bq query 'SELECT payload FROM `githubarchive.day.201801*`'``, reads the `payload` of all 31 days, about 70 GB (**estimate**), so it must fail with `Query exceeded limit for bytes billed: 2000000000.`

### Sandbox rules that change the SQL

`cloud/gcp/README.md` has the full list. The three that shape P12's files:

- **Tables, views and partitions expire after 60 days.** A date partition from 2018 expires at once, so task 9 partitions by a day number, `event_day` (an INT64 such as 20180103), with `RANGE_BUCKET`. Integer-range partitions never expire.
- **No DML, no streaming and no Data Transfer Service.** Task 11's scheduled query and its late day need billing, so task 11 starts the Free Trial.
- **10 GiB of storage for life.** `gitpulse.events` (about 0.63 GB) and `gitpulse.pushes` (about 43 MB) fit many times over; a table built twice still counts twice.

## Every planned query: dry-run estimate and expected answer

All bytes are **estimates** from the files. The expected answers are **counted** from the files; the BigQuery tables should give the same numbers, because they hold the same events. Mentors: use them to spot a wrong number.

| File (task) | Columns read | Estimate | Expected answer |
|---|---|---|---|
| `q01_events_per_type.sql` (7) | `type` (and `id` if it counts ids), day 1 | ~8.5 MB with `type` only (billed 10 MB); ~16.8 MB with `id` | 687,304 events in 14 types; see the table below |
| `q02_top_starred.sql` (7) | `type`, `repo.name`, day 1 | ~26.3 MB | wangshub/wechat_jump_game 1,075; facebookresearch/wav2letter 550; ossu/computer-science 260; vergecurrency/VERGE 207; huyingjie/Checklist-Checklist 185; faceair/youjumpijump 183; picturepan2/instagram.css 180; tipsy/github-profile-summary 166; transloadit/uppy 152; rameshvarun/NeuralKart 143 |
| `q03_top_merged.sql` (7) | `type`, `repo.name`, `actor.login`, `payload`, day 1 | **~1.23 GB**, the largest | LanguageResources/Homework 80; faisalnoufal/skiddy 25; yenkins/test-zuul 24; robkelley15/indivisiblemn03.github.io 20; NixOS/nixpkgs 18; 0 merged by bots in each. The day has 10,409 merged and 15,308 opened pull requests |
| `q04_daily_totals.sql` (7) | `type`, `created_at`, days 1 and 2 | ~39.0 MB | 2018-01-01: 687,304 events, 391,963 pushes, 61,746 stars. 2018-01-02 before 06:00 UTC: 225,212 events, 118,003 pushes, 31,528 stars |
| q04 with commits (7, dry run only) | adds `payload` of days 1 and 2 | ~3.9 GB: **over the limit** | the planning moment of task 7 |
| `q05_events_per_hour.sql` (7) | `created_at`, day 1 | ~5.5 MB (billed 10 MB) | the 24 hourly counts below |
| **The five together** (8) | | **~1.32 GB** | well under 10 GB; a few reruns of q03 still fit |
| Limit test (7) | `payload`, 31 days | ~70 GB | fails at 2 GB, costs nothing |
| `build_events.sql` (9) | `id`, `type`, `created_at`, `repo.id`, `repo.name`, `actor.id`, days 1 to 7 | ~565 MB; table ~0.63 GB, ~7.6 million rows | under the limit |
| `q06_stars_public.sql` (9) | `type`, `repo.name`, day 3 | ~51 MB | the top 10 starred of 2018-01-03 (**not measured**: day 3 was not downloaded). The three q06 files must agree with each other |
| `q06_stars_date.sql` (9) | your table, filter on `DATE(created_at)` only | ~350 MB estimate: all seven days | the same top 10. Real bytes are lower than the estimate because of clustering on `event_type` |
| `q06_stars_pruned.sql` (9) | your table, filter on `event_day = 20180103` | ~62 MB estimate: one partition | the same top 10. Real bytes are much lower again (clustering); 10,485,760 billed is the saving working |
| `build_pushes.sql` (10) | `id`, `type`, `created_at`, `repo.name`, `payload`, day 1 | ~1.24 GB; table ~43 MB | 391,963 rows, one per push |
| `q07_commit_check.sql` (10) | the nested table | ~26 MB | 391,963 pushes; `SUM(commit_count)` 984,390; 513,744 commits listed; 3,059 pushes where the two differ (pushes of more than 20 commits); 44,292 pushes with an empty list, all with size 0 |
| `q07_commit_check_public.sql` (10, dry run only) | `type`, `payload`, day 1 | ~1.2 GB | the cost of reading `payload` every time |
| `q08_top_committers.sql` (10) | the nested table | ~33 MB | shenzhouzd/update 4,671; johgibso/lork 2,572; and so on. 445,038 distinct commits are listed in all |
| `append_20180108.sql` (11) | the build's columns, day 8 | ~107 MB | the late day; `daily_mv` shows 20180108 at once, `daily_summary` only after its next run |
| **The whole week** | | **~5 GB** | with one AI rerun of q03: far inside the free 1 TiB |

Remember when you compare with P9: **BigQuery's 2018-01-02 table holds all 24 hours**, while P9 loaded hours 0 to 5 only. Over the whole day, 2018-01-02 has 1,199,910 events, of which 617,431 are `PushEvent`, 118,863 `WatchEvent` and 60,950 `PullRequestEvent` (**counted**).

### q01: events per type on 2018-01-01 (counted)

| Type | Events | Share |
|---|---|---|
| `PushEvent` | 391,963 | 57.0% |
| `CreateEvent` | 91,647 | 13.3% |
| `WatchEvent` | 61,746 | 9.0% |
| `IssueCommentEvent` | 36,087 | 5.3% |
| `PullRequestEvent` | 28,836 | 4.2% |
| `IssuesEvent` | 22,329 | 3.2% |
| `ForkEvent` | 20,429 | 3.0% |
| `DeleteEvent` | 18,041 | 2.6% |
| `PullRequestReviewCommentEvent` | 5,465 | 0.8% |
| `GollumEvent` | 4,484 | 0.7% |
| `ReleaseEvent` | 2,410 | 0.4% |
| `MemberEvent` | 1,741 | 0.3% |
| `CommitCommentEvent` | 1,250 | 0.2% |
| `PublicEvent` | 876 | 0.1% |
| **Total** | **687,304** | 687,304 distinct ids |

### q05: events per UTC hour of 2018-01-01 (counted)

Hours 0 to 23: 20,541; 21,443; 21,131; 22,993; 19,906; 20,095; 22,197; 24,400; 24,047; 24,470; 25,185; 27,423; 30,262; 33,509; 35,294; 36,577; 36,274; 35,927; 34,504; 35,420; 34,644; 36,467; 33,544; 31,051.
The quietest hour is 4 (19,906, down 3,087 on hour 3) and the busiest is 15 (36,577). `data/gharchive/README.md` gives the same counts per hourly file.

## Measure it yourself (free)

These read only a table's description, not its data, so they should scan no bytes (**not measured**: a metadata call, expected to be free):

```bash
bq show githubarchive:day.20180101
bq show --format=prettyjson githubarchive:day.20180101
bq show --schema --format=prettyjson githubarchive:day.20180101
```

`bq show` names a table with a colon (`githubarchive:day.20180101`); SQL uses a dot and backticks (`` `githubarchive.day.20180101` ``). In the plain output, **Total Rows** is the row count and **Total Bytes** the table's logical size. In the JSON output, `numRows`, `numBytes` and `location` give the same and the region.

A dry run estimates a query without running it, and costs nothing:

```bash
bq query --dry_run < gitpulse/bigquery/sql/q01_events_per_type.sql
```

To confirm the per-column table above, dry-run one column at a time, on both days:

```bash
for col in payload type id created_at repo.name actor.login; do
  for day in 20180101 20180102; do
    echo "$col $day"
    bq query --dry_run "SELECT $col FROM \`githubarchive.day.$day\`"
  done
done
```

The day-2 `payload` line is the one that matters: it must be over 2,000,000,000 bytes, and day 1's under it.

## Personal data

GH Archive's events name real people: `actor.login` on every event, and commit author names and email domains inside `payload`. GitPulse part 2 reads `actor.login` only to count bot merges in q03, and publishes only counts and repository names. `gitpulse.events` keeps `actor_id` but no login, and `gitpulse.pushes` keeps each commit's `sha` and `distinct` flag only: **no author name or email in any table or file**, as in P9. Some repository names in the answers above are personal names; never publish lists of logins.

## Credit and licence

- **GH Archive states no licence and no terms of use.** `data/gharchive/README.md` explains what that means for the course and what GitHub's own policies say. The course stores none of the data.
- End `findings.md` and your README with this line: **"Data: GH Archive (https://www.gharchive.org), a record of GitHub's public events."**
- The Shakespeare table is one of Google's BigQuery samples, used only in the learn cards.

## Links

- GH Archive (GH Archive): https://www.gharchive.org/
- GH Archive's BigQuery schema (GitHub): https://github.com/igrigorik/gharchive.org/blob/master/bigquery/schema.js
- BigQuery public datasets (Google Cloud docs): https://docs.cloud.google.com/bigquery/public-data
- Query multiple tables using a wildcard table (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables
- Data types, with the size of each (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types
- BigQuery pricing (Google Cloud): https://cloud.google.com/bigquery/pricing
- Estimate and control costs (Google Cloud docs): https://docs.cloud.google.com/bigquery/docs/best-practices-costs
