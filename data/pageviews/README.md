# Wikipedia page views

How many people read each Wikipedia page, per day or per hour. The course uses it in three places:

- **Launchpad**: the page-views API (one address per page and date range), for your data robot (`collect.py` and `daily.yml`) and your first `curl` call.
- **PageLake (P5)**: the hourly dump files (one file per hour for all of Wikipedia), downloaded with `get_hours.py`.
- **PageLake part 2 (P6)**: the same course week, which Airflow now lands and rebuilds every day. Nothing new is downloaded; `get_hours.py --check` finds a missing hourly file.

**Licence**: page-view data is released by the Wikimedia Foundation under CC0 1.0 (no rights reserved). You need no permission, but please credit it: `Page-view data: Wikimedia Foundation (CC0 1.0).`

## Part 1: the page-views API

### The address pattern

```
https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/<Title>/daily/<YYYYMMDD>/<YYYYMMDD>
```

- `<Title>` is the part of the Wikipedia address after `/wiki/`, for example `Cricket_World_Cup` from `https://en.wikipedia.org/wiki/Cricket_World_Cup`. Underscores are safest. A title with letters outside English, such as `Beyoncé`, is URL-encoded: `Beyonc%C3%A9`.
- The two dates are the first and the last day, both included, written `YYYYMMDD` with no dashes.
- `en.wikipedia.org` is English Wikipedia; `all-access` counts desktop and mobile together; `user` leaves out known robots.

### One real answer

`https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/Chess/daily/20261001/20261003` answered (13 November 2026):

```json
{"items":[{"project":"en.wikipedia","article":"Chess","granularity":"daily","timestamp":"2026100100","access":"all-access","agent":"user","views":3644},{"project":"en.wikipedia","article":"Chess","granularity":"daily","timestamp":"2026100200","access":"all-access","agent":"user","views":3558},{"project":"en.wikipedia","article":"Chess","granularity":"daily","timestamp":"2026100300","access":"all-access","agent":"user","views":2455}]}
```

So `Chess` had 3,644 views on 1 October 2026, 3,558 on 2 October and 2,455 on 3 October. The answer has one item per day inside the `items` list, and the number sits under `views`. `timestamp` is the date plus the hour `00`. A day with no views comes back as `0`.

### A 404 answer

A wrong title, or a day that is not published yet, gives HTTP 404 with a JSON body such as:

```json
{"detail":"The date(s) you used are valid, but we either do not have data for those date(s), or the project you asked for is not loaded yet. Please check documentation for more information","method":"get","status":404,"title":"Not Found","type":"about:blank","uri":"/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/No_such_page_xyz/daily/20261001/20261003"}
```

A day's views appear the day after (UTC). On 12 November 2026 at 17:24 UTC, 11 November was there and 12 November gave 404. Wikimedia does not document the exact time.

### Polite use

- Send a **User-Agent** that names your tool and a way to contact you. Wikimedia's preferred form is `<client name>/<version> (<contact information>) <library>/<version>`. Requests without one "may be blocked without notice". With `curl`, add `-A "practice (github.com/<username>)"`.
- **Wait for each answer** before you send the next request. Never send many requests at once.
- Ask for a date range in one request instead of one request per day.
- Rules: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html and https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
- Getting started: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/getting-started.html

## Part 2: the data robot (`collect.py` and `daily.yml`)

The robot is a small GitHub Actions job in your own public repository `data-robot`. Every morning it adds yesterday's views of your pages to `pageviews.csv` and commits the file.

| File | What it does |
|---|---|
| `collect.py` | Reads `pages.txt` and appends the new days to `pageviews.csv`. Standard library only, so GitHub's computer needs no installs |
| `daily.yml` | The workflow. It goes in your repository as `.github/workflows/daily.yml` |
| `pages.txt` | You write it: one Wikipedia title per line, such as `Cricket_World_Cup` |

Your repository looks like this:

```
data-robot/
  .github/workflows/daily.yml
  collect.py
  pages.txt
  pageviews.csv     (made by the first run)
  README.md
```

### `collect.py`

Before the first run, change one line at the top to your own repository's address (the script refuses to run with the placeholder):

```python
CONTACT = "github.com/<username>/data-robot"
```

The script sends it inside its User-Agent, for example `data-robot/1.0 (github.com/<username>/data-robot) python-urllib/3.12`, so Wikimedia knows who is asking. The other settings (`PROJECT`, `PAGES_FILE`, `OUTPUT_FILE`, `FIRST_RUN_DAYS`) can stay as they are.

What it does:
- **First run** (no `pageviews.csv` yet): it fetches the last 30 complete days (UTC) for every page. Three pages give **90 rows**.
- **Every later run**: it adds only the days after the last saved day, up to yesterday. If a run was missed, the next run catches up.
- **A page you add later** to `pages.txt` starts with its own 30 days.
- One request per page per run, one after the other.

`pageviews.csv` has the header `date,page,views`, the date as `YYYY-MM-DD`, the page as written in `pages.txt`, and the views as a whole number:

```
date,page,views
2026-10-13,Chess,3397
2026-10-13,Cricket_World_Cup,1487
2026-10-13,Bengaluru,2319
```

A first run prints one line per page, then the total (real run, 13 November 2026):

```
Chess: 30 days (2026-10-13 to 2026-11-11)
Cricket_World_Cup: 30 days (2026-10-13 to 2026-11-11)
Bengaluru: 30 days (2026-10-13 to 2026-11-11)
Wrote 90 new rows to pageviews.csv
```

When something is wrong:
- **A title with a typing mistake** prints `No data for <title>: check the spelling in pages.txt`. The other pages are still fetched, but the script ends with an error, so the run shows a red cross on the Actions tab. Fix `pages.txt` and run it again.
- **A title that contains a comma** (such as `Washington,_D.C.`) prints a note: the week 1 chart code splits lines on commas, so choose a title without one.
- **A day not published yet** is not an error: the script prints `no new days published yet` and the next run catches up.
- **The placeholder `CONTACT`** stops the script with a message that asks you to set it.

You can also run it on your laptop in the folder that holds `pages.txt`: `uv run python collect.py`.

### `daily.yml`

- **Name**: `Daily page views` (this is what the Actions tab shows).
- **Schedule**: `cron: '17 2 * * *'`, which is 02:17 UTC every day, 07:47 India time. GitHub may start a scheduled run some minutes late.
- **Run by hand**: `workflow_dispatch` adds the **Run workflow** button.
- **Permission**: `contents: write`, so the job may commit `pageviews.csv`.
- **One job, `collect`**, on GitHub's Ubuntu computer, with four steps: `Check out the repository`, `Set up Python` (3.12), `Collect page views` (runs `python collect.py`) and `Commit pageviews.csv` (commits as `github-actions[bot]`, only when the file changed).

Facts about schedules (GitHub Docs): the time is UTC; schedules run only on the default branch (`main`); runs near the start of an hour are often delayed; and **in a public repository GitHub turns a schedule off after 60 days without activity in the repository**. If your robot stops, open the Actions tab and switch the workflow on again.

GitHub Actions is free in public repositories. It is switched off in the course organisation, which is why the robot lives in your own account.

## Part 3: the hourly dump files (PageLake, P5 and P6)

Wikimedia publishes one file per hour with the views of every page of every wiki:

```
https://dumps.wikimedia.org/other/pageviews/<YYYY>/<YYYY>-<MM>/pageviews-<YYYYMMDD>-<HH>0000.gz
```

for example https://dumps.wikimedia.org/other/pageviews/2026/2026-11/pageviews-20261102-010000.gz. The folder listing is at https://dumps.wikimedia.org/other/pageviews/ and the official description at https://wikitech.wikimedia.org/wiki/Data_Platform/Data_Lake/Traffic/Pageviews.

### The line format

Each file is gzip-compressed text. Each line has four fields separated by single spaces:

```
domain_code page_title count_views total_response_size
```

Real lines from `pageviews-20261102-010000.gz`:

```
simple Main_Page 308 0
nl.m Hoofdpagina 296 0
sv Portal:Huvudsida 1322 0
sv.m Portal:Huvudsida 218 0
```

- `domain_code`: the wiki. `sv` is Swedish Wikipedia on a desktop browser; `sv.m` is the same wiki on the mobile site.
- `page_title`: the title as in the page's address, with underscores. About 1 line in 3,500 has a title with a double quote `"` (11,576 of the course week's 40,391,181 lines), so tell DuckDB not to treat quotes specially: `read_csv(..., delim = ' ', header = false, quote = '', escape = '')`.
- `count_views`: views in that hour.
- `total_response_size`: always `0` in these files.
- **A file is named after the END of the hour it covers, in UTC.** `pageviews-20261102-010000.gz` holds 00:00 to 01:00 on 2 November. The last hour of 2 November (23:00 to 24:00) is `pageviews-20261103-000000.gz`.

### Size, and why the course keeps six wikis

One full hourly file is 30 to 55 MB (32 to 53 MB on 1 to 12 November 2026; 40,223,886 bytes for `pageviews-20261102-010000.gz`), so one week is about 7 GB. `dumps.wikimedia.org` limits each address to 3 connections at a time and slows down heavy users. A class cannot download that.

So the course keeps only six Wikipedias, on desktop and mobile: `simple` (Simple English), `id` (Indonesian), `ko` (Korean), `nl` (Dutch), `sv` (Swedish) and `vi` (Vietnamese). The lines are kept unchanged, and only lines of those wikis are kept.

### The course week

The course uses **2 to 8 November 2026** (UTC): 7 days, 168 files, from `pageviews-20261102-010000.gz` to `pageviews-20261109-000000.gz`.

The kit copy, filtered to the six wikis and measured on 13 November 2026:

| Day (UTC) | Files | Lines | Bytes |
|---|---:|---:|---:|
| 2 November | 24 | 4,752,273 | 39,987,770 |
| 3 November | 24 | 4,688,074 | 39,431,461 |
| 4 November | 24 | 4,631,129 | 39,059,294 |
| 5 November | 24 | 4,710,860 | 39,612,527 |
| 6 November | 24 | 4,760,808 | 40,195,884 |
| 7 November | 24 | 11,078,530 | 89,642,434 |
| 8 November | 24 | 5,769,507 | 49,466,064 |
| **Week** | **168** | **40,391,181** | **337,395,434** (about 337 MB) |

Most hours are 1.1 to 3.1 MB with 130,000 to 370,000 lines. `pageviews-20261102-010000.gz` has 155,729 lines.

**7 November is different.** The five hours from 10:00 to 15:00 UTC (files `pageviews-20261107-110000.gz` to `pageviews-20261107-150000.gz`) hold 1.2 to 1.7 million lines and 9 to 13 MB each. Almost every extra line is a desktop title with exactly 1 view, on `nl`, `sv`, `vi`, `id` and `ko`: in the 12:00 file, 1,391,709 of 1,487,023 lines have 1 view. It looks like an automated reader that Wikimedia counted as a person. The kit keeps it unchanged: it is real data, and a good thing to notice when you compare days in silver and gold.

### `get_hours.py`

```bash
uv run python ~/de-kit/data/pageviews/get_hours.py --start 2026-11-02 --days 7 --out data/raw
```

| Option | Meaning |
|---|---|
| `--start YYYY-MM-DD` | The first day (UTC). Required |
| `--days N` | How many days (default 1). 7 days give 168 files |
| `--out DIR` | Where the files go (default `data/raw`) |
| `--wikis LIST` | The wikis to keep, comma-separated (default `simple,id,ko,nl,sv,vi`) |
| `--source kit` | (default) Download the filtered course week from the kit's GitHub release. Only 2 to 8 November 2026 with the default wikis |
| `--source wikimedia` | Download Wikimedia's full files and keep only your wikis while they arrive. Use it for other dates or wikis. Slow: about 1 to 2 minutes per hour of data |
| `--check` | Download nothing: check that every file for these dates is in `--out`, complete, with four fields per line and only your wikis |

It prints one line per file (name, lines, size, seconds) and a total. Files already in `--out` are skipped, so if the download stops, run the same command again: it continues where it stopped. A file is saved under its final name only when it is complete. It uses only Python's standard library, one connection at a time, and a User-Agent that names the course kit. Please do not run several copies at once against `dumps.wikimedia.org`: it allows 3 connections per address, and a classroom shares one address.

The kit copy's address: `https://github.com/Anaxionai/de-v3-kit/releases/download/pageviews-2026-11/<file name>`.

### Content warning

These are real reading figures. Lists of the most-viewed pages sometimes include adult or violent titles. You may leave such titles out of anything you publish; say in one line that you did.
