# The course datasets

Every dataset the course uses: where it comes from, its licence and the credit line to copy, how big it is, how you get it, and whether the kit ships a sample. Each folder's own README has the details.

**Data stays out of Git.** Scripts download or generate data into your product's `data/` folder, which your `.gitignore` ignores. The kit itself holds only small files: the two IPL season files, and the sample folders named below.

**Credit lines.** When you publish anything made from a dataset (a README, a chart, a profile page), copy its credit line. Most licences below require it, and it is good practice for the others.

## Summary

"Paid course" says whether the source's terms allow this paid course to use the data as it does: students download it themselves, and the kit hosts only the files named in "Sample". **To confirm** means the terms are silent or unclear, and the centre should ask the publisher before the cohort starts.

| Dataset | Folder | Used in | Licence | Paid course |
|---|---|---|---|---|
| IPL ball-by-ball (Cricsheet) | `ipl/` | Launchpad, P2, P10 | ODC-By 1.0 | Yes, with credit |
| Wikipedia page views | `pageviews/` | Launchpad, map weeks, P5, P6 | CC0 1.0 | Yes |
| Public APIs without a key | `public-apis.md` | Launchpad, map weeks | One per API | Yes for the listed APIs (one has no terms) |
| Airports (OurAirports) | `map/` | Map weeks | Public domain | Yes |
| Wikipedia live edits (EventStreams) | `map/`, `edits/` | Map weeks, P8 | CC BY-SA 4.0 | Yes, with credit; holds personal data |
| Market prices (data.gov.in) | `prices/` | P1 | GODL-India | Yes, with credit |
| Online Retail II (UCI) | `retail/` | P3, P14 | CC BY 4.0 | Yes, with credit |
| Air quality (OpenAQ) | `airquality/` | P4 | OpenAQ terms plus one licence per provider | **To confirm** |
| Station database (generated) | `airquality/stationdb/` | P4 | Made up by the kit | Yes |
| NYC taxi trips (TLC) | `taxi/` | P7, P13 | No licence stated | **To confirm** |
| GitHub events (GH Archive) | `gharchive/` | P9, P12 | No licence stated | **To confirm** |
| Citi Bike trips and live station feed | `bikes/` | P10, P11 | Citi Bike Data License Agreement | Yes to teach with; **never host, mirror or stream** |
| BigQuery public tables (GH Archive day tables) | `bigquery/` | P12 | No licence stated (as GH Archive) | **To confirm** (as GH Archive) |
| Clinic data and visit notes (generated) | `clinic/` | P13, P15 | Made up by the kit | Yes |

## The datasets

### IPL ball-by-ball data: `ipl/`
- **Source**: Cricsheet, https://cricsheet.org/. `ipl_json.zip` (P2) and `ipl_csv2.zip` (the season files).
- **Licence**: Open Data Commons Attribution License 1.0 (ODC-By 1.0). `ipl/NOTICE.md` explains the conditions.
- **Credit line**: `Match data from Cricsheet (https://cricsheet.org/), licensed under the Open Data Commons Attribution License 1.0 (https://opendatacommons.org/licenses/by/1-0/).`
- **Size**: `season.csv` 2,630,140 bytes, 17,523 rows (the 2026 season, 74 matches). `season-published.csv` 2,640,571 bytes, 17,581 rows (wrong on purpose). `get_matches.py` downloads 5,214,168 bytes and saves 1,243 match files plus `README.txt` and `LICENSE.txt`, 105,718,901 bytes in all (13 November 2026).
- **Get it**: `season.csv` and `season-published.csv` are in the kit. `uv run python ~/de-kit/data/ipl/get_matches.py --out data/matches` for every match.
- **Sample**: the two season files.
- **Paid course**: yes. ODC-By allows use, sharing and changes, including commercial use, with credit. Cricsheet's own `README.txt` adds an informal wish that people "can't just take data and sell it"; the course does not sell the data, and a courtesy note to Cricsheet would remove any doubt.

### Wikipedia page views: `pageviews/`
- **Source**: Wikimedia Foundation. The page-views API (`https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/...`) and the hourly dump files (`https://dumps.wikimedia.org/other/pageviews/`).
- **Licence**: CC0 1.0. Use is also subject to Wikimedia's terms of use and User-Agent policy.
- **Credit line**: `Page-view data: Wikimedia Foundation (CC0 1.0).`
- **Size**: an API answer is a few kilobytes; the data robot's first run writes 90 rows for 3 pages. A full hourly dump file is 30 to 55 MB (about 7 GB a week). The course week, filtered to six wikis, is 168 files, 40,391,181 lines and 337,395,434 bytes (filtered from 7,948,158,169 bytes of full files).
- **Get it**: `collect.py` and `daily.yml` (the data robot); `get_hours.py --start 2026-11-02 --days 7 --out data/raw` for the dump files. P6 (PageLake part 2) runs the same course week through Airflow, so it downloads nothing new; `get_hours.py --check` lists any hourly file that is missing.
- **Sample**: the filtered course week is published as a release of the kit repository (release `pageviews-2026-11`), not in the kit's files. `get_hours.py` downloads it by default.
- **Paid course**: yes.

### Public APIs without a key: `public-apis.md`
- **Source**: 11 example addresses from 10 free services (Wikipedia twice, USGS, World Bank, Frankfurter, GitHub, Open Library, Crossref, Sunrise-Sunset.org, India Post PIN codes, Carbon Intensity), each fetched on 13 November 2026.
- **Licence**: one per API, listed in the file. Sunrise-Sunset.org asks for the credit `Sun data by Sunrise-Sunset.org`.
- **Size**: each answer is under 60 kB.
- **Get it**: `curl -s "<address>" -o other-api.json`.
- **Sample**: none.
- **Paid course**: yes for the listed APIs: students call them for their own learning. The India Post PIN code service publishes no terms. Open-Meteo is left out on purpose: its free API is for non-commercial use only.

### Airports: `map/`
- **Source**: OurAirports, `https://davidmegginson.github.io/ourairports-data/airports.csv` (the GitHub copy; ourairports.com had a certificate error on 12 and 13 November 2026).
- **Licence**: public domain; the GitHub repository carries The Unlicense.
- **Credit line**: `Airport data from OurAirports (ourairports.com), released to the public domain.`
- **Size**: 12,758,762 bytes, 86,351 airports, 19 columns (13 November 2026). Rebuilt every day.
- **Get it**: `curl -L -o data/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv`.
- **Sample**: none.
- **Paid course**: yes.

### Wikipedia live edits (EventStreams): `map/` and `edits/`
- **Source**: Wikimedia EventStreams, `https://stream.wikimedia.org/v2/stream/recentchange`.
- **Licence**: the edit data is CC BY-SA 4.0. The service is meant for small tools: one connection, a User-Agent, no long-running copies.
- **Credit line**: `Edit data from Wikimedia projects via EventStreams, CC BY-SA 4.0.`
- **Size**: 2,576 events in 60 seconds on 13 November 2026 (about 20 to 60 a second).
- **Get it**: `map/watch_edits.py --seconds 60 --save data/edits.jsonl`; in P8, `edits/late_and_duplicate.py` re-sends events late and twice.
- **Sample**: none.
- **Paid course**: yes, with credit. Events hold usernames, which are personal data: never commit saved events.

### Market prices: `prices/`
- **Source**: data.gov.in, "Variety-wise Daily Market Prices Data of Commodity" (AGMARKNET, Ministry of Agriculture and Farmers Welfare), API `https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24`. Needs a free key in `DATA_GOV_IN_KEY`.
- **Licence**: Government Open Data License - India (GODL-India), https://www.data.gov.in/Godl.
- **Credit line**: the exact line is in `prices/README.md` (provider, year, dataset, platform, date, address, licence).
- **Size**: estimated at about 1,000 to 1,500 rows a day for the course's commodities, about 30,000 rows a month (not measured: nobody had a key). A one-day snapshot of the whole dataset on 18 October 2023 had 6,434 rows.
- **Get it**: `get_prices.py --month YYYY-MM` (one CSV per day plus `source.json`); `--check` tests a key.
- **Sample**: `prices/sample/`, one month for students without a key. **Not in the kit yet**: there is no keyless route to the data, so it needs a staff key.
- **Paid course**: yes. GODL allows commercial and non-commercial use with the attribution line.

### Online Retail II: `retail/`
- **Source**: UCI Machine Learning Repository, `https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip`.
- **Licence**: CC BY 4.0.
- **Credit line**: `Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.` plus the licence line in `retail/README.md`, which also says what the kit's conversion changed.
- **Size**: the zip is 45,622,418 bytes; the CSV is 116,441,405 bytes, 1,067,371 rows (1,044,848 without the overlapping December 2010 rows).
- **Get it**: `get_retail.py --out data`; `make_changes.py --student <your-id>` writes a customer change batch.
- **Sample**: none; the kit never hosts a copy.
- **Paid course**: yes, with the citation, a licence link and a note of the changes.

### Air quality: `airquality/`
- **Source**: OpenAQ API v3, `https://api.openaq.org/v3/...`. Needs a free key in `OPENAQ_API_KEY` (one key per person; sharing a key is forbidden).
- **Licence**: OpenAQ's terms of use, plus the licence of each data provider, given per location in `licenses`.
- **Credit line**: `Air-quality data from OpenAQ (openaq.org)`, plus each provider's name and licence.
- **Size**: limited by the API: 60 calls a minute, 2,000 an hour, at most 1,000 results a page. Not measured: the kit builders had no key.
- **Get it**: ClearAir's own client (`load-api`), explained in `airquality/README.md`.
- **Sample**: `airquality/sample/`, real API pages for students whose key has not arrived. **Not in the kit yet**: every call needs a key, and only locations whose licence allows redistribution and commercial use may go in it.
- **Paid course**: **to confirm.** The terms forbid products that "duplicate or directly compete with" OpenAQ's service and say nothing about courses. Students using their own keys for learning looks fine, but the centre should confirm classroom use with OpenAQ before launch.

### Station database: `airquality/stationdb/`
- **Source**: generated by the kit. `compose.yaml` starts PostgreSQL 16 on port 5433; `change_stations.py --student <your-id> [--reset]` fills and changes it.
- **Licence**: none needed; every name is made up.
- **Size**: 400 stations after a reset; each batch updates 10, adds 5 and deletes 3.
- **Sample**: none needed.
- **Paid course**: yes.

### NYC taxi trips: `taxi/`
- **Source**: NYC Taxi and Limousine Commission (TLC), `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet` and the zone lookup `.../misc/taxi_zone_lookup.csv`.
- **Licence**: none stated on the TLC page; the NYC.gov terms say "All rights are reserved".
- **Credit line**: `NYC Taxi and Limousine Commission (TLC) Trip Record Data`, with TLC's note that it does not guarantee the data's accuracy.
- **Size**: January 2024 is 49,961,641 bytes and 2,964,624 trips; February 2024 50,349,284 bytes and 3,007,526 trips; March 2024 60,078,280 bytes and 3,582,628 trips; the zone lookup 12,331 bytes and 265 zones.
- **Get it**: `taxi/get_trips.py --months 2024-01 [2024-02 ...] --out data`.
- **Sample**: none.
- **Paid course**: **to confirm**, ideally by asking TLC. The data is widely used for teaching, but no licence is published.

### GitHub events: `gharchive/`
- **Source**: GH Archive, `https://data.gharchive.org/YYYY-MM-DD-H.json.gz` (one file per hour).
- **Licence**: none stated by GH Archive. The events contain GitHub usernames and other personal data.
- **Credit line**: `GitHub event data from GH Archive (gharchive.org).`
- **Size**: 5.5 to 12.8 MB an hour, about 216 MB for 1 January 2018; a day in 2024 or 2025 is 2.3 to 2.8 GB.
- **Get it**: `gharchive/get_hours.py --date 2018-01-01 --hours 0-23 --out data/gharchive` (P9). In P12 (GitPulse part 2) the same events are read in BigQuery's public day tables, with nothing downloaded (see `bigquery/`).
- **Sample**: none.
- **Paid course**: **to confirm.** No terms are published, and the data holds personal data.

### Citi Bike trips: `bikes/`
- **Source**: Citi Bike (Lyft), trip files at `https://s3.amazonaws.com/tripdata/` (the course uses the Jersey City files `JC-YYYYMM-citibike-tripdata.csv.zip`), and the live station feed, found through the GBFS 2.3 discovery file `https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json` (station status at `https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json`).
- **Licence**: the Citi Bike Data License Agreement (https://citibikenyc.com/data-sharing-policy): use "for any lawful purpose", but section 2(b) forbids hosting, streaming, publishing or selling the data "as a stand-alone dataset". The operator lists the live feed on the same system-data page, so the course treats the feed as Data under the same agreement.
- **Credit line**: name Citi Bike as the source and say the course is not connected with Citi Bike or Lyft.
- **Size**: 1 to 4.5 MB zipped and about 50,000 trips a month for Jersey City (January 2024: 50,661 trips, a 10.5 MB CSV; May 2024: 97,479 trips, 20.3 MB); the New York files are 150 MB to 1 GB. The station feed is about 1.1 MB a response for 2,520 stations; P11's hourly landing keeps the changed stations only, about 25 MB a day.
- **Get it**: directly from the operator's address. In P10, Azure Data Factory copies the files. In P11 (CycleCity part 2, on AWS), the student's code downloads a month over HTTPS, unzips it and uploads the CSV to the student's own private bucket, because Athena and Glue cannot read zip files; a Lambda function polls the station feed once an hour, never more than once a minute.
- **Sample**: **none allowed**: the kit must never host or mirror the files.
- **Paid course**: yes to teach with: students download the data from the operator for their own analysis. Station snapshots stay in the student's private bucket and are never republished or streamed. A lawyer's glance at sections 2(b) and 2(e) is advised before launch.

### BigQuery public tables: `bigquery/`
- **Source**: Google BigQuery public datasets: GH Archive's day tables `githubarchive.day.YYYYMMDD` (one table per UTC day, and the wildcard `githubarchive.day.201801*` with `_TABLE_SUFFIX`), and `bigquery-public-data.samples.shakespeare` for the learn cards. P12 reads 1 to 8 January 2018, the same events P9 loaded into Snowflake.
- **Licence**: GH Archive states no licence (see the GitHub events section above). The Shakespeare table is one of Google's BigQuery samples.
- **Credit line**: `Data: GH Archive (https://www.gharchive.org), a record of GitHub's public events.`
- **Size**: not measured on BigQuery (the kit builders had no account). Estimated from GH Archive's hourly files: `day.20180101` about 1.41 GB (687,304 events) and `day.20180102` about 3.03 GB (1,199,910 events); the JSON column `payload` holds 85 to 88% of each day's bytes. `bigquery/README.md` gives the per-column sizes and the scan budget (2 GB a query, 10 GB for the five final runs).
- **Get it**: queries in the BigQuery sandbox or `bq`, inside the free monthly allowance; nothing is downloaded.
- **Sample**: none.
- **Paid course**: **to confirm**, as for GH Archive. The course stores none of the data and publishes only counts and repository names.

### Clinic data: `clinic/`
- **Source**: generated by `clinic/make_clinic.py --student <your-id> --days 30`: about 1,200 patients, 40 doctors and 300 to 450 appointments a day, with deliberate flaws. In P15 (CareLine part 2), `--notes` adds one visit-notes file a day in `notes/`: made-up notes from two pilot doctors, about 550 to 650 notes and 27,000 to 32,000 words in 30 days, with planted phone numbers, emails and names to find and mask, and two corrected notes a day. The P13 files stay byte for byte the same.
- **Licence**: none needed; every name and note is made up, and no real person's data is used.
- **Sample**: none in the kit.
- **Paid course**: yes. In P15 only masked note text is ever sent to a model: Google's terms for the free Gemini tier say not to submit personal information. `clinic/models.md` explains the free model key.

## Other data the course touches

- **P13** reads a Great Expectations tutorial sample of NYC taxi trips (`yellow_tripdata_sample_2019-01.csv`, 10,000 rows) from the `great-expectations/gx_tutorials` repository. Its licence is not stated there; it is TLC data (see the taxi section).
- **P14** uses Microsoft's Adventure Works sample report from `github.com/microsoft/powerbi-desktop-samples` (MIT licence).
- **The capstone briefs** suggest four more sources, each with its own terms: the Carbon Intensity API for Great Britain (CC BY 4.0; its terms forbid selling access), NYC 311 service requests (NYC Open Data: no restrictions on use), the Environment Agency flood-monitoring API (Open Government Licence v3.0) and the Crossref API (metadata usable for any purpose; abstracts may be copyrighted). A capstone you choose yourself must use a source whose licence allows a paid course: no "non-commercial only" data.

## Checked on

Licence facts come from each module author's checks on 12 and 13 November 2026, and from the kit builders' own downloads on 13 November 2026. If a publisher changes its terms, the folder README is updated first.
