"""Convert every price to rupees per kilogram, and reject the prices you cannot trust.

Task 11. Run it from the pricewatch/ folder:

    uv run python units.py data/raw

It loads and cleans the records, converts them, and saves data/clean/prices.csv.
Modules you will need: csv (DictWriter) and statistics (median).
"""

import sys
from pathlib import Path

from clean import clean_records
from load import BadRow, read_all  # noqa: F401  (your rules in convert_record raise BadRow)

# The kilograms in each price unit, keyed by the unit in lower case.
UNITS = {}  # TODO(task 11): one entry each for "rs./quintal", "rs./kg" and "rs./tonne"

# The lowest modal price you accept as rupees per quintal. Choose it from your own data
# (step 1) and explain it in NOTES.md.
MIN_QUINTAL_PRICE = None  # TODO(task 11): your threshold


def to_rupees_per_kg(price, unit):
    """Convert one price to rupees per kilogram, rounded to 2 places.

    Look up unit.strip().lower() in UNITS and divide by its kilograms.
    Raise ValueError for a unit that is not in UNITS.
    Example: to_rupees_per_kg(2450, "Rs./Quintal") gives 24.5.
    """
    raise NotImplementedError("TODO(task 11): write to_rupees_per_kg(price, unit)")


def convert_record(record):
    """Return a new record with the three prices in rupees per kilogram and unit "kg".

    Raise BadRow, with a short reason, for:
    - a price of zero or less;
    - prices not in the order minimum <= modal <= maximum;
    - a modal price below MIN_QUINTAL_PRICE (reason "unit unclear").
    Never repair a rejected price by guessing, for example by multiplying it by 100.
    """
    raise NotImplementedError("TODO(task 11): write convert_record(record)")


def convert_all(records):
    """Convert every record. Returns (good, bad_rows), the same way read_prices does."""
    raise NotImplementedError("TODO(task 11): write convert_all(records)")


def save_clean(records, path):
    """Write the records to a CSV file with csv.DictWriter.

    The header is these nine fields, in this order:
        date, state, market, commodity, variety, unit, min_price, max_price, modal_price
    Write the date as YYYY-MM-DD with record["date"].isoformat(). Create the folder if
    it is missing.
    """
    raise NotImplementedError("TODO(task 11): write save_clean(records, path)")


if __name__ == "__main__":
    records, bad_rows = read_all(Path(sys.argv[1]))
    records = clean_records(records)
    # TODO(task 11): print the five lowest and five highest modal_price of each commodity,
    # with market and state. Then convert, save data/clean/prices.csv, and print rows in,
    # rows out, bad rows per reason, and each commodity's lowest, median and highest price.
    # TODO(task 11): three assert lines for to_rupees_per_kg, one for each unit.
