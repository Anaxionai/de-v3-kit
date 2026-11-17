# GitPulse on BigQuery: the scan budget

The ledger of every query that counts towards the budget. The rules: no query over 2 GB (2,000,000,000 bytes), and the five final runs of q01 to q05 under 10 GB (10,000,000,000 bytes) together. Bytes are always whole numbers, as `bq` and `sql/bytes_report.sql` print them. Each table a query reads is billed at least 10 MB (10,485,760 bytes).

## Query-size limit

<!-- TODO(task 7): paste the three lines of your ~/.bigqueryrc here, inside a code block. -->

## Five questions

<!-- TODO(task 7): fill in the dry-run estimate of each file, in bytes, and the total. Every estimate must be under 2 GB, and the total under 10 GB. -->
<!-- TODO(task 8): add the real bytes billed and the cache hit of each final run, from bytes_report.sql, and the real total. In Note, explain in one line any real value far from its estimate. -->

| File | Dry-run estimate (bytes) | Real bytes billed | Cache hit | Note |
|---|---|---|---|---|
| `sql/q01_events_per_type.sql` | | | | |
| `sql/q02_top_starred.sql` | | | | |
| `sql/q03_top_merged.sql` | | | | |
| `sql/q04_daily_totals.sql` | | | | |
| `sql/q05_events_per_hour.sql` | | | | |
| **Total** | | | | |

## q04 with commits (task 7)

<!-- TODO(task 7): the dry-run estimate of q04 with the commits of each push added (JSON_VALUE(payload, '$.size')), and one sentence on why it is so much larger and what you did about it. -->

## Cheaper query (AI move)

<!-- TODO(task 8): the query you asked AI to make cheaper, with its bytes before and after (dry run, and the real run if the result stayed the same). -->

## Partition saving: the three q06 runs

<!-- TODO(task 9): the estimate and real bytes of q06_stars_public, q06_stars_date and q06_stars_pruned, and the saving of pruned against date as a percentage. In docs/partitioning.md, say which of pruned and public was cheaper and why. Add the build of gitpulse.events too. -->

## Nested table: build, q07, q08 and the public dry run

<!-- TODO(task 10): the bytes of build_pushes, q07_commit_check and q08_top_committers, the dry-run estimate of q07_commit_check_public, and after how many re-runs the nested table pays for itself. -->

## Serving: the summary, the view and the late day (task 11)

<!-- TODO(task 11): the real bytes of the summary test, the materialised view, the append of 2018-01-08 and the two reader queries after the late day. serving.md compares the reader queries with these numbers. -->

## Bytes used this week (task 12)

<!-- TODO(task 12): the bytes billed per day this week (bytes_report.sql grouped by DATE(creation_time), over the whole week, not only today) and the week's total. Paste the same under ## Teardown in evidence.md; the wrap-up README shows this total. -->
