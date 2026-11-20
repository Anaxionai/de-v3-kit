"""The week 1 cleaning rebuilt with pandas, and a check that both versions agree.

Task 19: run `uv add pandas`, then move this file into the package, as
pricewatch/pricewatch/frame.py. Use column operations and boolean masks, never a loop
over the rows. Calling your week 1 name functions with .map is fine.
"""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


def load_frame(raw_dir: Path) -> pd.DataFrame:
    """Read every prices-*.csv file in raw_dir with dtype=str and join them with pd.concat."""
    raise NotImplementedError("TODO(task 19): write load_frame(raw_dir)")


def clean_frame(df: pd.DataFrame, unit: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply the week 1 rules to the whole table. Returns (clean, rejected).

    - Rename the columns to the record field names first.
    - Convert whole columns with pd.to_datetime(..., format="%d/%m/%Y", errors="coerce")
      and pd.to_numeric(..., errors="coerce"): a value that fails becomes missing.
    - Clean state, market and commodity with your week 1 functions, through
      .map(..., na_action="ignore").
    - One boolean mask per rule: a missing value, a price of zero or less, prices out of
      order, a modal price below your threshold. Join them with | into one mask.
    - The clean rows get the three prices in rupees per kilogram (rounded to 2 places),
      unit "kg", and only the nine record columns.
    """
    raise NotImplementedError("TODO(task 19): write clean_frame(df, unit)")


@dataclass
class CompareResult:
    """What compare() found: the row counts of both chains and whether the tables match.

    TODO(task 19): the fields plain_rows, pandas_rows, plain_bad and pandas_bad (each an
    int) and same (a bool).
    """


def compare(raw_dir: Path) -> CompareResult:
    """Run the week 1 chain and the pandas chain on the same raw folder and compare them.

    Make the week 1 records a table with pd.DataFrame(records) and convert its date with
    pd.to_datetime. Sort both tables by the nine columns, reset_index(drop=True), and
    compare them inside try with
    pandas.testing.assert_frame_equal(a, b, check_dtype=False, atol=0.005).
    """
    raise NotImplementedError("TODO(task 19): write compare(raw_dir)")
