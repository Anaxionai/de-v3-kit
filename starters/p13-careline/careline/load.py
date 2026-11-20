"""Load the clinic's files into the raw layer: every value as text, with its file name.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run python -m careline.load --all                         # reference files and every day
    uv run --env-file .env python -m careline.load --set-salt    # task 11
"""

from pathlib import Path

from careline.db import DATA_DIR

APPOINTMENTS_DIR = DATA_DIR / "appointments"


def day_path(day: str) -> Path:
    """The appointments file of one day: data/appointments/appointments_<day>.csv."""
    return APPOINTMENTS_DIR / f"appointments_{day}.csv"


def load_reference() -> None:
    """Replace raw.patients and raw.doctors with data/patients.csv and data/doctors.csv.

    Read each file with pandas.read_csv(path, dtype=str, keep_default_na=False),
    so every value stays text and an empty cell stays "". Store the file's name
    in source_file.
    """
    raise NotImplementedError("TODO(task 8): replace the patients and doctors tables")


def load_day(day: str) -> int:
    """Load one day's appointments file into raw.appointments; return the rows loaded.

    Delete the rows whose source_file is this file's name, then insert the
    file, in one transaction, so loading a day twice keeps the same count.
    A missing file raises FileNotFoundError.
    """
    # TODO(task 10): before the delete, call contract.check_header() with the
    # file's columns, so a file that breaks the contract is refused at the door.
    raise NotImplementedError("TODO(task 8): reload one day's file")


def set_salt() -> None:
    """Store CARELINE_SALT from the environment in raw.pipeline_secret (one row).

    Refuse to run when CARELINE_SALT is empty or still "change-me".
    """
    raise NotImplementedError("TODO(task 11): store the salt in raw")


def main(argv: list[str] | None = None) -> None:
    """Read the command line with argparse and run what it asks for.

    --all: load_reference(), then load_day() for every file in APPOINTMENTS_DIR,
    printing the rows per file.
    """
    # TODO(task 11): add --set-salt, which calls set_salt().
    raise NotImplementedError("TODO(task 8): the --all option")


if __name__ == "__main__":
    main()
