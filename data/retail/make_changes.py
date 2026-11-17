#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Write a customer change batch for slowly changing dimension (SCD type 2) practice, for RetailBase (P3).

Run it inside your retailbase/ folder, after get_retail.py:

    uv run ~/de-kit/data/retail/make_changes.py --student <your-id>

<your-id> is your GitHub username in lower case. It writes data/customer_changes.csv with the
header customer_id,country,changed_on and 60 rows, in random order:
  - 40 moves: existing customers who now live in another country, from the date changed_on;
  - 10 new customers: ids from 19001 to 19999, which have no sales yet;
  - 10 rows with no change: existing customers with the country they already have.

The same --student always gives the same batch, on any computer, so your mentor can make
your batch again. Different students get different batches.

How the customers are chosen (read this before task 11):
  - Rows of the first sheet dated from 2010-12-01 are left out, as in your fact table:
    they are copies of rows in the second sheet.
  - Moves and no-change rows use only customers with exactly one country in the file.
    A moved customer has sales on at least two different days, and changed_on is one of
    those days other than the first. So each moved customer has sales before the change
    and sales on or after it, and both versions of the customer get fact rows.
  - A no-change row and a new customer get a changed_on in 2011, before 2011-12-10.

The script uses only the Python standard library. The data is the UCI Online Retail II file
(CC BY 4.0); the batch itself is made up for practice.
"""

import argparse
import csv
import datetime as dt
import hashlib
import random
import sys
from pathlib import Path

NEW_COUNTRIES = ["France", "Germany", "Netherlands", "Spain", "Belgium", "Switzerland",
                 "Portugal", "Australia", "Sweden", "Italy", "Norway", "Denmark"]
OVERLAP_START = dt.datetime(2010, 12, 1)   # the first sheet repeats the second sheet from this day
FIRST_SHEET = "Year 2009-2010"
LAST_DAY = dt.date(2011, 12, 10)           # the day after the last sale in the file
MOVES, NEW_CUSTOMERS, NO_CHANGE = 40, 10, 10
NEW_IDS = range(19001, 20000)              # the file's largest customer id is 18287


class Dice:
    """Random choices that are the same for the same seed on every Python version.

    Python only promises that random() gives the same numbers for the same seed in every
    version; helpers such as choice() and sample() have changed in the past. So every
    helper here is built on random() alone.
    """

    def __init__(self, seed_text: str) -> None:
        # hash() changes every time Python starts, so we use SHA-256 instead.
        digest = hashlib.sha256(seed_text.encode("utf-8")).digest()
        self._rng = random.Random(int.from_bytes(digest[:8], "big"))

    def number(self, low: int, high: int) -> int:
        """A whole number from low to high, both included."""
        return low + int(self._rng.random() * (high - low + 1))

    def pick(self, items):
        """One item from a list."""
        return items[int(self._rng.random() * len(items))]

    def shuffle(self, items: list) -> None:
        """Shuffle a list in place (the Fisher-Yates method)."""
        for i in range(len(items) - 1, 0, -1):
            j = self.number(0, i)
            items[i], items[j] = items[j], items[i]

    def sample(self, items, count: int) -> list:
        """count different items from a list, in random order."""
        pool = list(items)
        for i in range(count):
            j = self.number(i, len(pool) - 1)
            pool[i], pool[j] = pool[j], pool[i]
        return pool[:count]


def read_customers(raw: Path) -> tuple[dict[int, set[str]], dict[int, set[dt.date]]]:
    """For each customer id: the countries and the sale days in the file (overlap left out)."""
    countries: dict[int, set[str]] = {}
    days: dict[int, set[dt.date]] = {}
    with raw.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if not row["Customer ID"]:
                continue
            when = dt.datetime.fromisoformat(row["InvoiceDate"])
            if row["Sheet"] == FIRST_SHEET and when >= OVERLAP_START:
                continue
            customer = int(row["Customer ID"])
            countries.setdefault(customer, set()).add(row["Country"])
            days.setdefault(customer, set()).add(when.date())
    return countries, days


def make_batch(student: str, countries: dict[int, set[str]], days: dict[int, set[dt.date]]) -> list[tuple]:
    """The 60 rows (customer_id, country, changed_on, kind) for one student, shuffled."""
    dice = Dice(f"retailbase|{student}")
    single = sorted(c for c, names in countries.items() if len(names) == 1)
    movable = [c for c in single if len(days[c]) >= 2]
    movers = dice.sample(movable, MOVES)
    chosen = set(movers)
    unchanged = dice.sample([c for c in single if c not in chosen], NO_CHANGE)
    new_ids = dice.sample(NEW_IDS, NEW_CUSTOMERS)

    rows = []
    for customer in movers:
        sale_days = sorted(days[customer])
        changed_on = dice.pick(sale_days[1:])  # at least one sale before the change, and one on or after it
        old = next(iter(countries[customer]))
        rows.append((customer, dice.pick([c for c in NEW_COUNTRIES if c != old]), changed_on, "move"))
    for customer in unchanged:
        changed_on = LAST_DAY - dt.timedelta(days=dice.number(1, 300))
        rows.append((customer, next(iter(countries[customer])), changed_on, "no change"))
    for customer in new_ids:
        changed_on = LAST_DAY - dt.timedelta(days=dice.number(1, 300))
        rows.append((customer, dice.pick(NEW_COUNTRIES), changed_on, "new"))
    dice.shuffle(rows)
    return rows


def check_batch(rows: list[tuple], countries: dict[int, set[str]], days: dict[int, set[dt.date]]) -> None:
    """Stop with a clear message if the batch breaks a rule that tasks 11 and 12 depend on."""
    problems = []
    kinds = [kind for *_, kind in rows]
    if (kinds.count("move"), kinds.count("new"), kinds.count("no change")) != (MOVES, NEW_CUSTOMERS, NO_CHANGE):
        problems.append("the batch does not hold 40 moves, 10 new customers and 10 rows with no change")
    if len({customer for customer, *_ in rows}) != len(rows):
        problems.append("a customer id appears twice")
    for customer, country, changed_on, kind in rows:
        if kind == "move":
            sale_days = sorted(days[customer])
            if len(countries[customer]) != 1 or country in countries[customer]:
                problems.append(f"move {customer}: the country does not change")
            if not sale_days[0] < changed_on <= sale_days[-1] or changed_on not in sale_days:
                problems.append(f"move {customer}: {changed_on} is not a later sale day")
        elif kind == "no change":
            if countries.get(customer) != {country}:
                problems.append(f"no change {customer}: the country differs")
        elif customer in countries or customer not in NEW_IDS:
            problems.append(f"new customer {customer}: the id is already used or out of range")
        if kind != "move" and not dt.date(2011, 1, 1) <= changed_on < LAST_DAY:
            problems.append(f"{kind} {customer}: {changed_on} is not in 2011 before {LAST_DAY}")
    if problems:
        sys.exit("The batch failed its own check, so nothing was written. Tell your mentor:\n  "
                 + "\n  ".join(problems[:5]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write a customer change batch for SCD type 2 practice.")
    parser.add_argument("--student", required=True, help="your GitHub username in lower case")
    parser.add_argument("--raw", default="data/online_retail_II.csv",
                        help="the file get_retail.py wrote (default: data/online_retail_II.csv)")
    parser.add_argument("--out", default="data/customer_changes.csv",
                        help="where to write the batch (default: data/customer_changes.csv)")
    args = parser.parse_args(argv)
    student = args.student.strip().lower()
    if not student:
        parser.error("--student must not be empty")
    raw = Path(args.raw)
    if not raw.exists():
        sys.exit(f"{raw.as_posix()} not found. Run this script inside retailbase/, after "
                 "uv run ~/de-kit/data/retail/get_retail.py --out data")

    countries, days = read_customers(raw)
    rows = make_batch(student, countries, days)
    check_batch(rows, countries, days)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["customer_id", "country", "changed_on"])
        for customer, country, changed_on, _kind in rows:
            writer.writerow([customer, country, changed_on.isoformat()])
    print(f"Wrote {out.as_posix()}: {len(rows)} rows ({MOVES} moves, {NEW_CUSTOMERS} new customers, "
          f"{NO_CHANGE} with no change)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
