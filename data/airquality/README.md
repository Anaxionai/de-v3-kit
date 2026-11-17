# Air-quality data: the OpenAQ API and the station database (ClearAir, P4)

ClearAir loads from two sources:

1. **The OpenAQ API**: hourly air-quality readings from measuring stations around the world. You need a free key.
2. **The station database**: a small PostgreSQL database on your laptop (port 5433) that plays a company's own system. It holds made-up stations, and a script changes them so you have something to load.

Credit line for your README: **Air-quality data from OpenAQ (openaq.org)**, followed by the licence of each provider whose data you show (see "Licences" below).

## Part 1: the OpenAQ API

### Get a key

1. Sign up at https://explore.openaq.org/register. Use your own email address.
2. Confirm the email, then sign in. Your key appears on your account page: https://explore.openaq.org/account. You can also make a new key there.
3. Put it in ClearAir's `.env` file, never in code or in Git:

   ```
   OPENAQ_API_URL=https://api.openaq.org
   OPENAQ_API_KEY=<your key>
   ```

   Your `.env.example` keeps the line `OPENAQ_API_KEY=` with no value.

Each person may register only one key, and OpenAQ's terms forbid giving your key to anyone else. Never share it with a classmate, and never paste it into a chat, an issue or `evidence.md`.

Your key has not arrived? Use the sample pages: see "What to do if your key has not arrived" below.

### The address and the header

- `OPENAQ_API_URL` is the host, `https://api.openaq.org`. Every path starts with `/v3`. (`https://api.openaq.org` answers 200, but `https://api.openaq.org/v3` on its own answers 404.)
- Send the key in the header `X-API-Key`. Without it every call answers 401 with `{"message": "Unauthorized. A valid API key must be provided in the X-API-Key header."}` (checked on 13 November 2026).
- Versions 1 and 2 of the API were switched off on 31 January 2025 and answer 410. Ignore old tutorials that use `/v2`.

Try it in Git Bash once your key is in `.env`:

```bash
set -a; source .env; set +a
curl -s -H "X-API-Key: $OPENAQ_API_KEY" "$OPENAQ_API_URL/v3/locations/2178" | uv run python -m json.tool | head -30
```

### The endpoints the course uses

| Call | What it returns |
|---|---|
| `GET /v3/locations?coordinates=<lat>,<lon>&radius=<metres>&limit=100&page=N` | Measuring stations ("locations") within `radius` metres (at most 25,000) of a point |
| `GET /v3/sensors/<sensor-id>/hours?datetime_from=<UTC time>&datetime_to=<UTC time>&limit=100&page=N` | One sensor's hourly averages, oldest first |
| `GET /v3/locations/<id>` | One location, for example `2178` (the example in OpenAQ's documentation) |

**`coordinates` is latitude first, then longitude**, for example `coordinates=12.9716,77.5946` for Bengaluru. OpenAQ's own Examples page shows longitude first; that example fails with 422.

Each location has `id`, `name`, `locality`, `timezone`, `country`, `coordinates`, `licenses`, `datetimeFirst`, `datetimeLast` and `sensors`. Each sensor has an `id`, a `name` and a `parameter` with `id`, `name` (for example `pm25`), `units` and `displayName`.

Each hourly result has `value`, `parameter` (`id`, `name`, `units`), `period`, `coverage`, `summary` and `flagInfo`. Inside `period`:
- `datetimeFrom.utc` is the start of the hour and `datetimeTo.utc` is its end. ClearAir stores `period.datetimeTo.utc` as `period_end`.
- Hours are "time-ending": the reading for 03:00 covers 02:00 to 02:59.

### Limits

- 60 calls a minute and 2,000 calls an hour per key.
- Most answers carry the headers `x-ratelimit-used`, `x-ratelimit-limit`, `x-ratelimit-remaining` and `x-ratelimit-reset`.
- Above the limit the API answers 429. Wait and try again; never retry in a tight loop. Breaking the limits again and again can get a key banned.
- ClearAir's client sleeps 1 second after each call, which keeps you far below the limits.

Status codes you will meet: 401 (no key or a wrong key), 404 (an id that does not exist), 422 (a bad parameter, such as longitude first), 429 (too many calls) and 410 (an old API version).

### Paging

- `limit` is 100 by default and at most 1,000. `page` starts at 1.
- On a full page, `meta.found` can be the text `">100"` instead of a number, so do not use it as a total.
- Keep asking for the next page until a page has fewer results than `limit`.

### Times

- Send UTC times with a `Z`, for example `2026-11-05T00:00:00Z`. A time without a zone is read as the station's local time.
- `datetime_from` is exclusive (results after it) and `datetime_to` is inclusive (results up to and including it).

### What to do if your key has not arrived

Sample pages are meant to ship in `sample/` in this folder, in exactly the layout ClearAir saves (`<run-id>/locations-001.json` and `<sensor-id>/page-001.json`). **They are not in the kit yet**: `sample/README.md` explains why and what to do meanwhile. Until they arrive, ask your mentor, and build the parts of task 8 that do not need the API (settings, the client with a fake page, the tests).

When the pages are there, copy one run into your project and load it without calling the API:

```bash
cp -r ~/de-kit/data/airquality/sample/<run-id> clearair/data/raw/
uv run --env-file .env python -m clearair.cli load-api --raw data/raw/<run-id>
```

### Documentation

- Quick start: https://docs.openaq.org/using-the-api/quick-start
- API key: https://docs.openaq.org/using-the-api/api-key
- Rate limits: https://docs.openaq.org/using-the-api/rate-limits
- Pagination: https://docs.openaq.org/using-the-api/pagination
- Dates and times: https://docs.openaq.org/using-the-api/dates-datetimes
- Locations and sensors: https://docs.openaq.org/resources/locations and https://docs.openaq.org/resources/sensors
- Licences: https://docs.openaq.org/resources/licenses
- Terms of use: https://docs.openaq.org/about/terms

### Licences

OpenAQ collects data from many providers (governments, research groups, low-cost sensor networks). Each location carries its provider's licence in `licenses`, with fields such as `commercialUseAllowed`, `attributionRequired`, `redistributionAllowed`, `shareAlikeRequired` and `modificationAllowed`. OpenAQ's terms ask you to credit OpenAQ as well as the original provider.

For your product README: credit OpenAQ with the line above, and name the provider and licence of each location you show. Do not publish raw readings of a location whose licence does not allow redistribution.

## Part 2: the station database

A small PostgreSQL 16 database that plays ClearAir's second source: the stations table of the company's own system.

| | |
|---|---|
| Start it | `docker compose up -d` in `~/de-kit/data/airquality/stationdb` |
| Is it ready? | `docker compose ps` shows `(healthy)` after about 10 seconds |
| From your laptop | `localhost:5433`, database `stationdb`, user `source`, password `source` |
| In `.env` | `STATIONDB_URL=postgresql://source:source@localhost:5433/stationdb` |
| From another container | `stationdb:5432` inside the same Compose network, or `host.docker.internal:5433` from any container |
| psql | `docker compose exec stationdb psql -U source -d stationdb` |
| Stop it | `docker compose down` (rows are kept in the volume `stationdb_stationdb-data`) |
| Delete its rows | `docker compose down -v` |

It runs with `wal_level=logical` (the `command:` line in `compose.yaml`), so a change-data-capture tool such as Debezium can read every insert, update and delete from the database's own log. You need this only for the Stretch goal in P8; the user `source` already has the replication right it needs.

It uses port 5433 because the data lab's PostgreSQL already uses 5432. The two are separate databases: `connection refused` on 5433 means the station database is not running; on 5432, the data lab is not running.

The password `source` works only on your laptop. Never use it on a real server.

### The `stations` table

The first start creates an empty table with these nine columns:

| Column | Type | Meaning |
|---|---|---|
| `station_id` | `INTEGER PRIMARY KEY` | The station's number. A deleted id is never used again |
| `name` | `TEXT NOT NULL` | A made-up name, such as `Lakeside North Gate` |
| `city` | `TEXT NOT NULL` | One of 24 made-up cities |
| `latitude` | `NUMERIC(8,5) NOT NULL` | Degrees north (negative is south) |
| `longitude` | `NUMERIC(8,5) NOT NULL` | Degrees east (negative is west) |
| `operator` | `TEXT NOT NULL` | Who runs the station |
| `status` | `TEXT NOT NULL` | `active` or `maintenance` |
| `installed_on` | `DATE NOT NULL` | The day the station was installed |
| `updated_at` | `TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()` | When the row last changed |

There is also an index on `updated_at`, and a trigger: `stations_touch BEFORE UPDATE ... FOR EACH ROW` calls `touch_updated_at()`, which sets `NEW.updated_at := clock_timestamp()`. So every `UPDATE` stamps the row with the time of the change, even if the program that changed it forgot. Run `\d stations` in psql to see it.

### `change_stations.py`: fill and change the table

It needs the database running. `uv run` installs its one package (`psycopg`) by itself, from the lines at the top of the script.

```bash
uv run ~/de-kit/data/airquality/stationdb/change_stations.py --student <your-id> --reset
uv run ~/de-kit/data/airquality/stationdb/change_stations.py --student <your-id>
```

`<your-id>` is your GitHub username in lower case. It picks the random numbers, so your stations differ from your classmates' but are the same after every reset.

**With `--reset`** it empties `stations` and adds exactly 400 made-up stations, ids 1 to 400. About 8 in 100 are in `maintenance`. Their `updated_at` times are spread over the last 180 days, and the two newest stations share the same time (one hour before the reset, on the hour). It prints, for example:

```
reset: 400 stations, newest updated_at 2026-11-12 19:00:00+00 (2 stations share it)
```

**With no flag** it applies one change batch, different on each run:
- updates 10 stations (a status change or a new operator; the trigger moves their `updated_at`),
- adds 5 stations with new ids above every id used before,
- deletes 3 other stations with a hard `DELETE` (they are gone: no row, no flag).

It prints the ids of each kind and the new total:

```
batch 1: updated 10 (ids 5, 37, 69, 87, 187, 225, 235, 266, 372, 395), added 5 (ids 401-405), deleted 3 (ids 10, 196, 384); stations now 402
```

Run it after a full load, then load again: an incremental load (one that reads only changed rows) must find the 10 updated and the 5 added stations, and must notice the 3 that are gone. `--url <address>` or the `STATIONDB_URL` variable points it at another database; `--help` lists the options.

If it cannot connect, it says so and prints the start command. Measured on 13 November 2026: after a reset and one batch, `SELECT COUNT(*) FROM stations WHERE updated_at >= <the newest reset time>` returns 17 rows (10 updated, 5 added and the 2 that share the newest reset time).
