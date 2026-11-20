# The model key and the model names for CareLine part 2 (P15)

CareLine part 2 uses two models from Google's Gemini API, both on the free tier:

| Setting in `.env` | Value | What it does |
|---|---|---|
| `CHAT_MODEL` | `gemini-3.5-flash-lite` | Answers questions and pulls facts out of text |
| `EMBED_MODEL` | `gemini-embedding-2` | Turns a text into a vector (a list of numbers) |
| vector size N | **768** | The length of each vector. Your `vector(N)` column is `vector(768)` |

Checked on 13 November 2026 on Google's pages (the Gemini API docs moved from `ai.google.dev` to `aistudio.google.com/docs`; the old addresses redirect):

- `gemini-3.5-flash-lite` is a **stable** model and free on the free tier. The models page says: "For any new projects, use our latest models: Gemini 4 Hydrogen or 3.5 Flash-Lite."
- `gemini-3.8-flash` is also stable and free. It is slower, and it may give better answers. You may use it as `CHAT_MODEL` instead.
- The docs' own examples now use `gemini-4-hydrogen`, which is also free. The course was not tested with it, so stay with `gemini-3.5-flash-lite`.
- `gemini-2.5-flash` and `gemini-2.5-pro` are deprecated. From 1 December 2026 Google sends their calls to newer models. Do not use them.
- `gemini-embedding-2` is the newest embedding model. Its vectors have 3,072 numbers unless you ask for fewer (128 to 3,072; Google recommends 768, 1,536 or 3,072). CareLine asks for 768, with `output_dimensionality=768`, because a pgvector index works only up to 2,000 numbers. At 768 the model scales the vector to length 1 itself.

Model names are not secrets. You may put them in `.env.example` and in your README.
Model names change about twice a year. If a call answers `404` or `model not found`, check the [models page](https://aistudio.google.com/docs/models) and tell your mentor.

## 1. Get a free key

1. You need a Google account. Google's terms say you must be **18 or older** to use the API. India is on the list of countries where it works.
2. Open https://aistudio.google.com/apikey and sign in. Accept the terms.
3. Click **Create API key**. Copy the key.
4. Do not add a billing account. Without one, you stay on the free tier and nothing can cost money.

Keep the key in a `.env` file in the folder where you run your code (`~/try-ai` for the cards, `careline/` from task 9):

```bash
GEMINI_API_KEY=paste-your-key-here
CHAT_MODEL=gemini-3.5-flash-lite
EMBED_MODEL=gemini-embedding-2
```

No spaces and no quotes around the key. `.env.example` holds the same names with **no key**:

```bash
GEMINI_API_KEY=
CHAT_MODEL=gemini-3.5-flash-lite
EMBED_MODEL=gemini-embedding-2
```

**Quotes in `.env`.** Put double quotes around any value that has spaces, such as P13's line:

```bash
_PIP_ADDITIONAL_REQUIREMENTS="great_expectations pyyaml pandas psycopg[binary]"
```

uv stops reading `.env` at the first unquoted value with spaces (`warning: Failed to parse environment file`), so every setting after it is lost, your key too. Docker Compose removes the quotes, so Airflow still gets the value. Task 8 adds the quotes.

Never commit `.env`. Check that Git ignores it before your first commit:

```bash
git check-ignore -v .env
```

It must print the `.gitignore` line that ignores `.env` (CareLine's `.gitignore` has had it since P13). If it prints nothing, add `.env` to `.gitignore` first.
A key that reaches GitHub can be found and misused within minutes. If that happens, delete the key in AI Studio and create a new one.

The Python package `google-genai` reads `GEMINI_API_KEY` by itself. It also reads `GOOGLE_API_KEY`, and if both are set, `GOOGLE_API_KEY` wins. Keep only `GEMINI_API_KEY`.

Install the package in your project with `uv add google-genai`. The examples below were checked with `google-genai` 3.3.0, the newest on 13 November 2026 (`kit/VERSIONS.md`). The chat calls need version 2.3.0 or newer.

## 2. Only masked text is ever sent to a model

On the free tier, Google may use what you send and what the model answers to improve its products. Google's terms (effective 23 March 2026) say:

> "Do not submit sensitive, confidential, or personal information to the Unpaid Services."

and "human reviewers may read, annotate, and process your API input and output".

CareLine's notes are made up **and** masked:

- Task 7 masks every note into `clean.visit_notes` before anything else happens: emails, then phone numbers, then names. Its scan proves that clean holds no personal data (`data/clinic/README.md` has the patterns).
- Every text that goes to a model comes from `clean.visit_notes` or from your own questions, never from `raw`.
- From task 9, **every model call goes through one guard**, `assert_masked(texts, names)` in `careline/mask.py`. It runs `find_personal()` on each text and raises `ValueError` when anything is found, naming the kind (phone, email or name), never the value. Call it first, in each function that talks to a model:

  ```python
  def embed_texts(texts, names):
      assert_masked(texts, names)          # the first line: nothing leaves your laptop before this passes
      # ... then the one embedding call of section 4
  ```

  `ask()` and `extract_batch()` start the same way, with every text they are about to send: the question, the chunks' texts, the notes' masked texts.
  A test shows the guard refusing a phone number, so nobody can remove it by accident.
- The try-its of the learn cards send only the cards' own made-up sentences. Never paste a note from `raw`, a key or a password into a model, into `AI_LOG.md` or into a chat.

## 3. Chat, with token counts

Save this as `try_llm.py` in `~/try-ai` and run it with `uv run --env-file .env python try_llm.py`:

```python
"""Ask the chat model one question and print its token counts.

Run it with: uv run --env-file .env python try_llm.py
"""
import os

from google import genai

MODEL = os.environ.get("CHAT_MODEL", "gemini-3.5-flash-lite")
client = genai.Client()            # reads GEMINI_API_KEY from the environment

context = ""                       # card 1, step 5: put "The CareLine team meets in room 4 on Thursdays." here
question = "In which room does the CareLine team meet on Thursdays?"
prompt = f"{context}\n\n{question}".strip()

before = client.models.count_tokens(model=MODEL, contents=prompt)
print("tokens in the prompt (counted before the call):", before.total_tokens)

interaction = client.interactions.create(model=MODEL, input=prompt, store=False)
print(interaction.output_text)
print("input tokens:", interaction.usage.total_input_tokens)
print("output tokens:", interaction.usage.total_output_tokens)
print("total tokens:", interaction.usage.total_tokens)
```

- `client.interactions.create` is the call Google's docs recommend for new projects. The older `client.models.generate_content` still works.
- `interaction.output_text` is the model's answer as text.
- **Token counts.** `count_tokens` counts the prompt before you send it. After the call, `interaction.usage` holds the counts the call used. `total_tokens` can be larger than input plus output, because a model can also spend tokens thinking (`interaction.usage.total_thought_tokens`).
- Google's rules of thumb: a token is about 4 characters, and 100 tokens are about 60 to 80 English words.
- `store=False` asks Google not to keep the conversation. Without it, the free tier keeps each call for 1 day.
- To give the model a role, add `system_instruction="..."` to `interactions.create`. In `ask()` (task 9) a role such as "Answer only from the notes below; say so if they do not answer the question" helps.

## 4. Embeddings: one vector for each text

Save this as `try_embed.py` and run it with `uv run --env-file .env python try_embed.py`:

```python
"""Embed three texts, each as its own item, and print the length of each vector.

Run it with: uv run --env-file .env python try_embed.py
"""
import os

from google import genai
from google.genai import types

MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-2")
SIZE = 768                         # the vector size N: your vector(N) column must match it
client = genai.Client()


def embed(texts: list[str]) -> list[list[float]]:
    """One call for up to 20 texts. Each text is its own Content item, so each gets its own vector."""
    result = client.models.embed_content(
        model=MODEL,
        contents=[types.Content(parts=[types.Part.from_text(text=t)]) for t in texts],
        config=types.EmbedContentConfig(output_dimensionality=SIZE),
    )
    vectors = [e.values for e in result.embeddings]
    if len(vectors) != len(texts) or any(len(v) != SIZE for v in vectors):
        raise ValueError(f"asked for {len(texts)} vectors of size {SIZE}, got {[len(v) for v in vectors]}")
    return vectors


texts = [
    "task: question answering | query: Which patient hurt a knee on the stairs?",
    "title: consultation note | text: Pain in the right knee since a fall on the steps at home.",
    "title: consultation note | text: Itchy rash on both arms for a week.",
]
for text, vector in zip(texts, embed(texts)):
    print(len(vector), text)
```

It prints `768` three times. Card 3 then compares the question's vector with each note's vector.

### The plain-list trap

With `gemini-embedding-2`, a plain list of strings is **one** input, not three. Google's embeddings page says: "Adding multiple inputs directly to the `contents` parameter produces one aggregated embedding for all inputs."

```python
result = client.models.embed_content(model=MODEL, contents=texts,
                                     config=types.EmbedContentConfig(output_dimensionality=SIZE))
print(len(result.embeddings))      # 1, not 3: one vector for all three texts together
```

No error tells you. That is why `embed()` above wraps each text in its own `types.Content` item and checks that one vector came back for each text. Your `embed_texts()` (task 9) does the same, after `assert_masked()`.
(The older `gemini-embedding-001` returns one vector per string for a plain list. Do not mix the two models: vectors from different models cannot be compared.)

### The text formats for chunks and questions

`gemini-embedding-2` has no `task_type` setting ("You cannot use the `task_type` field for the `gemini-embedding-2` model"). Instead, the task goes into the text itself. Use exactly these two formats, from Google's embeddings page:

| What you embed | Format | CareLine example |
|---|---|---|
| A chunk (a document) | `title: {title} \| text: {content}` | `title: consultation note \| text: Pain in the left knee for three months. Clicking when bending the knee. ...` |
| A question | `task: question answering \| query: {content}` | `task: question answering \| query: Which patient hurt a knee on the stairs?` |

In CareLine a chunk's title is its note type: `title: triage note | text: ...` or `title: consultation note | text: ...`, with the chunk's masked text after `text:`. (Guided: the starter's `document_text()` and `question_text()` in `embed.py` build exactly these.)
Embed every chunk and every question with the **same model** and the **same size**. A vector from one model means nothing to another.

## 5. JSON that follows a schema

Save this as `try_extract.py`. Run `uv add pydantic` first, then `uv run --env-file .env python try_extract.py`:

```python
"""Ask the chat model for JSON that follows a Pydantic model's schema, then parse it.

Run it with: uv run --env-file .env python try_extract.py
"""
import os

from google import genai
from pydantic import BaseModel

MODEL = os.environ.get("CHAT_MODEL", "gemini-3.5-flash-lite")
client = genai.Client()


class Visit(BaseModel):
    symptom: str | None
    body_area: str | None
    days: int | None


text = "Pain in the left knee for two weeks after a fall. Walks with a limp."
interaction = client.interactions.create(
    model=MODEL,
    input=f"Extract the visit from this note. Use null for a fact the note does not state.\n\n{text}",
    response_format={"type": "text", "mime_type": "application/json", "schema": Visit.model_json_schema()},
    store=False,
)
print(interaction.output_text)     # the raw JSON: print it when parsing fails
visit = Visit.model_validate_json(interaction.output_text)
print(visit)
```

- `Visit.model_json_schema()` turns the Pydantic model into a JSON schema. The model must answer in that shape.
- `Visit.model_validate_json(...)` reads the answer and checks every type.
- **A fixed list of words.** For task 10's urgency, use `typing.Literal`: Pydantic turns it into the schema's `enum`, and Google's structured-output page uses `Literal` in its own Python examples.

  ```python
  from typing import Literal

  class VisitFacts(BaseModel):
      note_id: str
      symptom: str | None
      body_area: str | None
      urgency: Literal["routine", "soon", "urgent"] | None
  ```

- For many rows in one call (task 10), make a second model, `class FactsBatch(BaseModel): rows: list[VisitFacts]`, and send its schema. Put each note's `note_id` next to its masked text in the prompt, so the model can say which row is which.
- Google's warning: "While output is syntactically correct JSON, always validate values in your application." A schema fixes the shape, not the truth: your `validate()` checks the values.
- Google ignores some schema rules, such as `minLength` and `maxLength`, without an error. Check those in your own code. A very large or deeply nested schema is refused with `400 INVALID_ARGUMENT`.

## 6. Free-tier limits and HTTP 429

**The limits: see AI Studio after sign-in.** Google no longer prints the free-tier numbers (requests per minute, tokens per minute, requests per day). Its rate-limits page says they "can be viewed in Google AI Studio", at https://aistudio.google.com/rate-limit. That page also shows how much of today's quota you have used. Checked on 13 November 2026; nobody in the course team had a key that day, so this guide gives no numbers yet.

What Google's rate-limits page states:

- "Rate limits are applied per project, not per API key." Two keys in one Google Cloud project share one limit.
- The daily limit resets at midnight Pacific time: **13:30 India time** from November to early March, **12:30** from March to early November.
- Over a limit, a call fails with HTTP `429` and the status `RESOURCE_EXHAUSTED`.
- Google does not say whether one embedding call with 20 texts counts as 1 request or 20.

What P15 needs (30 days of notes, about 750 chunks at 60 words):

| Task | Calls |
|---|---|
| 9 | about 40 embedding calls of 20 chunks, 10 single questions, and 6 chat calls for the AI move |
| 10 | about 30 extraction calls of 20 notes |
| 11 | 2 or 3 embedding calls and 1 or 2 extraction calls a day of notes |
| 12 | about 30 embedding calls (every note again, one chunk each at 200 words) and 40 single questions |

What to do in CareLine:

- **Pause 7 seconds after each call** in a loop (`time.sleep(7)`). That keeps you under about 9 calls a minute. When you can see your real limits in AI Studio, you may shorten it.
- **On HTTP 429**, stop. Wait one minute and run the step again: `embed.py` and `extract.py` continue where they stopped. If it fails again at once, the daily limit is used up. Wait until 13:30 (or 12:30) India time.
- Try every model step with `--limit 20` first.
- Never delete embedded chunks to "start clean": one full embedding pass is about 750 chunks.
- No quota left? Task 12 says what to compare instead. Never share a key: your mentor pairs you with another student for the day.

## Sources

- Models (Gemini API docs): https://aistudio.google.com/docs/models
- Pricing, free tier column (Gemini API docs): https://aistudio.google.com/docs/pricing
- Rate limits (Gemini API docs): https://aistudio.google.com/docs/rate-limits
- Using Gemini API keys (Gemini API docs): https://aistudio.google.com/docs/api-key
- Embeddings (Gemini API docs): https://aistudio.google.com/docs/embeddings
- Text generation (Gemini API docs): https://aistudio.google.com/docs/text-generation
- Understand and count tokens (Gemini API docs): https://aistudio.google.com/docs/tokens
- Structured outputs (Gemini API docs): https://aistudio.google.com/docs/structured-output
- Gemini API terms of service: https://aistudio.google.com/docs/terms
