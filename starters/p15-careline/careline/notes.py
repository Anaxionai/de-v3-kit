"""Load the clinic's visit notes into raw, and mask them into clean.visit_notes.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run python -m careline.notes           # load the new note files, then mask new or corrected notes
    uv run python -m careline.notes --scan    # count the notes with personal data in raw and in clean

make_clinic.py --notes writes the files (the kit's data/clinic/README.md, "Visit notes").
"""

import argparse
from pathlib import Path

# Built from this file's place, like DATA_DIR in careline/db.py, so it works from any folder.
NOTES_DIR = Path(__file__).resolve().parents[1] / "data" / "notes"


def load_notes() -> tuple[int, int]:
    """Load every file in NOTES_DIR whose name is not yet in raw.visit_notes.source_file.

    The file names already loaded are your watermark (P4): a file is loaded once,
    so a second run loads 0 files. Insert each row's six file columns as text,
    with the file's name in source_file. Read the files with a CSV reader: a
    note holds commas.
    Open the connection with careline.db.connect() inside this function. Import
    it there, not at the top of this file, so the tests never load the database
    driver (main() below does the same).
    Returns (files loaded, rows loaded).
    """
    raise NotImplementedError("TODO(task 7): load only the note files not loaded before")


def mask_new(conn) -> int:
    """Write the masked text of every raw note that is new or corrected into clean.visit_notes.

    A raw row is new when clean.visit_notes has no row for its note_id, and
    corrected when its version is higher than the clean row's version. Mask it
    with mask_text() and the names from load_names(conn) (careline.mask), and keep
    exactly one clean row per note_id, at its newest version: an upsert,
    INSERT ... ON CONFLICT (note_id) DO UPDATE.
    Returns the number of notes written. A second run returns 0.
    """
    raise NotImplementedError("TODO(task 7): mask the new and corrected notes into clean")


def scan(conn) -> tuple[int, int]:
    """Count the rows in which find_personal() finds anything: (raw.visit_notes, clean.visit_notes).

    Scan raw.visit_notes.note_text (every row, every version) and
    clean.visit_notes.masked_text, with the names from load_names(conn).
    The raw count must equal the "notes with planted personal data" number that
    make_clinic.py printed, and the clean count must be 0.
    """
    raise NotImplementedError("TODO(task 7): count the notes with personal data in raw and in clean")


def main(argv: list[str] | None = None) -> None:
    """Load and mask (no option), or scan (--scan), and print the counts."""
    parser = argparse.ArgumentParser(description="Load and mask CareLine's visit notes.")
    parser.add_argument("--scan", action="store_true", help="count the notes with personal data in raw and in clean")
    args = parser.parse_args(argv)
    # Imported here, so importing this module never loads the database driver.
    from careline.db import connect

    if args.scan:
        with connect() as conn:
            raw, clean = scan(conn)
        print(f"raw.visit_notes:   {raw} note rows with personal data")
        print(f"clean.visit_notes: {clean} notes with personal data")
        return
    files, rows = load_notes()
    with connect() as conn:
        masked = mask_new(conn)
    print(f"loaded {files} files ({rows} rows), masked {masked} notes")


if __name__ == "__main__":
    main()
