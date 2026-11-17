#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Download every IPL (or WPL) match from Cricsheet as JSON files, for Scorebook (P2).

Run it inside your scorebook/ folder in Git Bash:

    uv run python ~/de-kit/data/ipl/get_matches.py --out data/matches
    uv run python ~/de-kit/data/ipl/get_matches.py --league wpl --out data/wpl

It downloads https://cricsheet.org/downloads/<league>_json.zip (about 5 MB for
the IPL), and saves into one flat folder:
  - one file per match, named <match_id>.json, for example 980987.json
  - README.txt, Cricsheet's list of the matches in the archive
  - LICENSE.txt, the data licence
No zip file is left behind. A second run replaces the files.

The script uses only the Python standard library, so there is nothing to install.

Match data from Cricsheet (https://cricsheet.org/), licensed under the
Open Data Commons Attribution License 1.0 (https://opendatacommons.org/licenses/by/1-0/).
"""

import argparse
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ADDRESS = "https://cricsheet.org/downloads/{league}_json.zip"
USER_AGENT = "de-course-kit/1.0 (data/ipl/get_matches.py)"
MATCH_FILE = re.compile(r"^\d+\.json$")  # Cricsheet names each match <match_id>.json
EXTRA_FILES = ("README.txt", "LICENSE.txt")


def download(url: str, target: Path) -> None:
    """Save the file at url into target. Exit with a clear message if the download fails."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as handle:
            while chunk := response.read(1024 * 1024):
                handle.write(chunk)
    except urllib.error.HTTPError as problem:
        sys.exit(f"Download failed: {url} answered HTTP {problem.code}. Try again later.")
    except (urllib.error.URLError, TimeoutError, OSError) as problem:
        sys.exit(f"Download failed: could not reach {url} ({problem}). Check your internet connection.")


def extract(archive_path: Path, out_dir: Path) -> list[str]:
    """Copy the match files, README.txt and LICENSE.txt out of the zip into out_dir.

    The zip is downloaded data, so we never trust the paths inside it: each file is
    written under its base name only, straight into out_dir.
    Returns the names of the match files that were saved.
    """
    saved = []
    try:
        archive = zipfile.ZipFile(archive_path)
    except zipfile.BadZipFile:
        sys.exit("Download failed: the file is not a zip archive. Try again later.")
    with archive:
        for member in archive.infolist():
            name = member.filename.replace("\\", "/").split("/")[-1]  # base name only
            if member.is_dir() or not (MATCH_FILE.match(name) or name in EXTRA_FILES):
                continue
            (out_dir / name).write_bytes(archive.read(member))
            if MATCH_FILE.match(name):
                saved.append(name)
    return saved


def archive_count(readme: Path) -> int | None:
    """The number in README.txt's sentence 'This archive contains 1243 ... matches.'

    The sentence is split over two lines in the file, so the pattern allows any spaces or line breaks.
    """
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8", errors="replace")
    found = re.search(r"This\s+archive\s+contains\s+(\d+)", text)
    return int(found.group(1)) if found else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download every match of one league from Cricsheet as JSON files into one folder.")
    parser.add_argument("--out", default="data/matches",
                        help="folder to save the match files in (default: data/matches)")
    parser.add_argument("--league", choices=["ipl", "wpl"], default="ipl",
                        help="ipl for the Indian Premier League, wpl for the Women's Premier League (default: ipl)")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    before = {path.name for path in out_dir.glob("*.json")}

    # Download into a temporary file that is deleted at the end, so no zip stays behind.
    with tempfile.TemporaryDirectory() as scratch:
        archive_path = Path(scratch) / f"{args.league}_json.zip"
        download(ADDRESS.format(league=args.league), archive_path)
        saved = extract(archive_path, out_dir)

    if not saved:
        sys.exit("The archive held no match files. Cricsheet may have changed its downloads; tell your mentor.")

    print(f"Saved {len(saved)} match files to {out_dir.as_posix()}")

    # Two checks that save you an hour later. They print only when something is wrong.
    expected = archive_count(out_dir / "README.txt")
    if expected is not None and expected != len(saved):
        print(f"WARNING: README.txt says the archive contains {expected} matches, but {len(saved)} were saved.")
    others = before - set(saved)
    if others:
        print(f"WARNING: {len(others)} other .json files in {out_dir.as_posix()} are not in this archive "
              f"(another league?). Keep one league per folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
