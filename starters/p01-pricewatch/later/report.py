"""The weekly report: cheapest and dearest markets, missing days and price jumps.

Task 20: move this file into the package, as pricewatch/pricewatch/report.py.
Task 21 adds the gap and jump functions at the end.
"""

import pandas as pd

# TODO(task 20): MIN_DAYS, the fewest reporting days a market needs in a week to be
# compared (the brief uses 3).
# TODO(task 21): FILL_LIMIT (the brief uses 2 days) and JUMP_LIMIT (the brief uses 0.5).


def daily_prices(clean: pd.DataFrame) -> pd.DataFrame:
    """The mean modal_price per date, state, market and commodity (as_index=False),
    because a market can report two varieties on one day. Add year and week from
    dt.isocalendar(): a week runs from Monday to Sunday."""
    raise NotImplementedError("TODO(task 20): write daily_prices(clean)")


def weekly_prices(daily: pd.DataFrame) -> pd.DataFrame:
    """Per commodity, year, week, state and market: the mean price and the number of
    reporting days. Keep only the market-weeks with at least MIN_DAYS days, and print
    how many you dropped."""
    raise NotImplementedError("TODO(task 20): write weekly_prices(daily)")


def weekly_extremes(weekly: pd.DataFrame) -> pd.DataFrame:
    """One row per commodity and week: cheapest_market, cheapest_price, dearest_market,
    dearest_price (each market with its state) and markets_compared. Find the rows with
    groupby(...)["price"].idxmin() and idxmax(), then merge."""
    raise NotImplementedError("TODO(task 20): write weekly_extremes(weekly)")


def series_table(daily: pd.DataFrame) -> pd.DataFrame:
    """One column per (commodity, state, market) and one row for every day of the month,
    so a day with no report holds NaN. Use pivot_table, then reindex over
    pd.date_range(first, last, freq="D"), and name the index "date" again."""
    raise NotImplementedError("TODO(task 21): write series_table(daily)")


def fill_gaps(wide: pd.DataFrame, limit: int) -> pd.DataFrame:
    """Return the table with the last reported price carried forward for at most
    `limit` days. A longer gap stays empty. A value was filled where `wide` is missing
    and the result is not: mark those values, so nobody takes them for real reports."""
    raise NotImplementedError("TODO(task 21): write fill_gaps(wide, limit)")


def find_jumps(wide: pd.DataFrame, limit: float) -> pd.DataFrame:
    """Return the change of each reported price that moved by more than `limit` against
    the last report (0.5 is a change of more than half), and NaN everywhere else.
    Measure the change with wide.ffill().pct_change(fill_method=None)."""
    raise NotImplementedError("TODO(task 21): write find_jumps(wide, limit)")
