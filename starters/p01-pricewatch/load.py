"""Read the raw price files into records, and report every row that cannot be read.

Task 9. Run it from the pricewatch/ folder:

    uv run python load.py data/raw
    uv run python load.py data/broken

A record is a dictionary with these keys:
    date (a datetime.date), state, market, commodity, variety, unit (text),
    min_price, max_price, modal_price (float).

Modules you will need: csv (DictReader), json and datetime (datetime.strptime).
"""

import sys
from pathlib import Path


class BadRow(ValueError):
    """A row that cannot be read. Its message is a short reason, such as "bad date: 31/02/2026"."""


def parse_row(row, unit):
    """Turn one row from csv.DictReader into a record, or raise BadRow.

    row:  a dictionary of the raw columns (State, Market, Arrival_Date, Min_Price, ...).
    unit: the price unit of the whole file, from source.json, such as "Rs./Quintal".

    - date comes from Arrival_Date, which is day first:
      datetime.strptime(text, "%d/%m/%Y").date()
    - min_price, max_price and modal_price come from Min_Price, Max_Price and
      Modal_Price with float().
    - state, market, commodity and variety stay as text, unchanged (task 10 cleans them).

    Raise BadRow with a short reason, "<what>: <value>", for:
    - a missing or empty value (a line cut short gives None for its missing columns);
    - a date that does not exist, such as 31/02/2026;
    - a price that is not a number, such as abc.
    Check for None and empty text before you convert: float(None) raises TypeError.
    Rules about the prices themselves (zero, out of order, unclear unit) come in task 11.
    """
    raise NotImplementedError("TODO(task 9): write parse_row(row, unit)")


def read_prices(path, unit):
    """Read one prices-YYYY-MM-DD.csv file. Returns (records, bad_rows).

    - Read the file with csv.DictReader and call parse_row for each row.
    - Catch BadRow for each row (except BadRow as problem:). Add a bad row with the
      file name, the line number and str(problem), then carry on with the next row.
      Line 1 is the header: for line_no, row in enumerate(reader, start=2):
    - If the header lacks a column you need, raise ValueError naming the column: that
      whole file is unusable.
    - Never use a bare except:, and never hide an error with except Exception: pass.

    A bad row can be a dictionary, such as {"file": ..., "line": ..., "reason": ...}.
    """
    raise NotImplementedError("TODO(task 9): write read_prices(path, unit)")


def read_all(folder):
    """Read every prices-*.csv file in `folder`. Returns (records, bad_rows) for the month.

    - Read price_unit from the folder's source.json and pass it to read_prices.
    - Read the files in name order (sorted), so the days come in date order.
    - Join the records of all the files into one list, and their bad rows into another.
    """
    raise NotImplementedError("TODO(task 9): write read_all(folder)")


if __name__ == "__main__":
    records, bad_rows = read_all(Path(sys.argv[1]))
    # TODO(task 9): print the number of files, records and bad rows, the number of bad
    # rows per reason (the text before the colon), and then each bad row.
