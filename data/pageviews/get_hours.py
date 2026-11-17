#!/usr/bin/env python3
"""Download hourly Wikipedia page-view files for PageLake (P5).

Run it from your pagelake/ folder in Git Bash:

    uv run python ~/de-kit/data/pageviews/get_hours.py --start 2026-11-02 --days 7 --out data/raw

You get one file per hour: 7 days give 168 files, named
pageviews-20261102-010000.gz ... pageviews-20261109-000000.gz.
A file is named after the END of the hour it covers (UTC), so the hour
00:00-01:00 on 2 November is pageviews-20261102-010000.gz.

Each file is gzip-compressed text, one line per page and hour:

    domain_code page_title count_views total_response_size
    sv.m Sverige 152 0

Wikimedia's full files are 30-55 MB each (about 7 GB for a week). The course
keeps only six Wikipedias (desktop and mobile): simple, id, ko, nl, sv and vi.
That leaves 1-3 MB for most hours (about 337 MB for the course week).

Two sources:
  --source kit        (default) the course week, already filtered, from the
                      kit's GitHub release. Fast, and kind to Wikimedia.
  --source wikimedia  the real dump files from dumps.wikimedia.org, filtered
                      while they download. Use it for other dates or wikis.
                      It is slow: about 2 minutes per hour of data.

Safe to run twice: files already in --out are skipped, so a stopped
download continues where it stopped. Check your files with --check.

Standard library only, so there is nothing to install.
Page-view data: Wikimedia Foundation, released under CC0 1.0.
"""

import argparse
import gzip
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

# ---- Settings -----------------------------------------------------------
KIT_REPO = "https://github.com/Anaxionai/de-v3-kit"
KIT_RELEASE = KIT_REPO + "/releases/download/pageviews-2026-11"
KIT_WEEK_START = date(2026, 11, 2)  # the kit copy holds 2 to 8 November 2026
KIT_WEEK_DAYS = 7
DUMPS = "https://dumps.wikimedia.org/other/pageviews"
DEFAULT_WIKIS = "simple,id,ko,nl,sv,vi"
USER_AGENT = (f"de-course-kit/1.0 ({KIT_REPO}; data/pageviews/get_hours.py) "
              f"python-urllib/{sys.version_info.major}.{sys.version_info.minor}")
ATTEMPTS = 4  # tries per file before giving up
CHUNK = 1024 * 1024  # read 1 MB at a time


def hour_file_names(start: date, days: int) -> list[str]:
    """The file names for every hour of the days asked for.

    The file for the hour that STARTS at H is named after H + 1 hour.
    """
    first = datetime(start.year, start.month, start.day)
    names = []
    for hour in range(days * 24):
        end_of_hour = first + timedelta(hours=hour + 1)
        names.append(end_of_hour.strftime("pageviews-%Y%m%d-%H0000.gz"))
    return names


def source_url(source: str, name: str) -> str:
    """Where one file is downloaded from."""
    if source == "kit":
        return f"{KIT_RELEASE}/{name}"
    # Wikimedia keeps each file in a folder for its own year and month.
    year, month = name[10:14], name[14:16]
    return f"{DUMPS}/{year}/{year}-{month}/{name}"


def keep_codes(wikis: str) -> set[bytes]:
    """The domain codes to keep: each wiki on desktop (sv) and mobile (sv.m)."""
    codes = set()
    for wiki in wikis.split(","):
        wiki = wiki.strip()
        if wiki:
            codes.add(wiki.encode())
            codes.add(wiki.encode() + b".m")
    return codes


def open_url(url: str):
    """Open url with our User-Agent. The caller reads it and closes it."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request, timeout=60)


def save_kit_file(url: str, part: Path) -> None:
    """Copy one ready-made file from the kit release into part."""
    with open_url(url) as response, part.open("wb") as handle:
        while chunk := response.read(CHUNK):
            handle.write(chunk)


def save_filtered_dump(url: str, part: Path, codes: set[bytes]) -> None:
    """Stream one full Wikimedia file and write only the lines we keep.

    Lines are kept byte for byte, so the file looks like Wikimedia's, only shorter.
    mtime=0 makes the output the same on every run.
    """
    with open_url(url) as response:
        source = gzip.GzipFile(fileobj=response)
        with part.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            for line in source:
                if line.split(b" ", 1)[0] in codes:
                    out.write(line)


def count_lines(path: Path) -> int:
    """Read a .gz file to the end and count its lines (this also proves it is complete)."""
    with gzip.open(path, "rb") as handle:
        return sum(1 for _ in handle)


def fetch_one(source: str, name: str, out_dir: Path, codes: set[bytes]) -> int:
    """Download one file into out_dir, with retries. Returns its line count."""
    url = source_url(source, name)
    target = out_dir / name
    part = out_dir / (name + ".part")  # renamed only when complete
    for attempt in range(1, ATTEMPTS + 1):
        try:
            if source == "kit":
                save_kit_file(url, part)
            else:
                save_filtered_dump(url, part, codes)
            lines = count_lines(part)
            part.replace(target)
            return lines
        except urllib.error.HTTPError as problem:
            part.unlink(missing_ok=True)
            if problem.code == 404:
                if source == "kit":
                    sys.exit(f"\nNot found: {url}\nThe kit copy is not published yet. "
                             "Tell your mentor, or add --source wikimedia (slow).")
                sys.exit(f"\nNot found: {url}\nWikimedia has not published this hour yet, "
                         "or the date is wrong. Files appear about an hour after the hour ends.")
            reason = f"HTTP {problem.code}"
        except (urllib.error.URLError, TimeoutError, OSError, EOFError, gzip.BadGzipFile) as problem:
            part.unlink(missing_ok=True)
            reason = str(problem)
        if attempt < ATTEMPTS:
            wait = 10 * 2 ** (attempt - 1)  # 10, 20, 40 seconds
            print(f"  {name}: {reason}; trying again in {wait} s ({attempt}/{ATTEMPTS})", flush=True)
            time.sleep(wait)
    sys.exit(f"\nGave up on {name} after {ATTEMPTS} tries. Check your internet connection "
             "and run the same command again: finished files are kept.")


def check_files(names: list[str], out_dir: Path, codes: set[bytes]) -> int:
    """--check: every file is there, complete, has 4 fields per line and only our wikis."""
    problems = 0
    total_lines = 0
    for name in names:
        path = out_dir / name
        if not path.exists():
            print(f"MISSING  {name}")
            problems += 1
            continue
        number = 0
        try:
            with gzip.open(path, "rb") as handle:
                for number, line in enumerate(handle, start=1):
                    fields = line.rstrip(b"\n").split(b" ")
                    if len(fields) != 4 or fields[0] not in codes:
                        print(f"BAD LINE {name} line {number}: {line[:80]!r}")
                        problems += 1
                        break
                total_lines += number
        except (OSError, EOFError) as problem:
            print(f"BROKEN   {name}: {problem} (delete it and download again)")
            problems += 1
    leftovers = sorted(out_dir.glob("*.part"))
    for part in leftovers:
        print(f"LEFTOVER {part.name} (an unfinished download; it is safe to delete)")
    if problems:
        print(f"Check failed: {problems} problem(s) in {len(names)} files.")
        return 1
    print(f"Check OK: {len(names)} files, {total_lines:,} lines, all complete.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download hourly Wikipedia page-view files (one .gz per hour, UTC).")
    parser.add_argument("--start", required=True, type=date.fromisoformat,
                        help="first day, YYYY-MM-DD (UTC), for example 2026-11-02")
    parser.add_argument("--days", type=int, default=1, help="number of days (default: 1)")
    parser.add_argument("--out", default="data/raw", help="folder for the files (default: data/raw)")
    parser.add_argument("--wikis", default=DEFAULT_WIKIS,
                        help=f"comma list of Wikipedia codes to keep (default: {DEFAULT_WIKIS})")
    parser.add_argument("--source", choices=["kit", "wikimedia"], default="kit",
                        help="kit: the filtered course week (default); wikimedia: the full dumps, filtered here")
    parser.add_argument("--check", action="store_true",
                        help="download nothing; check the files already in --out")
    args = parser.parse_args(argv)

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.days < 1:
        parser.error("--days must be 1 or more")
    codes = keep_codes(args.wikis)
    if not codes:
        parser.error("--wikis needs at least one code, for example sv")
    names = hour_file_names(args.start, args.days)
    out_dir = Path(args.out)

    if args.check:
        return check_files(names, out_dir, codes)

    if args.source == "kit":
        week_end = KIT_WEEK_START + timedelta(days=KIT_WEEK_DAYS - 1)
        last_day = args.start + timedelta(days=args.days - 1)
        if args.start < KIT_WEEK_START or last_day > week_end or codes != keep_codes(DEFAULT_WIKIS):
            parser.error(f"the kit copy holds only {KIT_WEEK_START} to {week_end} for the wikis "
                         f"{DEFAULT_WIKIS}. Add --source wikimedia for other dates or wikis.")

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{len(names)} hourly files from {args.source} into {out_dir.as_posix()}/", flush=True)
    fetched = skipped = 0
    for name in names:
        target = out_dir / name
        if target.exists():
            skipped += 1
            print(f"{name}  already there, skipped", flush=True)
            continue
        started = time.monotonic()
        lines = fetch_one(args.source, name, out_dir, codes)
        size_mb = target.stat().st_size / 1_000_000
        seconds = time.monotonic() - started
        fetched += 1
        print(f"{name}  {lines:>9,} lines  {size_mb:5.2f} MB  {seconds:5.1f} s", flush=True)
        if args.source == "wikimedia":
            time.sleep(1)  # a short pause between big downloads, to be polite

    total_mb = sum((out_dir / name).stat().st_size for name in names) / 1_000_000
    print(f"Done: {len(names)} files in {out_dir.as_posix()}/ "
          f"({fetched} downloaded, {skipped} already there), {total_mb:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
