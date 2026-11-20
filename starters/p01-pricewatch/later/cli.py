"""PriceWatch's one command, with a subcommand for each step.

Task 12: move this file into the package, as pricewatch/pricewatch/cli.py.
Tasks 19 to 24 add to it. Run it from the product folder (the one with pyproject.toml):

    uv run python -m pricewatch.cli fetch <folder>
    uv run python -m pricewatch.cli load
    uv run python -m pricewatch.cli report
    uv run python -m pricewatch.cli compare
    uv run python -m pricewatch.cli chart <commodity>

cli.py only reads the command and calls functions from the other modules. Import them
in the package form, for example: from pricewatch.load import read_all
"""


def main():
    """Read the command from sys.argv and run it.

    sys.argv[0] is the program, sys.argv[1] the command and sys.argv[2] its argument.
    Check len(sys.argv) before you read from it.

    TODO(task 12): fetch <folder> copies and checks the raw files; load cleans, converts
        and saves the clean CSV; report prints the number of clean rows and the lowest,
        median and highest price per commodity. A missing or unknown command prints one
        usage line and calls sys.exit(2).
    TODO(task 19): compare runs both cleaning chains and prints the CompareResult.
    TODO(task 20): report builds the clean table with clean_frame, prints the weekly
        cheapest and dearest markets, and saves reports/weekly_extremes.csv.
    TODO(task 21): report also prints the gap counts and the ten largest jumps.
    TODO(task 23): configure logging once, with the level from PRICEWATCH_LOG_LEVEL, and
        make load write reports/run_report.md.
    TODO(task 24): chart <commodity> draws the chart and saves reports/chart_data.csv.
    """
    raise NotImplementedError("TODO(task 12): read the command from sys.argv and run it")


if __name__ == "__main__":
    main()
