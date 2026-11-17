# Map weeks: the airports file and the live edit stream

The map weeks use two public sources:

1. **The airports file**: one small public CSV of every airport in the world, for your first database load and your first pipeline.
2. **The live edit stream**: every change on Wikipedia as it happens, read with `watch_edits.py`, for your first look at a stream.

## The airports file (OurAirports)

| | |
|---|---|
| Address | `https://davidmegginson.github.io/ourairports-data/airports.csv` |
| Publisher | OurAirports (https://ourairports.com/), data files on GitHub: https://github.com/davidmegginson/ourairports-data |
| Licence | Public domain. The GitHub repository carries The Unlicense. No permission is needed, but please credit OurAirports |
| Credit line | `Airport data from OurAirports (ourairports.com), released to the public domain.` |
| Updated | Every day: the row count changes a little from day to day |
| Size on 13 November 2026 | 12,758,762 bytes; 86,352 lines (`wc -l`): 1 header line and 86,351 airports; 19 columns |

Download it in Git Bash:

```bash
mkdir -p data
curl -L -o data/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv
head -n 2 data/airports.csv
wc -l data/airports.csv
```

The server sends `Access-Control-Allow-Origin: *`, so the DuckDB web shell can read the address directly: `SELECT count(*) FROM 'https://davidmegginson.github.io/ourairports-data/airports.csv';`. The site ourairports.com itself failed with a security-certificate error on 12 and 13 November 2026, so the course uses the GitHub address above.

The first line of the file is exactly:

```
"id","ident","type","name","latitude_deg","longitude_deg","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","icao_code","iata_code","gps_code","local_code","home_link","wikipedia_link","keywords"
```

### The columns

| Column | Meaning | Example (Bengaluru) |
|---|---|---|
| `id` | OurAirports' internal number | `35145` |
| `ident` | The airport's code in OurAirports. Unique: 86,351 different values for 86,351 rows | `VOBL` |
| `type` | One of 7 values: `small_airport` (42,789), `heliport` (23,283), `closed` (13,661), `medium_airport` (4,107), `seaplane_base` (1,274), `large_airport` (1,175), `balloonport` (62) | `large_airport` |
| `name` | The airport's name | `Kempegowda International Airport Bengaluru` |
| `latitude_deg` | Degrees north (negative is south) | `13.1979` |
| `longitude_deg` | Degrees east (negative is west) | `77.706299` |
| `elevation_ft` | Height above sea level, in feet. Empty for 14,983 airports; can be negative | `3000` |
| `continent` | `AF`, `AN`, `AS`, `EU`, `NA`, `OC` or `SA`. `NA` means North America: it is a code, not a missing value | `AS` |
| `iso_country` | Two-letter country code | `IN` |
| `iso_region` | Country and region (state) code | `IN-KA` |
| `municipality` | The town or city it serves | `Bengaluru` |
| `scheduled_service` | `yes` if airlines fly there on a timetable, otherwise `no`. DuckDB reads it as `BOOLEAN` | `yes` |
| `icao_code` | Four-letter ICAO code, often empty | `VOBL` |
| `iata_code` | Three-letter code on luggage tags, often empty | `BLR` |
| `gps_code` | Code used by GPS devices, often empty | `VOBL` |
| `local_code` | National code, often empty | |
| `home_link` | The airport's website, often empty | `http://www.bengaluruairport.com/home/home.jspx` |
| `wikipedia_link` | Its Wikipedia article, often empty | `https://en.wikipedia.org/wiki/Kempegowda_International_Airport` |
| `keywords` | Other names and search words, often empty | `Bangalore` |

Numbers to check your work on 13 November 2026: 247 countries; India (`IN`) has 630 airports that are not `closed`.

### `CREATE TABLE` for PostgreSQL (map weeks, loading task)

Paste this into psql inside the data lab (`docker exec -it datalab-postgres-1 psql -U de -d de`):

```sql
CREATE TABLE airports (
    id BIGINT,
    ident TEXT PRIMARY KEY,
    type TEXT,
    name TEXT,
    latitude_deg DOUBLE PRECISION,
    longitude_deg DOUBLE PRECISION,
    elevation_ft INTEGER,
    continent TEXT,
    iso_country TEXT,
    iso_region TEXT,
    municipality TEXT,
    scheduled_service TEXT,
    icao_code TEXT,
    iata_code TEXT,
    gps_code TEXT,
    local_code TEXT,
    home_link TEXT,
    wikipedia_link TEXT,
    keywords TEXT
);
```

Then copy the file into the container and load it:

```bash
MSYS_NO_PATHCONV=1 docker cp data/airports.csv datalab-postgres-1:/tmp/airports.csv
```

```
\copy airports FROM '/tmp/airports.csv' WITH (FORMAT csv, HEADER true)
```

psql prints `COPY 86351` (on 13 November 2026; the number changes a little each day). The primary key on `ident` is what makes a lookup of one airport fast. Tested on PostgreSQL 16.15 (`pgvector/pgvector:0.8.7-pg16`, the data lab's image).

If psql says the table already exists, you loaded it before: run `DROP TABLE airports;` and start again.

## The live edit stream (Wikimedia EventStreams)

| | |
|---|---|
| Address | `https://stream.wikimedia.org/v2/stream/recentchange` |
| What it sends | One event for every change on every Wikimedia wiki: Wikipedia in every language, Wikidata, Commons and more |
| Format | Server-sent events: text lines, where each `data:` line holds one JSON event |
| Volume on 13 November 2026 | 2,576 events in 60 seconds (about 43 a second): `edit` 1,446, `categorize` 986, `log` 81, `new` 63 |
| Licence | Edit data from Wikimedia projects via EventStreams, CC BY-SA 4.0 |
| Documentation | https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams_HTTP_Service |

### `watch_edits.py`

It reads the stream and prints what arrives. It uses only Python's standard library, so there is nothing to install.

```bash
uv run python ~/de-kit/data/map/watch_edits.py                       # 60 seconds, one line per event
uv run python ~/de-kit/data/map/watch_edits.py --seconds 60 --save data/edits.jsonl
uv run python ~/de-kit/data/map/watch_edits.py --seconds 30 --quiet --save data/edits.jsonl
```

| Option | What it does |
|---|---|
| `--seconds N` | Stop after N seconds (default 60) |
| `--save PATH` | Append every event, unchanged, to PATH: one complete JSON object per line ("JSON lines"). The folder is made if it is missing |
| `--quiet` | Print only the 10-second totals and the summary, not one line per event |

What you see (a real `--quiet` run on 13 November 2026):

```
Listening to https://stream.wikimedia.org/v2/stream/recentchange for 60 s ...
total after 10 s: 377 events (edit 216, categorize 144, new 11, log 6)
total after 20 s: 811 events (edit 446, categorize 322, new 22, log 21)
total after 30 s: 1226 events (edit 677, categorize 475, log 41, new 33)
total after 40 s: 1678 events (edit 940, categorize 639, log 57, new 42)
total after 50 s: 2156 events (edit 1201, categorize 833, log 70, new 52)
total after 60 s: 2576 events (edit 1446, categorize 986, log 81, new 63)

Summary (time is up):
  events counted: 2576 events (edit 1446, categorize 986, log 81, new 63)
  seconds: 60
  saved to: data/edits.jsonl
  largest delay between an edit and its arrival: 27.9 s (edit on en.wiktionary.org)
```

Without `--quiet`, each event also gets one line: the time it arrived (your laptop's clock), the wiki, the type and the page title, for example `02:04:20  tr.wikipedia.org         edit       Ayesha A. Malik`.

Notes:
- **The delay** is the time the event reached you minus the time of the change (the event's `timestamp`). Most events arrive within a few seconds; some arrive much later.
- **Saved files are safe to read**: the script writes whole lines only, so `duckdb -c "SELECT count(*) FROM read_json('data/edits.jsonl')"` never sees half an event. On 13 November 2026 that count matched the summary exactly (2,576). `--save` adds to an existing file: delete it first for a fresh count.
- **Ctrl+C** stops early. The summary still prints, and every event saved so far stays in the file.
- **Test events**: Wikimedia sends a few test events with `meta.domain` set to `canary`. The script skips them; they are neither counted nor saved.
- **Long connections**: the server closes a connection after about 15 minutes. The script then reconnects and resumes from the last event it received (the `Last-Event-ID` header). In a 60-second run you will not see this.
- **Titles in every script** (Thai, Arabic, Hindi and more) print safely on Windows: the script switches its output to UTF-8.

### Polite use

- Open one connection at a time. Do not run several copies of the script at once.
- The script sends a User-Agent that names the course kit, as Wikimedia's User-Agent policy asks: https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
- Read for a minute or two, not for hours. EventStreams is meant for small tools, not for copying all of Wikipedia's changes.

### Personal data in the stream

Events name real people: the `user` field holds the editor's username, and titles of user pages (namespaces 2 and 3) contain usernames. Most editors who are not logged in appear as temporary accounts whose names start with `~` (52 of the 1,242 non-bot events in the run above). Treat these fields as personal data: never commit `data/edits.jsonl`, usernames, comments or user-page titles. Your course repository ignores `data/` folders.
