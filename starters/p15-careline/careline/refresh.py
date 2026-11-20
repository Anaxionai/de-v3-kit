"""Keep the index fresh: load, mask, chunk and embed only the notes that are new or corrected.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run --env-file .env python -m careline.refresh
    uv run --env-file .env python -m careline.refresh --no-embed
"""


def changed_notes(chunked: dict[str, int], current: dict[str, int]) -> tuple[list[str], list[str]]:
    """Compare two maps of note_id to version, and return (new, corrected), each sorted.

    `chunked` holds the version each note's chunks carry (ai.chunks), and `current`
    the note's version in clean.visit_notes. New: a note_id in `current` with no
    entry in `chunked`. Corrected: a note whose current version is higher than
    its chunks' version.
    A pure function: no database, no model.
    """
    raise NotImplementedError("TODO(task 11): the new and the corrected note ids")


def main(argv: list[str] | None = None) -> None:
    """One refresh, in this order: load_notes(), mask_new(), changed_notes() on the
    versions in ai.chunks and clean.visit_notes, chunk_notes() with the
    CHUNK_MAX_WORDS setting (as chunk.main() reads it) and, unless --no-embed is
    given, embed_chunks().

    Print a line such as "files 1, new 19, corrected 2, chunks embedded 27".
    A second run straight after prints "files 0, new 0, corrected 0, chunks embedded 0".
    Import the other careline modules and careline.db.connect() inside this function.
    """
    raise NotImplementedError("TODO(task 11): one refresh, with --no-embed")


if __name__ == "__main__":
    main()
