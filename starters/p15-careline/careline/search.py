"""Find visits by meaning: nearest-neighbour search over the embedded chunks.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run --env-file .env python -m careline.search
"""

from pathlib import Path

QUESTIONS_FILE = Path(__file__).resolve().parents[1] / "evalset" / "questions.csv"


def top_chunks(conn, question: str, k: int = 3) -> list[tuple[str, int, float, str]]:
    """Return the k chunks nearest to the question, nearest first.

    Embed question_text(question) with embed_texts() (careline.embed): the same
    model and vector size as the chunks, and the guard checks the question too
    (names from load_names(conn)). Then find the nearest chunks by cosine distance
    with SELECT ... ORDER BY embedding <=> %s LIMIT %s. The connection needs
    register_vector(conn) from pgvector.psycopg.

    Returns (note_id, chunk_no, distance, text) tuples.
    """
    raise NotImplementedError("TODO(task 9): embed the question, then ORDER BY embedding <=> %s LIMIT %s")


def main() -> None:
    """For every row of QUESTIONS_FILE (read_questions() in careline.evaluate), print
    the question, its expected note, and the note_id and distance of its top 3
    chunks. Paste the output under "## Ten questions" in evidence.md."""
    raise NotImplementedError("TODO(task 9): print the top 3 chunks of every test question")


if __name__ == "__main__":
    main()
