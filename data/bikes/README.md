# Citi Bike trip files and live station feed (CycleCity, P10 and P11)

CycleCity (P10) copies monthly bike-share trip files into your Azure data lake, then cleans and sums them.
In P11 (CycleCity part 2) you land the same files, and the live station feed, in your own AWS buckets.
This guide gives the file addresses, the columns, what is messy in the files, the live feed, and the operator's licence.

**This folder holds no trip data, on purpose.** The operator's licence does not allow the course to host or copy the files.
You download them from the operator yourself: with Data Factory in P10, with your own `land_month` function in P11. See [Licence](#licence).

Every fact below was checked on 13 November 2026 (India time).

## The files the course uses

Citi Bike is run by Lyft Bikes and Scooters, LLC (the operator in this guide).
It publishes one zip file of trips per month for New York, and one for Jersey City and Hoboken in New Jersey.

CycleCity uses the **Jersey City** files, because they are small:

- Jersey City, January 2024 to October 2026: 958,731 to 4,599,971 bytes zipped per month.
- New York, January 2025 to October 2026: 165 MB to 1,051 MB zipped per month. Do not use these in this module.

| What | Address |
|---|---|
| One month (most months) | `https://s3.amazonaws.com/tripdata/JC-YYYYMM-citibike-tripdata.csv.zip` |
| Example: January 2024 | `https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip` |
| Every file, as a web page | https://s3.amazonaws.com/tripdata/index.html |
| Every Jersey City file, as XML | `https://s3.amazonaws.com/tripdata/?prefix=JC-` |
| The operator's data page | https://citibikenyc.com/system-data |

`YYYYMM` is the year and month, for example `202401` for January 2024.
In Data Factory, the base URL of `ls_citibike` is `https://s3.amazonaws.com/tripdata/` and the file name is the relative URL.

The bucket holds 134 Jersey City months, from `JC-201509` (September 2015) to `JC-202610` (October 2026). No month is missing.

## Months whose file name is different

Six months do not follow the pattern. Four of them are months that CycleCity loads:

| Month | File name | When CycleCity loads it |
|---|---|---|
| October 2025 | `JC-202510-citibike-tripdata.zip` | Task 13, the 2024-2025 backfill |
| January 2026 | `JC-202601-citibike-tripdata.zip` | Task 13, the three new months |
| April 2026 | `JC-202604-citibike-tripdata.zip` | Task 22 |
| October 2026 | `JC-202610-citibike-tripdata.zip` | Only if your monthly trigger from task 23 runs after 10 November 2026 |
| July 2022 | `JC-202207-citbike-tripdata.csv.zip` (`citbike`: one letter is missing) | Never |
| August 2017 | `JC-201708 citibike-tripdata.csv.zip` (a space, not a hyphen) | Never |

The four recent names end `-citibike-tripdata.zip` instead of `-citibike-tripdata.csv.zip`.
Task 13's fallback copy, `Copy trips zip name`, handles exactly this case.
It does not handle the 2017 and 2022 names, but the course never loads those months.

For a name that does not exist, the bucket answers with HTTP status 404 and the error code `NoSuchKey`.
That is why `Copy trips` fails for a renamed month, and why the fallback then runs.

New months may arrive with either name. Check the list again in Git Bash before you trust this table:

```bash
curl -s "https://s3.amazonaws.com/tripdata/?prefix=JC-" | grep -o '<Key>[^<]*</Key>' | sed 's/<[^>]*>//g' | grep -v -E '^JC-[0-9]{6}-citibike-tripdata\.csv\.zip$'
```

On 13 November 2026 it printed the six names in the table.
Replace the last `grep ...` with `tail -3` to see the three newest months instead.

## When a new month appears

A month's file appears early in the next month.
From January 2024 to October 2026, 33 of the 34 files were in place by the 9th of the next month.
The one exception was May 2024, which appeared on 26 June 2024.

Your trigger `tr_monthly` (task 23) runs on the 10th.
If a file is late, both copies get 404, the run fails and your alert arrives. Rerun that month after the file appears.

## What is inside one zip

Each zip holds one CSV file named `JC-YYYYMM-citibike-tripdata.csv`.
The CSV's name ends `.csv` even when the zip's name ends `-tripdata.zip`.

In 32 of the 34 zips since January 2024, a second entry sits beside the CSV: `__MACOSX/._JC-YYYYMM-citibike-tripdata.csv`, 462 to 618 bytes.
It is file information from a Mac computer, not trip data. The April 2026 and October 2026 zips do not have it.
When Data Factory unzips a month into bronze, a `__MACOSX` folder lands next to the CSV. Leave it: task 12 explains why.

## Size of one month (measured)

I downloaded three months into a temporary folder, counted the rows, and deleted the files:

| Month | Zip name ends | Zip size (bytes) | CSV size (bytes) | Trips (data rows) |
|---|---|---|---|---|
| January 2024 | `.csv.zip` | 1,883,296 | 10,547,438 | 50,661 |
| January 2026 | `.zip` | 1,441,549 | 8,672,671 | 40,044 |
| October 2026 | `.zip` | 4,599,971 | 24,401,585 | 111,446 |

Each CSV also has one header row. Winter months are the smallest.
Summer and autumn months are 2 to 3 times the size of the January before them.
From January 2024 to October 2026, one month's CSV is 5,606,126 bytes (February 2026) to 26,022,320 bytes (October 2024).

What CycleCity copies into bronze, from the bucket listing and the zip contents:

| After | Months | Zipped (bytes) | CSV in bronze (bytes) |
|---|---|---|---|
| Task 13 | 27: January 2024 to March 2026 | 77,157,795 | 472,047,658 |
| Task 23 | 30: January 2024 to June 2026 | 87,234,493 | 534,462,949 |

## Landing a month on AWS (P11)

The operator's files sit in a public Amazon S3 bucket named `tripdata`, in region `us-east-1` (the bucket's answers carry the header `x-amz-bucket-region: us-east-1`).
Your CycleCity buckets are in `ap-south-1`. In P11 your function `land_month` downloads a month over HTTPS, unzips it in memory and uploads the CSV to your own raw bucket, under `trips/month=YYYYMM/`.

**Why not copy the zip from bucket to bucket?** Two reasons:

- The files are zips. Athena and Glue cannot read a zip archive, so a server-side copy would land a file that nothing can query.
- Reading the bucket through the S3 API, from your laptop or a Lambda function, would also need an IAM permission on `arn:aws:s3:::tripdata/*`. Downloading over HTTPS from `https://s3.amazonaws.com/tripdata/<file>` needs no AWS permission at all.

**The name rule `land_month` uses:**

1. Try `JC-YYYYMM-citibike-tripdata.csv.zip`.
2. If the answer is HTTP 404, try `JC-YYYYMM-citibike-tripdata.zip` (the renamed months above).
3. If that is 404 too, the month does not exist: raise `FeedNotFound`. A missing key answers HTTP 404 with the error code `NoSuchKey`, for example `JC-209901-citibike-tripdata.zip`.

Inside each 2024 zip: the CSV and a `__MACOSX/._JC-YYYYMM-citibike-tripdata.csv` entry. Upload only the `.csv`.
In the CSV, empty values have no quotes (`,,`), text values are in double quotes, and every line ends with CRLF. In the five months below, no trip starts in another month.

The months P11 lands, measured on 13 November 2026:

| Month | CSV size (bytes) | Trips | Which task |
|---|---|---|---|
| January 2024 | 10,547,438 | 50,661 | Task 11 |
| February 2024 | 11,589,492 | 55,613 | Task 11 |
| March 2024 | 13,669,442 | 65,581 | Task 11 |
| April 2024 | 16,494,655 | 79,116, of which 42,970 `electric_bike` | Task 22 |
| May 2024 | 20,299,365 | 97,479 | Task 23 |

The three task-11 months total 35.8 MB, well under the 100 MB limit of your Athena workgroup, even for a query that reads every raw month.

Your downloads stay out of Git: `data/` is never committed, and the course hosts no copy of any month.

## The columns

The three months measured have the same 13 columns, in this order. The operator's data page lists the same 13 fields.

| Column | What it holds | Example |
|---|---|---|
| `ride_id` | The trip's id. Up to September 2026: 16 characters, digits and the letters A to F, in quotes. From October 2026: a number of up to 19 digits, without quotes. | `"0744109F13385D1D"`, `6239929685212553526` |
| `rideable_type` | The kind of bike: `classic_bike` or `electric_bike`. | `electric_bike` |
| `started_at` | When the trip started, as local time (see below). | `2024-01-15 15:18:07` |
| `ended_at` | When the bike was returned, in the same format. | `2024-01-15 15:32:44` |
| `start_station_name` | The name of the station where the trip started. | `Morris Canal` |
| `start_station_id` | That station's short code. Keep it as text. | `JC072` |
| `end_station_name` | The name of the station where the trip ended. Can be empty. | `Oakland Ave` |
| `end_station_id` | That station's short code. Can be empty. | `JC022` |
| `start_lat` | Latitude of the start, in decimal degrees. | `40.712296724` |
| `start_lng` | Longitude of the start, in decimal degrees (negative: west of Greenwich). | `-74.038184762` |
| `end_lat` | Latitude of the end. Can be empty. | `40.7376037` |
| `end_lng` | Longitude of the end. Can be empty. | `-74.0524783` |
| `member_casual` | `member` if the rider has a membership, `casual` if not. | `member` |

The file format:

- A header row, commas between values, UTF-8 text without a byte order mark.
- Every line ends with CRLF (Windows line endings). Spark and Python's `csv` module read this without any change.
- Text values are in double quotes and numbers are not. From October 2026 `ride_id` is a number, so it has no quotes.
- Times have no time zone. They are local time in New York and Jersey City (`America/New_York`, the time zone in the operator's live feed). The trips agree: the fewest start at 03:00 and the most at 17:00.

The first two trips of January 2024:

```text
"ride_id","rideable_type","started_at","ended_at","start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng","end_lat","end_lng","member_casual"
"0744109F13385D1D","electric_bike","2024-01-15 15:18:07","2024-01-15 15:32:44","Morris Canal","JC072","Oakland Ave","JC022",40.712296724,-74.038184762,40.7376037,-74.0524783,"member"
"B1488BFEF9118000","classic_bike","2024-01-13 15:32:50","2024-01-13 15:36:18","JC Medical Center","JC110","Grove St PATH","JC115",40.71539114317,-74.04969155788422,40.71941,-74.04309,"member"
```

The first trip of October 2026, with the new `ride_id` and milliseconds:

```text
6239929685212553526,"electric_bike","2026-10-20 22:01:47.295","2026-10-20 22:06:44.476","JC Medical Center","JC110","Brunswick St","JC023",40.71539114317,-74.04969155788422,40.7241765,-74.0506564,"member"
```

The rows are not sorted by time.

## What is messy

Counted in the three months I measured:

| Check | January 2024 | January 2026 | October 2026 |
|---|---|---|---|
| `ride_id` format | 16 characters, A to F and digits | 16 characters, A to F and digits | number |
| Times with milliseconds | 0 | 40,044 (all) | 111,446 (all) |
| Empty `end_station_id` | 167 | 824 | 394 |
| Empty `start_station_id` | 1 | 1 | 0 |
| Trips that end at or before their start | 2 | 0 | 0 |
| Trips longer than 24 hours | 24 | 95 | 33 |
| Trips that start in the month before | 0 | 13 | 0 |
| Duplicate `ride_id` | 0 | 0 | 0 |
| `electric_bike` / `classic_bike` | 30,846 / 19,815 | 27,497 / 12,547 | 68,886 / 42,560 |
| `member` / `casual` | 42,743 / 7,918 | 34,566 / 5,478 | 83,204 / 28,242 |

What each problem means for CycleCity:

1. **Two `ride_id` formats.** Read every column as text in silver, as task 21 says. Then both formats load into the same column.
2. **Times with and without milliseconds.** Up to May 2024 times have no decimals. From June 2024 they have three, for example `2024-06-01 21:57:43.956`. Spark's `to_timestamp` with no format reads both.
3. **Empty end stations.** The end station's name, id and coordinates can be empty, and not always on the same rows. In January 2026, 824 trips have no `end_station_id` but only 502 have no `end_station_name`.
4. **Trips that end before they start, or last over 24 hours.** Task 21 drops both.
5. **Trips that start in the month before.** January 2026's file has 13 trips that started on 31 December 2025. Counted by `started_at`, they fall on 31 December in gold.
6. **Station ids are text.** Jersey City codes start `JC`, Hoboken codes start `HB`, and New York stations look like `6233.04`. A trip can end in New York: the first trip in January 2026's file ends at `Pier 61 at Chelsea Piers`, `6233.04`. Never cast a station id to a number.

The operator removes three kinds of trips before it publishes a file. Its data page says the files leave out:

> trips that are taken by staff as they service and inspect the system, trips that are taken to/from any of our "test" stations (which we were using more in June and July 2013), and any trips that were below 60 seconds in length

## The live station feed (P10 card 18, P11 tasks 9 and 24)

Citi Bike also publishes live data in GBFS (General Bikeshare Feed Specification, a standard JSON format for bike-share systems).
The operator's data page links the discovery file, which lists every feed. The course uses GBFS version 2.3:

| Feed | Address |
|---|---|
| Discovery file | https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json |
| Station status: bikes and docks free now | https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json |
| Station information: names, places, capacity | https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json |

Card 18 runs this command. On 13 November 2026 (India time) it printed:

```text
$ curl -s https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json | head -c 600
{"data": {"stations": [{"station_id": "2250952630016597152", "num_bikes_available": 9, "num_bikes_disabled": 2, "num_docks_available": 5, "num_docks_disabled": 0, "is_installed": 1, "is_renting": 1, "is_returning": 1, "last_reported": 1794515069, "vehicle_types_available": [{"vehicle_type_id": "1", "count": 3}, {"vehicle_type_id": "2", "count": 6}], "num_ebikes_available": 6, "num_scooters_available": 0, "num_scooters_unavailable": 0}, {"station_id": "2250953816197165238", "num_bikes_available": 3, "num_bikes_disabled": 3, "num_docks_available": 10, "num_docks_disabled": 0, "is_installed": 1,
```

- The feed covers the whole system: 2,520 stations in New York, Jersey City and Hoboken on 13 November 2026. The full response is about 1.08 MB.
- `ttl` is 60: the operator refreshes the feed every 60 seconds. Do not ask for it more than once a minute.
- `last_reported` is a Unix time: seconds since 1 January 1970, in UTC.
- The feed's `station_id` is not the id in the trip files. To match them, use `short_name` in the station information feed. For example, `short_name` `JC110` is `JC Medical Center` (capacity 21), the same station as `JC110` in the trip files.

If an address stops working, open https://citibikenyc.com/system-data and follow its link to the GBFS feed.

### Reading the feed from code (P11)

Your Lambda function never hard-codes the `station_status` address. It reads the discovery file and finds the feed by name:

- The feeds are a list under `data.en.feeds`, each `{"name": ..., "url": ...}`. The one you need has `"name": "station_status"`.
- Use the **2.3** discovery file above. The unversioned file, `https://gbfs.citibikenyc.com/gbfs/gbfs.json`, answers with version 1.1, whose station records have other fields (`legacy_id`, `eightd_has_available_keys`, and no `vehicle_types_available`).

The top level of `station_status` holds `last_updated`, `ttl` (60) and `version` (`2.3`), then `data.stations`. Each station record (version 2.3) has:

| Field | What it holds |
|---|---|
| `station_id` | The feed's id for the station (text) |
| `num_bikes_available`, `num_bikes_disabled` | Bikes that can be rented now, and broken ones |
| `num_docks_available`, `num_docks_disabled` | Free docks, and broken ones |
| `is_installed`, `is_renting`, `is_returning` | 1 or 0 |
| `last_reported` | When the station last reported, in Unix seconds (UTC) |
| `vehicle_types_available` | A list of `{"vehicle_type_id": ..., "count": ...}` |
| `num_ebikes_available` | Electric bikes available |
| `num_scooters_available`, `num_scooters_unavailable` | On most stations only |

What to expect, measured on 13 November 2026:

- 2,520 stations, about 1.08 MB a response.
- About 50 stations report `last_reported` 86400 (2 January 1970): a placeholder, not a real time. 54 have `is_installed` 0. Your first run lands them; a watermark skips them afterwards.
- An hourly run lands about 2,450 stations that reported since the last run: about 1 MB a run, about 25 MB a day.
- The `system_regions` feed names the areas: `70` is JC District (78 stations), `311` is Hoboken District (28 stations), `71` is NYC District.

**Polling rule:** P11's function runs once an hour. Never ask for the feed more than once a minute, its `ttl`.

## Licence

The operator publishes the data under its Data License Agreement, at https://citibikenyc.com/data-sharing-policy.
By downloading or using the data you agree to it. These are its key lines, quoted:

> **License.** Bikeshare hereby grants to you a non-exclusive, royalty-free, limited, perpetual license to access, reproduce, analyze, copy, modify, distribute in your product or service and use the Data for any lawful purpose ("License").

> The License does not authorize you to do, and you will not do or assist others in doing, any of the following:
> (b) Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material, as applicable, in analyses, reports, or studies published or distributed for non-commercial purposes;
> (c) Access the Data by means other than the interface Bikeshare provides or authorizes for that purpose;
> (f) Attempt to correlate the Data with names, addresses, or other information of customers or subscribers of Bikeshare; and
> (g) State or imply that you are affiliated, approved, endorsed, or sponsored by Bikeshare.

Clause (h) also forbids using the trademarks of Lyft Bikes and Scooters or Citigroup without written permission. CITI BIKE and its logo are such marks.

What this means for you:

- **Download each month from the operator's bucket.** That is the interface the operator provides. Data Factory does this for you in P10, and your `land_month` function in P11.
- **Never put the trip files, or a copy of them, in Git or in any public place.** Clause (b) forbids sharing the data as a dataset on its own. This is also why the kit has no copy and no sample.
- **The live station feed counts as Data under the same agreement.** The operator's data page lists it under "Real-Time Data", next to the agreement. Your hourly snapshots stay in your own private bucket: never publish them, share them or stream them on to anyone else, because clause (b) also forbids streaming the data. P11 task 22's changed copy of a month (`data/april-first.csv` and its upload) is private too, and the teardown deletes it.
- **Poll the feed gently.** Once an hour, as P11 does, is normal use of a feed published for apps. Never more than once a minute.
- **You may publish your analysis**, such as your `README.md` and `docs/answers.md` with your numbers, as non-commercial work.
- **Do not try to find out who made a trip**, and never join trips to people's names or addresses.
- **Your product is CycleCity, not Citi Bike.** Do not use the Citi Bike logo, and do not suggest that the operator approves your project.

The agreement asks for no credit line. Put this line in your `cyclecity/README.md` anyway:

```text
Trip data: Citi Bike System Data (Jersey City), https://citibikenyc.com/system-data, used under the Citi Bike Data License Agreement (https://citibikenyc.com/data-sharing-policy). CycleCity is not affiliated with, approved or endorsed by Citi Bike, Lyft or Citigroup.
```
