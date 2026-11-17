"""Embed the chunks into pgvector, up to 20 texts in each call to the embedding model.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run --env-file .env python -m careline.embed --limit 20
    uv run --env-file .env python -m careline.embed

The model call, the vector size N, the text formats and the pause between calls
are in the kit's data/clinic/models.md. Only masked text reaches the model:
embed_texts() calls assert_masked() before anything else.
"""

import argparse

VECTOR_SIZE = 768  # N: it must equal the size in models.md and vector(N) in sql/03_ai.sql
BATCH_SIZE = 20  # texts in one call to the embedding model
PAUSE_SECONDS = 7  # the wait after each call, as models.md says (free-tier rate limits)


def document_text(note_type: str, text: str) -> str:
    """A chunk in the document format of models.md: "title: consultation note | text: ..."."""
    return f"title: {note_type} note | text: {text}"


def question_text(question: str) -> str:
    """A question in the question format of models.md: "task: question answering | query: ..."."""
    return f"task: question answering | query: {question}"


def embed_texts(texts: list[str], names: list[str]) -> list[list[float]]:
    """Embed up to BATCH_SIZE texts with ONE call to the embedding model (EMBED_MODEL).

    1. Call assert_masked(texts, names) (careline.mask) first: a text with
       personal data never leaves your laptop.
    2. Send each text as its own content item (types.Content) and ask for
       VECTOR_SIZE numbers (output_dimensionality). A plain list of strings comes
       back as ONE combined vector: models.md shows the right call. Import
       google.genai inside this function, after the guard, so the guard's tests
       need no key and no network.
    3. Raise ValueError unless exactly one vector of VECTOR_SIZE numbers came
       back for each text.

    Returns the vectors in the order of the texts.
    """
    raise NotImplementedError("TODO(task 9): the guard, then one embedding call for up to 20 texts")


def embed_chunks(conn, limit: int | None = None) -> tuple[int, int]:
    """Embed the rows of ai.chunks WHERE embedding IS NULL, BATCH_SIZE at a time.

    - Call register_vector(conn) from pgvector.psycopg first, and pass each
      vector as pgvector.Vector(values).
    - Get the names once with load_names(conn) for the guard.
    - Send each chunk as document_text(note_type, text); the note type is in
      clean.visit_notes.
    - Save each vector in its row, commit after every batch, and sleep
      PAUSE_SECONDS after each call. Stop after `limit` chunks when it is given.

    A run that stops part-way (HTTP 429) loses no finished batch, and the next run
    continues where it stopped. Returns (chunks embedded, calls made).
    """
    # TODO(task 11): set embedded_at = now() in the same UPDATE as each vector.
    raise NotImplementedError("TODO(task 9): embed the chunks that have no embedding yet")


def main(argv: list[str] | None = None) -> None:
    """Embed the chunks that have no embedding yet. --limit N stops after N chunks."""
    parser = argparse.ArgumentParser(description="Embed CareLine's chunks into pgvector.")
    parser.add_argument("--limit", type=int, help="embed at most this many chunks (try --limit 20 first)")
    args = parser.parse_args(argv)
    # Imported here, so importing this module never loads the database driver.
    from careline.db import connect

    with connect() as conn:
        embedded, calls = embed_chunks(conn, limit=args.limit)
    print(f"embedded {embedded} chunks in {calls} calls")


if __name__ == "__main__":
    main()
