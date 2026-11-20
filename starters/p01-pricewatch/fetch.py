"""Copy one month of raw price files into data/raw/ and check what arrived.

Task 8. Run it from the pricewatch/ folder:

    uv run python fetch.py <folder>

<folder> holds source.json and one prices-YYYY-MM-DD.csv file per day: the folder that
get_prices.py names on its Done: line, or the kit's sample month ~/de-kit/data/prices/sample.

Modules you will need: csv (DictReader), json, shutil (copy2) and datetime (date).
"""

import sys
from pathlib import Path


def fetch_month(source, raw_dir):
    """Copy source.json and every file it lists from `source` into `raw_dir`, and check them.

    source:  a Path to the month's folder (it holds source.json).
    raw_dir: a Path to copy into, such as Path("data/raw"). Create it if it is missing.

    - Read source.json. Its "files" list has one entry per day, with "name" and "rows".
    - Copy source.json and each listed file with shutil.copy2. Never open a raw file
      for writing: the raw copy must stay exactly as the source sent it.
    - In the same loop, count each copied file's data rows with csv.DictReader (the
      header is not a data row) and compare the count with that file's "rows".

    Returns a dictionary with:
    - "files": one (name, rows counted) pair per copied day file, in order;
    - "rows": the total number of data rows;
    - "empty_days": the names of the files with no data rows (header only);
    - "mismatches": one (name, expected, counted) entry per file whose count is not "rows".
    Zero empty days or zero mismatches is a valid result.
    """
    raise NotImplementedError("TODO(task 8): write fetch_month(source, raw_dir)")


if __name__ == "__main__":
    summary = fetch_month(Path(sys.argv[1]), Path("data/raw"))
    # TODO(task 8): print each file with its rows, the totals, and the weekday name of each
    # empty day. date.fromisoformat(name[7:17]).strftime("%A") gives the weekday of the
    # file prices-YYYY-MM-DD.csv.
