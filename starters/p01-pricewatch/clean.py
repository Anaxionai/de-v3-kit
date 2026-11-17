"""Give every market and commodity one spelling.

Task 10. Run it from the pricewatch/ folder:

    uv run python clean.py data/raw

Always compare a market together with its state: two towns in different states can
share a name.
"""

import sys
from pathlib import Path

from load import read_all

# Your chosen spelling for each name that a rule cannot fix.
# Key: the name in lower case after tidy(). Value: the spelling you choose.
# An empty table is fine if NOTES.md says that your month needs no alias.
MARKET_ALIASES = {}

# Commodity names as PriceWatch spells them, keyed the same way as MARKET_ALIASES.
# For example, Coriander(Leaves) should come out as Coriander leaves.
COMMODITY_NAMES = {}


def tidy(text):
    """Return the name with its spaces made regular.

    - Strip both ends, and turn each run of spaces into one space.
    - Remove a space before "," or ")" and a space after "(".
    - Put exactly one space before "(" and after ",".
    Use split, join and replace. For example "Garh Shankar  (Kotfatuhi )" and
    "Garh Shankar(Kotfatuhi)" must give the same text.
    """
    raise NotImplementedError("TODO(task 10): write tidy(text)")


def name_key(text):
    """A key for comparing names: tidy(text) in lower case, keeping only letters and digits.

    Test each character with isalnum(). Two spellings of one market give the same key.
    """
    raise NotImplementedError("TODO(task 10): write name_key(text)")


def clean_market(name):
    """Return the one spelling of a market name.

    Tidy the name, give it title case, then look up its lower-case form in
    MARKET_ALIASES. Names that differ only in case, extra spaces, or the spacing around
    brackets and commas must come out identical.
    """
    raise NotImplementedError("TODO(task 10): write clean_market(name)")


def clean_commodity(name):
    """Return the one spelling of a commodity name, through COMMODITY_NAMES.

    Work the same way as clean_market. A name that is not in the table stays tidy.
    """
    raise NotImplementedError("TODO(task 10): write clean_commodity(name)")


def clean_records(records):
    """Return a new list of new records with a clean state, market and commodity.

    Make each new record with dict(record), so the records you were given never change.
    """
    raise NotImplementedError("TODO(task 10): write clean_records(records)")


if __name__ == "__main__":
    records, bad_rows = read_all(Path(sys.argv[1]))
    # TODO(task 10): count the distinct (state, market) pairs; print each group of tidy
    # names with the same (state, name_key(market)) and more than one spelling; print the
    # candidates that share the text before the first "(" or ","; then print the distinct
    # markets before and after cleaning, and the groups that still have two spellings.
    # TODO(task 10): five assert lines for clean_market: extra spaces, lower case, no space
    # before a bracket, a space before a comma, and one alias.
