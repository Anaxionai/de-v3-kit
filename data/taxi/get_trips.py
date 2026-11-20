#!/usr/bin/env python3
"""Download New York yellow taxi trip files and the zone lookup for TaxiScale (P7).

Run it from your taxiscale/ folder in Git Bash:

    uv run --no-project python ~/de-kit/data/taxi/get_trips.py --months 2024-01 --out data
    uv run --no-project python ~/de-kit/data/taxi/get_trips.py --months 2024-02 2024-03 --out data

It writes:
    <out>/yellow/yellow_tripdata_YYYY-MM.parquet   one Parquet file per month (about 50-60 MB)
    <out>/zones/taxi_zone_lookup.csv               the 265 taxi zones (12 KB)

The files come from the NYC Taxi and Limousine Commission (TLC):
    https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet
    https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

Safe to run twice. A file that is already there is skipped. A file is saved
under a .part name and renamed only when it is complete, so a stopped
download never looks finished: run the same command again to finish it.
Check your files with --check.

Standard library only, so there is nothing to install.
Data: NYC Taxi and Limousine Commission (TLC) Trip Record Data.
"""

import argparse
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ---- Settings -----------------------------------------------------------
BASE_URL = "https://d37ci6vzurychx.cloudfront.net"
USER_AGENT = "de-course-kit/1.0 (data/taxi/get_trips.py)"
ATTEMPTS = 4  # tries per file before giving up
CHUNK = 1024 * 1024  # read 1 MB at a time
ZONE_ROWS = 265  # rows in the zone lookup, not counting the header
FIRST_MONTH = "2009-01"  # the oldest yellow taxi file TLC publishes


def check_month(text: str) -> str:
    """Accept YYYY-MM (for example 2024-01) and return it unchanged."""
    parts = text.split("-")
    if len(parts) != 2 or len(parts[0]) != 4 or len(parts[1]) != 2 or not (parts[0] + parts[1]).isdigit():
        raise argparse.ArgumentTypeError(f"months look like 2024-01, not {text!r}")
    if not 1 <= int(parts[1]) <= 12 or text < FIRST_MONTH:
        raise argparse.ArgumentTypeError(f"{text} is not a month TLC has data for")
    return text


def size_text(size: int) -> str:
    """Bytes as text a person reads: 50.0 MB, or 12 KB for a small file."""
    return f"{size / 1_000_000:.1f} MB" if size >= 1_000_000 else f"{size / 1000:.0f} KB"


def trip_file(month: str) -> tuple[str, str]:
    """The address of one month's file and where it goes under --out."""
    name = f"yellow_tripdata_{month}.parquet"
    return f"{BASE_URL}/trip-data/{name}", f"yellow/{name}"


def zone_file() -> tuple[str, str]:
    """The address of the zone lookup and where it goes under --out."""
    return f"{BASE_URL}/misc/taxi_zone_lookup.csv", "zones/taxi_zone_lookup.csv"


def download(url: str, part: Path) -> int:
    """Copy url into part, 1 MB at a time. Returns the number of bytes saved."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    saved = 0
    with urllib.request.urlopen(request, timeout=60) as response, part.open("wb") as handle:
        expected = response.headers.get("Content-Length")
        while chunk := response.read(CHUNK):
            handle.write(chunk)
            saved += len(chunk)
    if expected and saved != int(expected):
        raise OSError(f"stopped early: {saved:,} of {int(expected):,} bytes")
    return saved


def fetch_one(url: str, target: Path) -> str:
    """Download one file to target. Returns "saved", "skipped" or "missing"."""
    if target.exists():
        print(f"{target.as_posix()}  already there, skipped", flush=True)
        return "skipped"
    target.parent.mkdir(parents=True, exist_ok=True)
    part = target.with_name(target.name + ".part")
    for attempt in range(1, ATTEMPTS + 1):
        try:
            started = time.monotonic()
            saved = download(url, part)
            part.replace(target)
            seconds = time.monotonic() - started
            print(f"{target.as_posix()}  {size_text(saved)}  saved in {seconds:.0f} s", flush=True)
            return "saved"
        except urllib.error.HTTPError as problem:
            part.unlink(missing_ok=True)
            # TLC's server answers 403 (not 404) for a month it has not published.
            if problem.code in (403, 404):
                print(f"{target.as_posix()}  NOT FOUND: {url} (HTTP {problem.code}). "
                      "TLC publishes each month about two months late; check the month.", flush=True)
                return "missing"
            reason = f"HTTP {problem.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as problem:
            part.unlink(missing_ok=True)
            reason = str(problem)
        if attempt < ATTEMPTS:
            wait = 10 * 2 ** (attempt - 1)  # 10, 20, 40 seconds
            print(f"  {reason}; trying again in {wait} s ({attempt}/{ATTEMPTS})", flush=True)
            time.sleep(wait)
    print(f"{target.as_posix()}  GAVE UP after {ATTEMPTS} tries. Run the same command again later.", flush=True)
    return "missing"


def check_parquet(path: Path) -> str | None:
    """A complete Parquet file starts and ends with the 4 bytes PAR1. Returns a problem or None."""
    size = path.stat().st_size
    if size < 12:
        return "too small to be a Parquet file"
    with path.open("rb") as handle:
        head = handle.read(4)
        handle.seek(size - 4)
        tail = handle.read(4)
    if head != b"PAR1" or tail != b"PAR1":
        return "not a complete Parquet file"
    return None


def check_zones(path: Path) -> str | None:
    """The zone lookup has a header and 265 rows. Returns a problem or None."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].replace('"', "") != "LocationID,Borough,Zone,service_zone":
        return "the first line is not LocationID,Borough,Zone,service_zone"
    if len(lines) - 1 != ZONE_ROWS:
        return f"{len(lines) - 1} rows, expected {ZONE_ROWS}"
    return None


def check_files(months: list[str], out_dir: Path) -> int:
    """--check: every file is there and complete."""
    problems = 0
    targets = [out_dir / trip_file(month)[1] for month in months] + [out_dir / zone_file()[1]]
    for target in targets:
        if not target.exists():
            print(f"{target.as_posix()}  MISSING")
            problems += 1
            continue
        problem = check_zones(target) if target.suffix == ".csv" else check_parquet(target)
        if problem:
            print(f"{target.as_posix()}  BROKEN: {problem}. Delete it and run the download again.")
            problems += 1
        else:
            print(f"{target.as_posix()}  OK  {size_text(target.stat().st_size)}")
    for part in sorted(out_dir.glob("*/*.part")):
        print(f"{part.as_posix()} is an unfinished download; it is safe to delete.")
    if problems:
        print(f"Check failed: {problems} of {len(targets)} files missing or broken.")
        return 1
    print(f"Check OK: {len(targets)} files.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download NYC yellow taxi trip files (one Parquet file per month) and the zone lookup.")
    parser.add_argument("--months", nargs="+", required=True, type=check_month, metavar="YYYY-MM",
                        help="one or more months, space-separated, for example 2024-02 2024-03")
    parser.add_argument("--out", default="data", help="folder for the files (default: data)")
    parser.add_argument("--check", action="store_true",
                        help="download nothing; check the files already in --out")
    args = parser.parse_args(argv)
    months = sorted(set(args.months))
    out_dir = Path(args.out)

    if args.check:
        return check_files(months, out_dir)

    print(f"{len(months)} month(s) and the zone lookup into {out_dir.as_posix()}/", flush=True)
    results = {"saved": 0, "skipped": 0, "missing": 0}
    for url, relative in [trip_file(month) for month in months] + [zone_file()]:
        results[fetch_one(url, out_dir / relative)] += 1

    print(f"Done: {results['saved']} downloaded, {results['skipped']} already there, "
          f"{results['missing']} missing.")
    if results["missing"]:
        print(f"{results['missing']} file(s) missing. Fix the month, or run the same command again; "
              "finished files are kept.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
