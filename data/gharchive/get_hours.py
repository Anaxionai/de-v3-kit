#!/usr/bin/env python3
"""Download hourly GitHub event files from GH Archive for GitPulse (P9).

Run it from your gitpulse/ folder in Git Bash:

    uv run python ~/de-kit/data/gharchive/get_hours.py --date 2018-01-01 --hours 0-23 --out data/gharchive

GH Archive keeps one file per hour (UTC). The address of one file is

    https://data.gharchive.org/YYYY-MM-DD-H.json.gz

where H is the hour with no leading zero: 0, 1, ... 23.
Each file is gzip-compressed JSON, one GitHub event per line.
The files keep their GH Archive names, still gzipped: 2018-01-01-0.json.gz.

Options:
  --date   the day, YYYY-MM-DD (required)
  --hours  one hour (5) or a range (0-23); default 0-23
  --out    the folder for the files; default data/gharchive (made if missing)
  --check  download nothing: read every file to the end and count its events

Safe to run twice. A file that is already there with the right size is
skipped. A file is saved under a .part name and renamed only when it is
complete, so a stopped download never looks finished.

Standard library only, so there is nothing to install.
Data: GH Archive (https://www.gharchive.org), a record of GitHub's public events.
"""

import argparse
import gzip
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

# ---- Settings -----------------------------------------------------------
BASE_URL = "https://data.gharchive.org"
USER_AGENT = "de-course-kit/1.0 (data/gharchive/get_hours.py)"
ATTEMPTS = 4  # tries per file before moving on
CHUNK = 1024 * 1024  # read 1 MB at a time
PAUSE_SECONDS = 1  # a short pause between files, to be polite


def parse_hours(text: str) -> list[int]:
    """Turn "5" into [5] and "0-23" into [0, 1, ..., 23]."""
    if "-" in text:
        first, last = text.split("-", 1)
        start, end = int(first), int(last)
    else:
        start = end = int(text)
    if not (0 <= start <= end <= 23):
        raise ValueError(f"hours must be between 0 and 23, low to high: {text}")
    return list(range(start, end + 1))


def file_name(day: date, hour: int) -> str:
    """GH Archive's name for one hour: no leading zero on the hour."""
    return f"{day.isoformat()}-{hour}.json.gz"


def open_url(url: str, method: str = "GET"):
    """Open url with our User-Agent. The caller reads it and closes it."""
    request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request, timeout=60)


def remote_size(url: str) -> int | None:
    """The size in bytes that GH Archive reports for a file, or None if unknown."""
    with open_url(url, method="HEAD") as response:
        length = response.headers.get("Content-Length")
    return int(length) if length else None


def download(url: str, part: Path) -> int:
    """Copy url into part, 1 MB at a time. Returns the number of bytes saved."""
    saved = 0
    with open_url(url) as response, part.open("wb") as handle:
        expected = response.headers.get("Content-Length")
        while chunk := response.read(CHUNK):
            handle.write(chunk)
            saved += len(chunk)
    if expected and saved != int(expected):
        raise OSError(f"stopped early: {saved:,} of {int(expected):,} bytes")
    return saved


def fetch_one(name: str, out_dir: Path) -> str:
    """Download one hour. Returns "saved", "skipped", "not found" or "failed"."""
    url = f"{BASE_URL}/{name}"
    target = out_dir / name
    part = out_dir / (name + ".part")
    for attempt in range(1, ATTEMPTS + 1):
        try:
            if target.exists():
                size = remote_size(url)
                if size is None or target.stat().st_size == size:
                    print(f"{name:<24} {target.stat().st_size / 1_000_000:6.1f} MB  already there, skipped",
                          flush=True)
                    return "skipped"
                print(f"{name:<24} wrong size on disk, downloading again", flush=True)
            started = time.monotonic()
            saved = download(url, part)
            part.replace(target)
            seconds = time.monotonic() - started
            print(f"{name:<24} {saved / 1_000_000:6.1f} MB  saved in {seconds:.0f} s", flush=True)
            return "saved"
        except urllib.error.HTTPError as problem:
            part.unlink(missing_ok=True)
            if problem.code == 404:
                print(f"{name:<24} NOT FOUND on GH Archive ({url}). "
                      "Check the date and the hour.", flush=True)
                return "not found"
            reason = f"HTTP {problem.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as problem:
            part.unlink(missing_ok=True)
            reason = str(problem)
        if attempt < ATTEMPTS:
            wait = 10 * 2 ** (attempt - 1)  # 10, 20, 40 seconds
            print(f"{name:<24} {reason}; trying again in {wait} s ({attempt}/{ATTEMPTS})", flush=True)
            time.sleep(wait)
    print(f"{name:<24} GAVE UP after {ATTEMPTS} tries.", flush=True)
    return "failed"


def check_files(names: list[str], out_dir: Path) -> int:
    """--check: each file is there, unzips to the end, and its first line is a JSON event."""
    problems = 0
    total = 0
    for name in names:
        path = out_dir / name
        if not path.exists():
            print(f"{name:<24} MISSING")
            problems += 1
            continue
        try:
            with gzip.open(path, "rb") as handle:
                first = json.loads(handle.readline())
                events = 1 + sum(1 for _ in handle)
            if "type" not in first or "created_at" not in first:
                raise ValueError("the first line is not a GitHub event")
        except (OSError, EOFError, ValueError) as problem:
            print(f"{name:<24} BROKEN: {problem}. "
                  "Run the download again: it replaces a file whose size is wrong.")
            problems += 1
            continue
        total += events
        print(f"{name:<24} {path.stat().st_size / 1_000_000:6.1f} MB  {events:>8,} events")
    for part in sorted(out_dir.glob("*.part")):
        print(f"{part.name} is an unfinished download; it is safe to delete.")
    if problems:
        print(f"Check failed: {problems} of {len(names)} files missing or broken.")
        return 1
    print(f"Check OK: {len(names)} files, {total:,} events.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download hourly GitHub event files (one .json.gz per UTC hour) from GH Archive.")
    parser.add_argument("--date", required=True, type=date.fromisoformat,
                        help="the day, YYYY-MM-DD, for example 2018-01-01")
    parser.add_argument("--hours", default="0-23",
                        help="one hour such as 3, or a range such as 0-23 (default: 0-23)")
    parser.add_argument("--out", default="data/gharchive",
                        help="folder for the files (default: data/gharchive)")
    parser.add_argument("--check", action="store_true",
                        help="download nothing; check the files already in --out and count events")
    args = parser.parse_args(argv)

    try:
        hours = parse_hours(args.hours)
    except ValueError as problem:
        parser.error(str(problem))
    names = [file_name(args.date, hour) for hour in hours]
    out_dir = Path(args.out)

    if args.check:
        return check_files(names, out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{len(names)} hourly files for {args.date} into {out_dir.as_posix()}/", flush=True)
    results = {"saved": 0, "skipped": 0, "not found": 0, "failed": 0}
    for number, name in enumerate(names):
        result = fetch_one(name, out_dir)
        results[result] += 1
        if result == "saved" and number < len(names) - 1:
            time.sleep(PAUSE_SECONDS)

    on_disk = [out_dir / name for name in names if (out_dir / name).exists()]
    total_mb = sum(path.stat().st_size for path in on_disk) / 1_000_000
    missing = results["not found"] + results["failed"]
    print(f"Total: {len(on_disk)} of {len(names)} files, {total_mb:.1f} MB "
          f"({results['saved']} downloaded, {results['skipped']} already there, {missing} missing)")
    if results["failed"]:
        print(f"{results['failed']} download(s) failed. Check your internet connection and run the same "
              "command again; finished files are kept.")
    if results["not found"]:
        print(f"{results['not found']} hour(s) do not exist on GH Archive. Check --date and --hours.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
