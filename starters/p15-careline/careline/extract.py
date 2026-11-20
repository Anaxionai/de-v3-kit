"""Extract symptom, body area and urgency from the masked notes with the chat model, and check every row.

Run it from the careline/ folder, with the data lab's core profile running:

    uv run --env-file .env python -m careline.extract --limit 20
    uv run --env-file .env python -m careline.extract

The JSON (structured output) call is in the kit's data/clinic/models.md; the body
areas and the urgency words are in data/clinic/README.md.
"""

from typing import Literal

from pydantic import BaseModel

NOTES_PER_CALL = 20  # masked notes in one call to the chat model

# The 13 body areas of the kit's data/clinic/README.md, exactly as validate() accepts them.
BODY_AREAS = [
    "head", "throat", "chest", "abdomen", "skin", "whole body", "back",
    "neck", "shoulder", "wrist", "hip", "knee", "ankle",
]


class VisitFacts(BaseModel):
    """One note's facts as the model reads them. None means the note does not state it.

    Given as a type (task 10, step 1), so that the tests can build rows.
    """

    note_id: str
    symptom: str | None
    body_area: str | None
    urgency: Literal["routine", "soon", "urgent"] | None


class FactsBatch(BaseModel):
    """The answer to one call: the facts of up to NOTES_PER_CALL notes (task 10, step 2)."""

    rows: list[VisitFacts]


def extract_batch(notes: list[tuple[str, str]], names: list[str]) -> list[VisitFacts]:
    """Extract the facts of up to NOTES_PER_CALL notes with ONE call to the chat model.

    `notes` is a list of (note_id, masked_text) pairs from clean.visit_notes.
    - Call assert_masked() (careline.mask) on the texts first.
    - Ask for JSON that follows FactsBatch.model_json_schema(), and for null when
      a note does not state a fact. Put each note_id next to its text.
    - Parse the answer with FactsBatch.model_validate_json() and return its rows.
    The model may skip a note or return a note_id you did not send: return what
    it gave, and let main() record it.
    """
    raise NotImplementedError("TODO(task 10): the guard, then one JSON call for up to 20 notes")


def validate(facts: VisitFacts, text: str) -> list[str]:
    """Check one extracted row against its note's text; return its problems.

    An empty list means the row may enter ai.visit_facts. One problem for each
    rule the row breaks:
    - a body_area that is not None and not in BODY_AREAS;
    - "symptom not in text": a symptom that is not None and not in the text,
      ignoring case and extra spaces (compare " ".join(s.lower().split()));
    - urgency "urgent" when the text holds neither "urgent" nor "emergency".
    A pure function: no database, no model.
    """
    raise NotImplementedError("TODO(task 10): check one row in code")


def main(argv: list[str] | None = None) -> None:
    """Extract the facts of every note that has no row at its current version in
    ai.visit_facts or ai.facts_rejected, NOTES_PER_CALL notes in each call.

    Take an optional --limit N (argparse). Delete the older rows of those notes
    first. A row with no problems goes to ai.visit_facts; the others go to
    ai.facts_rejected with their problems. Add "no row returned" for a note the
    model skipped, and "not sent", with no version, for a note_id it invented.
    Print the calls made and the rows accepted and rejected: a repeat run makes
    0 calls. Connect with careline.db.connect(), imported inside this function.
    """
    raise NotImplementedError("TODO(task 10): extract, validate and store, only for notes with no row yet")


if __name__ == "__main__":
    main()
