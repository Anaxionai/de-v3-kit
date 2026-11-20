"""Measure retrieval with the test set: the hit rate at 1 and at 3 (task 12).

Run it from the careline/ folder, with the data lab's core profile running:

    uv run --env-file .env python -m careline.evaluate
"""

import csv
from pathlib import Path


def read_questions(path: str | Path) -> list[dict[str, str]]:
    """Read evalset/questions.csv: one dict per row, with the keys id, question and expected_note."""
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def hit_rate(results: list[tuple[str, list[str]]], k: int) -> float:
    """Return the share of questions whose expected note is among their first k chunks.

    `results` holds one (expected_note, note_ids) pair for each question, where
    note_ids are the note ids of the retrieved chunks in rank order, nearest first.
    For example [("N1", ["N1", "N4", "N9"]), ("N2", ["N4", "N9", "N2"])] gives 0.5
    at k=1 and 1.0 at k=3. An empty list gives 0.0. A pure function.
    """
    raise NotImplementedError("TODO(task 12): the hit rate at k")


def main() -> None:
    """Run top_chunks(conn, question, k=3) (careline.search) for every question in
    evalset/questions.csv. Print the hits at 1 and at 3 as counts of all the
    questions (such as "hits at 3: 17 of 20"), the ids of the questions that
    missed, and the mean number of words in the 3 chunks sent with a question."""
    raise NotImplementedError("TODO(task 12): measure the test set")


if __name__ == "__main__":
    main()
