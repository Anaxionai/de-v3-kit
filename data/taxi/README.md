# New York taxi trips for TaxiScale (P7)

TaxiScale reads the yellow taxi trip records of New York City: one row per trip, about 3 million trips a month.
The NYC Taxi and Limousine Commission (TLC) publishes them as one Parquet file per month.

## What is in this folder

| File | What it is |
|---|---|
| `get_trips.py` | Downloads the trip files for the months you name, and the zone lookup. Standard library only. |
| `README.md` | This guide. |

The data is not in the kit. `get_trips.py` puts it in your product's `data/` folder, which Git ignores.

## Download the data

Run these in Git Bash, from your `taxiscale/` folder:

```bash
uv run --no-project python ~/de-kit/data/taxi/get_trips.py --months 2024-01 --out data
uv run --no-project python ~/de-kit/data/taxi/get_trips.py --months 2024-02 2024-03 --out data
```

You see one line per file, for example:

```text
1 month(s) and the zone lookup into data/
data/yellow/yellow_tripdata_2024-01.parquet  50.0 MB  saved in 16 s
data/zones/taxi_zone_lookup.csv  12 KB  saved in 0 s
Done: 2 downloaded, 0 already there, 0 missing.
```

| Option | Meaning | Default |
|---|---|---|
| `--months` | one or more months as `YYYY-MM`, separated by spaces | (required) |
| `--out` | the folder to write into | `data` |
| `--check` | download nothing; check that the files in `--out` are complete | off |

It writes:

```text
data/yellow/yellow_tripdata_2024-01.parquet
data/zones/taxi_zone_lookup.csv
```

Good to know:

- **Safe to run twice.** A file that is already there is skipped.
- **A stopped download is never left looking finished.** The script writes to a `.part` file and renames it only when the whole file has arrived. If your internet stops, run the same command again.
- **Check your files** with `--check`: a Parquet file must start and end with the bytes `PAR1`, and the zone lookup must have 265 rows.
- **A month that is not published yet** gives `NOT FOUND ... (HTTP 403)`. TLC's server answers 403, not 404, for a missing file.

## The files

Addresses (no key needed):

```text
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet
https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Measured on 13 November 2026 (sizes from the server, row counts from each file's Parquet footer; January and February 2024 also counted in full with DuckDB):

| File | Bytes | Rows | Columns |
|---|---|---|---|
| `yellow_tripdata_2024-01.parquet` | 49,961,641 | 2,964,624 | 19 |
| `yellow_tripdata_2024-02.parquet` | 50,349,284 | 3,007,526 | 19 |
| `yellow_tripdata_2024-03.parquet` | 60,078,280 | 3,582,628 | 19 |
| `yellow_tripdata_2025-01.parquet` | 59,158,238 | 3,475,226 | 20 |
| `taxi_zone_lookup.csv` | 12,331 | 265 | 4 |

Each month is about 50-75 MB. The three months of 2024 that TaxiScale uses total 160 MB.

## The trip columns

The 2024 files have these 19 columns. The meanings come from TLC's yellow trip data dictionary (dated 18 March 2025). The types are the Parquet types as DuckDB reads them.

| Column | Type | Meaning |
|---|---|---|
| `VendorID` | integer | The company that sent the record: 1 = Creative Mobile Technologies, 2 = Curb Mobility, 6 = Myle Technologies, 7 = Helix |
| `tpep_pickup_datetime` | timestamp | When the meter was switched on |
| `tpep_dropoff_datetime` | timestamp | When the meter was switched off |
| `passenger_count` | big integer | Number of passengers |
| `trip_distance` | double | Trip distance in miles, from the taximeter |
| `RatecodeID` | big integer | Rate: 1 = standard, 2 = JFK, 3 = Newark, 4 = Nassau or Westchester, 5 = negotiated, 6 = group ride, 99 = unknown |
| `store_and_fwd_flag` | text | `Y` if the car stored the trip and sent it later (no connection), `N` if not |
| `PULocationID` | integer | Taxi zone where the meter was switched on (pickup) |
| `DOLocationID` | integer | Taxi zone where the meter was switched off (drop-off) |
| `payment_type` | big integer | 0 = flex fare, 1 = credit card, 2 = cash, 3 = no charge, 4 = dispute, 5 = unknown, 6 = voided trip |
| `fare_amount` | double | The time-and-distance fare from the meter, in US dollars |
| `extra` | double | Other extras and surcharges |
| `mta_tax` | double | Tax set by the metered rate in use |
| `tip_amount` | double | Card tips only; cash tips are not included |
| `tolls_amount` | double | All tolls paid on the trip |
| `improvement_surcharge` | double | A surcharge charged at the start of every trip since 2015 |
| `total_amount` | double | The total charged to passengers, without cash tips |
| `congestion_surcharge` | double | New York State congestion surcharge |
| `Airport_fee` | double | Fee for pickups at LaGuardia and JFK airports |

Column changes:

- **`Airport_fee` has a capital A in the Parquet files.** The data dictionary writes `airport_fee`. Spark matches column names without caring about case by default, but use `Airport_fee` to be safe.
- **From January 2025** the files add a 20th column, `cbd_congestion_fee`: "Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025."
- **From June 2026** the files add a 21st column, `request_source`. The data dictionary does not describe it yet. TaxiScale uses 2024 files, so neither new column appears in your work.

## The zone lookup

`taxi_zone_lookup.csv` maps the zone numbers in `PULocationID` and `DOLocationID` to names.

| Column | Meaning | Example |
|---|---|---|
| `LocationID` | the zone number, 1 to 265 | `132` |
| `Borough` | the borough | `Queens` |
| `Zone` | the zone name | `JFK Airport` |
| `service_zone` | TLC's service area | `Airports` |

- 265 rows after the header line. The header and the text values are in double quotes (`132,"Queens","JFK Airport","Airports"`), and the lines end with Windows line endings (CRLF). Spark's CSV reader handles both.
- Two rows are not real places: **264** is `Unknown`, `N/A`, `N/A` and **265** is `N/A`, `Outside of NYC`, `N/A`. Leave them out of reports about places.

## Known problems in the data

- **Pickups outside the file's month.** The January 2024 file holds 18 trips that did not start in January 2024: 15 earlier (2 in December 2002, 3 in January 2009 and 10 in December 2023) and 3 on 1 February 2024. Filter on the month you mean.
- **Empty values.** In January 2024, 140,162 trips have no `passenger_count` and no `Airport_fee`.
- **No guarantee.** TLC did not create the trip data and says it makes no representations about its accuracy.

## Publishing

TLC's page says: "Trip data is published monthly on this website, typically with a two-month delay to allow time for full vendor submissions."
On 13 November 2026 the newest month listed was September 2026.

## Terms of use and credit

- TLC's trip record page states no licence.
- The same trip records are also published on NYC Open Data. NYC Open Data's FAQ says: "Open Data belongs to all New Yorkers. There are no restrictions on the use of Open Data."
- TLC's disclaimer: "The trip data was not created by the TLC, and TLC makes no representations as to the accuracy of these data."

Credit the data in your README and in anything you publish: **"Data: NYC Taxi and Limousine Commission (TLC) Trip Record Data."**

## Links

- TLC trip record data (NYC Taxi and Limousine Commission): https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Yellow trip data dictionary (NYC Taxi and Limousine Commission, PDF): https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
- NYC Open Data FAQ (City of New York): https://www.nyc.gov/opendata/get-started/FAQs
