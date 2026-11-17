"""Cut every masked note into chunks of whole sentences, and store each chunk with its source.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run --env-file .env python -m careline.chunk
"""

import os

DEFAULT_MAX_WORDS = 60  # used when CHUNK_MAX_WORDS is not set in .env


def split_text(text: str, max_words: int = 60, overlap: int = 1) -> list[str]:
    """Split a text into chunks of whole sentences, in order.

    A pure function: no database, no model, no files.
    - Split the text into sentences with re.split(r"(?<=[.!?])\\s+", text).
    - Add sentences to a chunk until the next one would take it past max_words
      words. Never cut a sentence: a sentence longer than max_words is a chunk
      on its own.
    - Start each new chunk with the last `overlap` sentences of the chunk before.

    Returns the chunks as strings. A short text gives one chunk.
    """
    raise NotImplementedError("TODO(task 8): pack whole sentences into chunks, with overlap")


def chunk_notes(conn, max_words: int = DEFAULT_MAX_WORDS) -> tuple[int, int]:
    """Chunk every note of clean.visit_notes that has no chunk at its current version.

    Compare ai.chunks.version with clean.visit_notes.version. For each such note,
    delete its old chunks and insert the new ones from masked_text (note_id,
    chunk_no, version, appointment_id, text, word_count) inside one transaction,
    so the delete and the inserts succeed or fail together (with conn.transaction():
    in psycopg). Never chunk raw text.
    Returns (notes chunked, chunks written). A second run returns (0, 0).
    """
    raise NotImplementedError("TODO(task 8): chunk the notes that are new or have a new version")


def main() -> None:
    """Read CHUNK_MAX_WORDS (default 60), chunk the notes and print the counts."""
    max_words = int(os.environ.get("CHUNK_MAX_WORDS", DEFAULT_MAX_WORDS))
    # Imported here, so importing this module never loads the database driver.
    from careline.db import connect

    with connect() as conn:
        notes, chunks = chunk_notes(conn, max_words=max_words)
    print(f"chunked {notes} notes, {chunks} chunks")


if __name__ == "__main__":
    main()
