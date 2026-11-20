# /// script
# requires-python = ">=3.12"
# dependencies = ["psycopg[binary]"]
# ///
"""Change the stations in the station database, so there is something to load (ClearAir, P4).

Start the database first (in ~/de-kit/data/airquality/stationdb: docker compose up -d), then:

    uv run ~/de-kit/data/airquality/stationdb/change_stations.py --student <your-id> --reset
    uv run ~/de-kit/data/airquality/stationdb/change_stations.py --student <your-id>

--reset   empties the stations table and adds exactly 400 made-up stations (ids 1-400).
          Their updated_at times are spread over the last 180 days, and the two
          newest stations share the same time.
no flag   applies one change batch: updates 10 stations, adds 5 new ones and
          deletes 3 others. Each run makes a different batch.

<your-id> is your GitHub username in lower case. It picks the random numbers, so your
data differs from your classmates' data but is the same every time you reset.

uv installs psycopg (the PostgreSQL driver) for this script by itself: the lines at the
top of this file tell it to. Every name in the data is made up.
"""

import argparse
import os
import random
import sys
from datetime import UTC, date, datetime, timedelta

import psycopg

DEFAULT_URL = "postgresql://source:source@localhost:5433/stationdb"
STATIONS_AT_RESET = 400
UPDATES, ADDS, DELETES = 10, 5, 3

# Made-up cities with a made-up but plausible place on the map (latitude, longitude).
CITIES = {
    "Ashford Vale": (51.21, -1.48), "Brookhaven": (40.82, -73.11), "Cedar Falls": (42.53, -92.44),
    "Clearwater Bay": (-33.86, 151.07), "Eastmoor": (53.48, -2.23), "Fairview": (-1.29, 36.82),
    "Glenmore": (55.86, -4.25), "Harbour Point": (1.29, 103.85), "Highfield": (-26.20, 28.04),
    "Kingsport": (36.55, -82.56), "Lakeside": (43.65, -79.38), "Maple Ridge": (49.22, -122.60),
    "Millbrook": (-37.81, 144.96), "Northgate": (59.33, 18.07), "Oakdale": (37.77, -120.85),
    "Pine Hill": (35.68, 139.69), "Redcliff": (-31.95, 115.86), "Riverton": (12.97, 77.59),
    "Rosewood": (19.43, -99.13), "Silver Bay": (-22.91, -43.17), "Southport": (30.04, 31.24),
    "Stonebridge": (48.86, 2.35), "Summerton": (25.20, 55.27), "Westbrook": (28.61, 77.21),
}
PLACES = ["Market Square", "Central Park", "Bus Station", "Old Town", "River Road", "Hill Top",
          "Harbour", "School Lane", "Hospital", "Industrial Estate", "University", "North Gate",
          "East End", "West End", "Airport Road", "Stadium", "Library", "Bridge Street",
          "Garden City", "Railway Yard"]
OPERATORS = ["City Air Office", "Regional Environment Agency", "Clean Air Trust",
             "University Air Lab", "Harbour Authority", "National Weather Service"]


def connect(url):
    """Open a connection, or stop with a message that says how to start the database."""
    try:
        return psycopg.connect(url, connect_timeout=5, autocommit=True)
    except psycopg.OperationalError as problem:
        sys.exit(f"Cannot connect to the station database ({url}).\n"
                 "Start it: cd ~/de-kit/data/airquality/stationdb && docker compose up -d\n"
                 "then wait until 'docker compose ps' shows (healthy).\n"
                 f"Details: {str(problem).strip()}")


def new_station(rng, station_id):
    """One made-up station: (station_id, name, city, latitude, longitude, operator, status, installed_on)."""
    city = rng.choice(sorted(CITIES))
    lat, lon = CITIES[city]
    return (station_id,
            f"{city} {rng.choice(PLACES)}",
            city,
            round(lat + rng.uniform(-0.15, 0.15), 5),
            round(lon + rng.uniform(-0.15, 0.15), 5),
            rng.choice(OPERATORS),
            "maintenance" if rng.random() < 0.08 else "active",
            date(2015, 1, 1) + timedelta(days=rng.randrange(4018)))  # 2015 to 2025


def reset(conn, student):
    """Empty the table and add 400 stations. Returns the newest updated_at."""
    rng = random.Random(f"{student}:reset")
    now = datetime.now(UTC)
    newest = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    rows = []
    for station_id in range(1, STATIONS_AT_RESET + 1):
        updated_at = newest - timedelta(seconds=rng.randrange(1, 180 * 24 * 3600))
        rows.append(new_station(rng, station_id) + (updated_at,))
    # Exactly two stations share the newest time, so a ">=" incremental read shows a boundary row.
    for index in rng.sample(range(STATIONS_AT_RESET), 2):
        rows[index] = rows[index][:-1] + (newest,)
    with conn.transaction():
        conn.execute("TRUNCATE stations")
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO stations (station_id, name, city, latitude, longitude, operator, "
                            "status, installed_on, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            rows)
    return newest


def apply_batch(conn, student):
    """Update 10 stations, add 5 and delete 3. Returns (batch number, updated, added, deleted, total)."""
    ids = [row[0] for row in conn.execute("SELECT station_id FROM stations ORDER BY station_id")]
    if len(ids) < UPDATES + DELETES + 1:
        sys.exit("The stations table is (almost) empty. Run this script with --reset first.")
    highest = ids[-1]
    # The highest id is never deleted, so new ids always go above every id used before.
    batch = (highest - STATIONS_AT_RESET) // ADDS + 1
    rng = random.Random(f"{student}:batch:{batch}")

    updated = sorted(rng.sample(ids, UPDATES))
    added = list(range(highest + 1, highest + ADDS + 1))
    can_delete = [i for i in ids if i not in updated and i != highest]
    deleted = sorted(rng.sample(can_delete, DELETES))

    with conn.transaction():
        for station_id in updated:
            if rng.random() < 0.5:
                # A station goes into maintenance, or comes back.
                conn.execute("UPDATE stations SET status = CASE status WHEN 'active' THEN 'maintenance' "
                             "ELSE 'active' END WHERE station_id = %s", (station_id,))
            else:
                conn.execute("UPDATE stations SET operator = %s WHERE station_id = %s",
                             (rng.choice(OPERATORS), station_id))
        for station_id in added:
            # updated_at is left out, so it gets its default: the time of the insert.
            conn.execute("INSERT INTO stations (station_id, name, city, latitude, longitude, operator, "
                         "status, installed_on) VALUES (%s, %s, %s, %s, %s, %s, 'active', %s)",
                         new_station(rng, station_id)[:6] + (date.today(),))
        conn.execute("DELETE FROM stations WHERE station_id = ANY(%s)", (deleted,))
    total = conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
    return batch, updated, added, deleted, total


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reset or change the stations in the station database.")
    parser.add_argument("--student", required=True, help="your id: your GitHub username in lower case")
    parser.add_argument("--reset", action="store_true", help="empty the table and add 400 stations")
    parser.add_argument("--url", default=os.environ.get("STATIONDB_URL", DEFAULT_URL),
                        help=f"database address (default: $STATIONDB_URL or {DEFAULT_URL})")
    args = parser.parse_args(argv)
    student = args.student.strip().lower()

    with connect(args.url) as conn:
        if args.reset:
            newest = reset(conn, student)
            total = conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
            print(f"reset: {total} stations, newest updated_at {newest:%Y-%m-%d %H:%M:%S}+00 "
                  "(2 stations share it)")
        else:
            batch, updated, added, deleted, total = apply_batch(conn, student)
            print(f"batch {batch}: updated {len(updated)} (ids {', '.join(map(str, updated))}), "
                  f"added {len(added)} (ids {added[0]}-{added[-1]}), "
                  f"deleted {len(deleted)} (ids {', '.join(map(str, deleted))}); stations now {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
