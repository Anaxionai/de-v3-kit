#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Download one month of daily wholesale market prices from data.gov.in as raw CSV files.

This is the raw data for PriceWatch (P1). Run it from your pricewatch/ folder in Git Bash:

    export DATA_GOV_IN_KEY=<your key>
    uv run python ~/de-kit/data/prices/get_prices.py --month 2026-10

It writes into ~/de-kit/data/prices/downloads/2026-10/:
  - one file per calendar day, prices-YYYY-MM-DD.csv, with the 11 columns of the source;
    a day with no reports (most Sundays and holidays) still gets a file with the header only;
  - source.json, which names the dataset, its licence, the price unit and every file with its row count.

The values are saved exactly as the API sends them. Nothing is cleaned: that is your job in PriceWatch.
Prices are rupees per quintal (1 quintal = 100 kg).

Test your key first, without downloading a month (it makes a few small requests):

    uv run python ~/de-kit/data/prices/get_prices.py --check

The script uses only the Python standard library, so there is nothing to install.
README.md in this folder explains the key, the columns and what is messy in this data.
"""

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# The dataset: "Variety-wise Daily Market Prices Data of Commodity" on data.gov.in.
RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"
API = "https://api.data.gov.in/resource/"
KEY_VARIABLE = "DATA_GOV_IN_KEY"

# The 11 columns, in the order the source publishes them. Every file gets exactly this header.
HEADER = ["State", "District", "Market", "Commodity", "Variety", "Grade", "Arrival_Date",
          "Min_Price", "Max_Price", "Modal_Price", "Commodity_Code"]
DATE_LAYOUT = "%d/%m/%Y"  # Arrival_Date looks like 01/10/2026 (day/month/year)
DEFAULT_COMMODITIES = ["Tomato", "Onion", "Potato", "Brinjal", "Coriander(Leaves)"]

# The API filters by field name. These names come from the dataset page.
DATE_FILTER = "Arrival_Date"
COMMODITY_FILTER = "Commodity"
STATE_FILTER = "State"

PAGE_SIZE = 1000          # rows asked for in one request; the script keeps asking until it has them all
PAUSE_SECONDS = 0.5       # wait between two requests, to be polite to the server
MAX_PAGES = 200           # a safety stop for one commodity on one day
MAX_ROWS_PER_SET = 20_000  # one commodity on one day is a few hundred rows; far more means a filter was ignored
USER_AGENT = "de-course-kit/1.0 (data/prices/get_prices.py)"

KIT_FOLDER = Path(__file__).resolve().parent
README_HINT = "~/de-kit/data/prices/README.md"
SAMPLE_HINT = "~/de-kit/data/prices/sample"

SOURCE = {
    "dataset": "Variety-wise Daily Market Prices Data of Commodity",
    "publisher": "Directorate of Marketing and Inspection, Ministry of Agriculture and Farmers Welfare (AGMARKNET)",
    "page": "https://www.data.gov.in/resource/variety-wise-daily-market-prices-data-commodity",
    "resource_id": RESOURCE_ID,
    "licence": "Government Open Data License - India",
    "licence_url": "https://www.data.gov.in/Godl",
    "attribution": (
        "Directorate of Marketing and Inspection, Ministry of Agriculture and Farmers Welfare, 2024, "
        "Variety-wise Daily Market Prices Data of Commodity, Open Government Data Platform India, 21/05, "
        "https://www.data.gov.in/resource/variety-wise-daily-market-prices-data-commodity. "
        "Published under Government Open Data License - India: https://www.data.gov.in/Godl."
    ),
    "price_unit": "Rs./Quintal",
}


class ApiProblem(Exception):
    """The API answered, but not with what we need. The message says what to do."""


# ---------------------------------------------------------------------------
# Talking to the API
# ---------------------------------------------------------------------------

def server_message(problem: urllib.error.HTTPError) -> str:
    """The short error text the API sends with a refusal, such as 'Key not authorised'."""
    try:
        body = json.loads(problem.read().decode("utf-8", errors="replace"))
        return str(body.get("error") or body.get("message") or body)
    except (ValueError, AttributeError):
        return problem.reason or "no message"


def request_page(key: str, filters: dict[str, str], offset: int, limit: int) -> tuple[int, dict]:
    """Ask for one page of rows. Returns the HTTP status and the parsed answer.

    Numbers in the answer are kept as text (parse_int=str, parse_float=str), so a price
    such as 2450.50 is saved exactly as the API wrote it, not as 2450.5.
    The key is part of the address, so this function never prints the address.
    """
    params = {"api-key": key, "format": "json", "offset": str(offset), "limit": str(limit)}
    for name, value in filters.items():
        params[f"filters[{name}]"] = value
    url = API + RESOURCE_ID + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})

    waits = [5, 20, 60]  # seconds to wait before the second, third and fourth try
    for attempt in range(len(waits) + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                status, body = response.status, response.read()
        except urllib.error.HTTPError as problem:
            message = server_message(problem)
            if problem.code in (401, 403):
                raise ApiProblem(
                    f"The API refused your key (HTTP {problem.code}: {message}).\n"
                    f"Copy the key again from your data.gov.in account (see {README_HINT}), then run\n"
                    f"  export {KEY_VARIABLE}=<your key>\n"
                    f"Still refused after 15 minutes? Use the sample month {SAMPLE_HINT} "
                    "and tell your mentor.") from None
            if problem.code == 429 or problem.code >= 500:
                reason = f"HTTP {problem.code}: {message}"
            else:
                raise ApiProblem(f"The API answered HTTP {problem.code}: {message}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as problem:
            reason = f"no answer ({getattr(problem, 'reason', problem)})"
        else:
            try:
                payload = json.loads(body.decode("utf-8"), parse_int=str, parse_float=str)
            except ValueError:
                raise ApiProblem("The API did not answer with JSON. The site may be down; try again later.") from None
            if not isinstance(payload, dict) or payload.get("error") or payload.get("status") == "error":
                text = payload.get("error") or payload.get("message") if isinstance(payload, dict) else payload
                raise ApiProblem(f"The API answered with an error: {text}")
            return status, payload
        if attempt == len(waits):
            raise ApiProblem(f"The API did not answer after {attempt + 1} tries ({reason}). "
                             f"Try again later, or use the sample month {SAMPLE_HINT}.")
        print(f"  ... {reason}; trying again in {waits[attempt]} seconds", flush=True)
        time.sleep(waits[attempt])
    raise AssertionError("not reached")


def as_int(value) -> int | None:
    """'1234' or 1234 -> 1234; anything else -> None."""
    text = str(value).strip() if value is not None else ""
    return int(text) if text.isdigit() else None


def fetch_all(key: str, filters: dict[str, str]) -> tuple[int, list[dict]]:
    """Ask for every row that matches the filters, one page at a time."""
    records: list[dict] = []
    status, previous = 0, None
    for page_number in range(MAX_PAGES):
        if page_number:
            time.sleep(PAUSE_SECONDS)
        status, payload = request_page(key, filters, offset=len(records), limit=PAGE_SIZE)
        page = payload.get("records") or []
        if page and page == previous:
            raise ApiProblem("The API sent the same page twice, so it ignored the offset and rows would repeat. "
                             "Tell your mentor.")
        previous = page
        total = as_int(payload.get("total"))
        offered = max(total or 0, len(records) + len(page))
        if offered > MAX_ROWS_PER_SET:
            raise ApiProblem(f"The API offered {offered:,} rows for one commodity on one day. "
                             "It probably ignored a filter. Run --check and tell your mentor.")
        records.extend(page)
        if not page or (total is not None and len(records) >= total):
            return status, records
    raise ApiProblem(f"Stopped after {MAX_PAGES} pages for one commodity on one day. Tell your mentor.")


# ---------------------------------------------------------------------------
# Turning the answer into rows
# ---------------------------------------------------------------------------

def simple(name: str) -> str:
    """'Arrival_Date', 'arrival_date' and 'Arrival Date' all become 'arrivaldate'."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def to_row(record: dict) -> list[str]:
    """One API record as a list of 11 texts in HEADER order. The values are not changed."""
    by_name = {simple(name): value for name, value in record.items()}
    missing = [column for column in HEADER if simple(column) not in by_name]
    if missing:
        raise ApiProblem(f"The API sent no {', '.join(missing)} field. It sent: {', '.join(record)}. "
                         "The source may have changed; tell your mentor.")
    return ["" if by_name[simple(column)] is None else str(by_name[simple(column)]) for column in HEADER]


def check_rows(rows: list[list[str]], day: dt.date, commodity: str, state: str | None) -> None:
    """Stop if the API sent rows for another day, commodity or state: a filter did not work."""
    date_at, commodity_at, state_at = HEADER.index("Arrival_Date"), HEADER.index("Commodity"), HEADER.index("State")
    for row in rows:
        try:
            same_day = dt.datetime.strptime(row[date_at].strip(), DATE_LAYOUT).date() == day
        except ValueError:
            same_day = False
        if not same_day:
            raise ApiProblem(f"Asked for {day:{DATE_LAYOUT}} but got a row dated {row[date_at]!r}. "
                             "The date filter or the date layout has changed. Run --check and tell your mentor.")
        if simple(row[commodity_at]) != simple(commodity):
            raise ApiProblem(f"Asked for {commodity} but got {row[commodity_at]!r}. "
                             "The commodity filter has changed. Run --check and tell your mentor.")
        if state and simple(row[state_at]) != simple(state):
            raise ApiProblem(f"Asked for {state} but got {row[state_at]!r}. The state filter has changed.")


def download_day(key: str, day: dt.date, commodities: list[str],
                 states: list[str] | None) -> tuple[int, list[list[str]]]:
    """All rows of one day for the chosen commodities (and states), in that order."""
    rows: list[list[str]] = []
    status = 0
    for commodity in commodities:
        for state in states or [None]:
            filters = {DATE_FILTER: day.strftime(DATE_LAYOUT), COMMODITY_FILTER: commodity}
            if state:
                filters[STATE_FILTER] = state
            time.sleep(PAUSE_SECONDS)
            status, records = fetch_all(key, filters)
            new_rows = [to_row(record) for record in records]
            check_rows(new_rows, day, commodity, state)
            rows.extend(new_rows)
    return status, rows


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

def write_day(path: Path, rows: list[list[str]]) -> None:
    # newline="" and lineterminator="\n" give the same bytes on Windows, macOS and Linux.
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(rows)


def write_source(folder: Path, month: str, commodities: list[str], states: list[str] | None,
                 files: list[dict]) -> None:
    info = dict(SOURCE)
    info.update({
        "month": month,
        "commodities": commodities,
        "states": states or ["all"],
        "downloaded_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "files": files,
    })
    (folder / "source.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8", newline="\n")


def month_days(month: str) -> list[dt.date]:
    first = dt.datetime.strptime(month, "%Y-%m").date()
    days = []
    day = first
    while day.month == first.month:
        days.append(day)
        day += dt.timedelta(days=1)
    return days


# ---------------------------------------------------------------------------
# The two commands: download a month, or check the key
# ---------------------------------------------------------------------------

def get_key() -> str:
    key = os.environ.get(KEY_VARIABLE, "").strip()
    if not key:
        sys.exit(f"{KEY_VARIABLE} is not set, so the script cannot ask data.gov.in for prices.\n"
                 f"Get a free key: read {README_HINT}, section \"Get your free key\". Then run\n"
                 f"  export {KEY_VARIABLE}=<your key>\n"
                 f"No key yet? Use the sample month instead: {SAMPLE_HINT}")
    return key


def download_month(key: str, month: str, commodities: list[str], states: list[str] | None, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    # Remove an old source.json first: a folder without one is clearly not finished.
    (out / "source.json").unlink(missing_ok=True)
    days = month_days(month)
    where = f" in {', '.join(states)}" if states else ""
    print(f"Downloading {month} for {', '.join(commodities)}{where} from data.gov.in "
          f"({len(days)} days, {len(days) * len(commodities) * len(states or [None])} requests or more)", flush=True)
    files, total, empty = [], 0, 0
    for day in days:
        status, rows = download_day(key, day, commodities, states)
        name = f"prices-{day.isoformat()}.csv"
        write_day(out / name, rows)
        files.append({"name": name, "date": day.isoformat(), "rows": len(rows)})
        total += len(rows)
        empty += not rows
        print(f"{day.isoformat()} {day:%a}  HTTP {status}  {len(rows):,} rows", flush=True)
    write_source(out, month, commodities, states, files)
    print(f"Done: {len(files)} files ({empty} with no rows) and source.json, {total:,} rows, in {out.as_posix()}")


def check_key(key: str) -> bool:
    """A few small requests that show whether the key, the fields and the filters work."""
    status, payload = request_page(key, {}, offset=0, limit=1)
    records = payload.get("records") or []
    print(f"Key accepted: HTTP {status}. The dataset holds {payload.get('total', '?')} rows in all.")
    if not records:
        print("WARNING: the API sent no rows at all. Tell your mentor.")
        return False
    print(f"Fields sent: {', '.join(records[0])}")
    to_row(records[0])  # stops with a clear message if a column is missing
    print("All 11 columns are there.")

    # Find a recent day with tomato prices, to test the date and commodity filters.
    day = dt.date.today() - dt.timedelta(days=1)
    for _ in range(10):
        time.sleep(PAUSE_SECONDS)
        filters = {DATE_FILTER: day.strftime(DATE_LAYOUT), COMMODITY_FILTER: "Tomato"}
        status, payload = request_page(key, filters, offset=0, limit=5)
        rows = [to_row(record) for record in payload.get("records") or []]
        if rows:
            check_rows(rows, day, "Tomato", None)  # stops if the filters were ignored
            print(f"Filters work: Tomato on {day:{DATE_LAYOUT}} has {payload.get('total', '?')} rows "
                  f"(HTTP {status}). First market: {rows[0][HEADER.index('Market')]!r}.")
            print("Your key is ready. Now run the script with --month YYYY-MM.")
            return True
        day -= dt.timedelta(days=1)
    print("WARNING: no Tomato rows in the last 10 days. The filters may have changed; tell your mentor.")
    return False


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download one month of daily wholesale market prices (data.gov.in, AGMARKNET) "
                    f"as raw CSV files. Needs a free key in the environment variable {KEY_VARIABLE}.")
    parser.add_argument("--month", help="the month to download, as YYYY-MM, for example 2026-10 (a finished month)")
    parser.add_argument("--commodity", action="append",
                        help="a commodity to download, exactly as the source spells it; repeat for more "
                             f"(default: {', '.join(DEFAULT_COMMODITIES)})")
    parser.add_argument("--state", action="append",
                        help="download only this state, exactly as the source spells it; repeat for more "
                             "(default: every state)")
    parser.add_argument("--out", help="folder for the files (default: downloads/YYYY-MM next to this script)")
    parser.add_argument("--check", action="store_true",
                        help="test your key with a few small requests, without downloading a month")
    args = parser.parse_args(argv)
    if not args.check:
        if not args.month:
            parser.error("give --month YYYY-MM (for example last month), or --check to test your key")
        try:
            first = dt.datetime.strptime(args.month, "%Y-%m").date()
        except ValueError:
            parser.error(f"--month must look like 2026-10, not {args.month!r}")
        if first >= dt.date.today().replace(day=1):
            parser.error(f"{args.month} is not finished yet. Choose last month or an earlier one.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    key = get_key()
    try:
        if args.check:
            return 0 if check_key(key) else 1
        commodities = args.commodity or DEFAULT_COMMODITIES
        out = Path(args.out) if args.out else KIT_FOLDER / "downloads" / args.month
        download_month(key, args.month, commodities, args.state, out)
    except ApiProblem as problem:
        print(f"Stopped: {problem}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Stopped by you. Run the same command again to start the month again.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
