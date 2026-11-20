#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Download the UCI "Online Retail II" workbook and save it as one CSV file, for RetailBase (P3).

Run it inside your retailbase/ folder in Git Bash (about 3 minutes):

    uv run ~/de-kit/data/retail/get_retail.py --out data

The lines at the top of this file (between "# /// script" and "# ///") tell uv which Python
and which package (openpyxl, to read Excel files) the script needs. uv builds a separate
environment for it, so your own project's packages are not touched.

It writes <out>/online_retail_II.csv: UTF-8, comma separated, one header line, ten columns.
The first eight columns are the publisher's, unchanged:
    Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
The last two say where each row came from in the workbook:
    Sheet     the worksheet name ("Year 2009-2010" or "Year 2010-2011")
    SheetRow  the row number in that worksheet (row 2 is the first data row)

Slow internet? Download the zip once (a mentor can share it), then:

    uv run ~/de-kit/data/retail/get_retail.py --out data --zip path/to/online+retail+ii.zip

Source: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5CG6D  Licence: CC BY 4.0. README.md in this folder has the details.
"""

import argparse
import csv
import datetime as dt
import io
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
WORKBOOK = "online_retail_II.xlsx"
OUT_NAME = "online_retail_II.csv"
PUBLISHED = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
EXPECTED_ROWS = 1_067_371
USER_AGENT = "de-course-kit/1.0 (data/retail/get_retail.py)"


def text(value) -> str:
    """One cell as text: no '.0' on whole numbers, ISO timestamps, empty for a missing value."""
    if value is None:
        return ""
    if isinstance(value, dt.datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, float):
        # 13085.0 becomes 13085; 6.95 stays 6.95 (repr gives the shortest exact form).
        return str(int(value)) if value == int(value) else repr(value)
    return str(value)


def download(url: str) -> bytes:
    """The zip file as bytes, with a progress line every 10 MB."""
    print(f"Downloading {url} (about 45 MB) ...", flush=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    parts, size, next_report = [], 0, 10
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            while chunk := response.read(1024 * 1024):
                parts.append(chunk)
                size += len(chunk)
                if size >= next_report * 1024 * 1024:
                    print(f"  {next_report} MB", flush=True)
                    next_report += 10
    except urllib.error.HTTPError as problem:
        sys.exit(f"Download failed: the UCI site answered HTTP {problem.code}. "
                 "Try again later, or ask your mentor for the zip and use --zip.")
    except (urllib.error.URLError, TimeoutError, OSError) as problem:
        sys.exit(f"Download failed: could not reach the UCI site ({problem}). "
                 "Check your internet connection, or ask your mentor for the zip and use --zip.")
    return b"".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download Online Retail II and save it as one CSV file.")
    parser.add_argument("--out", default="data", help="folder to write online_retail_II.csv into (default: data)")
    parser.add_argument("--zip", default=None,
                        help="use an already downloaded online+retail+ii.zip instead of downloading")
    args = parser.parse_args(argv)

    if args.zip:
        try:
            blob = Path(args.zip).read_bytes()
        except OSError as problem:
            sys.exit(f"Cannot read the zip file {args.zip}: {problem}")
    else:
        blob = download(URL)

    from openpyxl import load_workbook  # imported here, so that --help works even without openpyxl

    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            workbook = load_workbook(io.BytesIO(archive.read(WORKBOOK)), read_only=True, data_only=True)
    except (zipfile.BadZipFile, KeyError):
        sys.exit(f"The zip file does not hold {WORKBOOK}. Download it again, or ask your mentor.")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / OUT_NAME
    # Write to a .part file first and rename it at the end, so a stopped run never leaves
    # a half-written online_retail_II.csv that looks complete.
    part_path = out_dir / (OUT_NAME + ".part")
    print("Converting the workbook to CSV (about 2 minutes) ...", flush=True)
    total = 0
    with part_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(PUBLISHED + ["Sheet", "SheetRow"])
        for sheet in workbook.worksheets:
            rows = sheet.iter_rows(values_only=True)
            header = [str(h) for h in next(rows)[:8]]
            if header != PUBLISHED:
                handle.close()
                part_path.unlink()
                sys.exit(f"Unexpected columns in sheet {sheet.title!r}: {header}. "
                         "The publisher may have changed the file; tell your mentor.")
            count = 0
            for sheet_row, row in enumerate(rows, start=2):
                writer.writerow([text(v) for v in row[:8]] + [sheet.title, sheet_row])
                count += 1
            print(f"Sheet {sheet.title}: {count:,} rows", flush=True)
            total += count
    workbook.close()
    part_path.replace(out_path)
    print(f"Wrote {out_path.as_posix()}: {total:,} rows, 10 columns")
    if total != EXPECTED_ROWS:
        print(f"WARNING: expected {EXPECTED_ROWS:,} rows. The publisher may have changed the file; tell your mentor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
