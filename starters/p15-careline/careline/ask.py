"""Ask the chat model a question, with or without the chunks that search found (task 9's AI move)."""


def ask(question: str, chunks: list[tuple[str, int, float, str]], names: list[str]) -> str:
    """Answer a question with ONE call to the chat model (CHAT_MODEL); return the answer text.

    - `chunks` are the tuples top_chunks() returns, or [] to ask without them.
      With chunks, put each chunk's note_id and text above the question, and ask
      the model to answer only from them and to name the note it used.
    - Call assert_masked() (careline.mask) first, on the question and on every
      chunk's text.
    - The call is client.interactions.create(..., store=False), as in models.md.
      Import google.genai inside this function.

    For the AI move, ask 3 questions with and without their top 3 chunks and log
    both answers in AI_LOG.md. You may add a main() here to run that.
    """
    raise NotImplementedError("TODO(task 9): the guard, then one chat call with or without the chunks")
