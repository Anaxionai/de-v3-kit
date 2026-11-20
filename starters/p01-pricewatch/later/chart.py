"""Chart one vegetable's price in three markets across the month.

Task 24: run `uv add matplotlib`, then move this file into the package, as
pricewatch/pricewatch/chart.py.
"""

import pandas as pd


def chart_table(daily: pd.DataFrame, commodity: str) -> pd.DataFrame:
    """One commodity's reported prices: one row per date and one column per market,
    for the three markets with the most reporting days (value_counts().head(3)).
    Use reported prices only, never filled ones, so a gap shows as a break in the line."""
    raise NotImplementedError("TODO(task 24): write chart_table(daily, commodity)")


# TODO(task 24): draw the table as a line chart with a title, labelled axes with the unit,
# a price axis that starts at zero and the source line, and save it as
# reports/<commodity>_3_markets.png. Save the table as reports/chart_data.csv.
