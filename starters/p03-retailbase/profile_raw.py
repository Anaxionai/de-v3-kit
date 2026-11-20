"""Profile the raw sales file with pandas, before any table is designed.

Task 7. Run it from retailbase/, after `uv add pandas` (step 1) and the download (step 2):

    uv run python profile_raw.py
"""

import pandas as pd

RAW_FILE = "data/online_retail_II.csv"

# Show wide tables in one block, so the output you paste into evidence.md stays readable.
pd.set_option("display.width", 120)


def main():
    """Read RAW_FILE and print what it holds.

    - Read the CSV with pd.read_csv(..., dtype=str), so every value stays text, exactly
      as it arrived.
    - Print df.shape, then df.isna().sum(): the missing values in each column.
    - Print the first and last InvoiceDate of each Sheet. The dates are text in the form
      YYYY-MM-DD HH:MM:SS, so the smallest text is the earliest date.
    """
    raise NotImplementedError("TODO(task 7): read the raw file and print its profile")


if __name__ == "__main__":
    main()
