# Guided add-on: P15 CareLine part 2

This is an **add-on** to your own `careline/` folder from P13, for module 17 (data for AI). It holds only the **new** files that part 2 needs, at their places inside `careline/`: the masking, chunking, embedding, search, extraction, refresh and evaluation modules with every function named and described, two SQL files with their headers, the test files with skipped tests, and the test set's header. **Your P13 files stay as they are**: the add-on never replaces one.

Every function, query, table and test a task asks for is still yours to write.

## Add it to your folder (task 7)

Task 7 copies your `careline/` folder forward from P13 first. Then, in Git Bash, inside task 7's folder:

```bash
git -C ~/de-kit pull
cp -rn ~/de-kit/starters/p15-careline/. careline/
cd careline
```

`-n` never overwrites a file you already have, and `p15-careline/.` copies the add-on's contents into your `careline/`, each file at its place. This file, `STARTER-P15.md`, lands in `careline/` too: it is not your README. Copy the add-on **once**; from task 8 on, copy your `careline/` folder forward as each brief says.

The add-on has no `pyproject.toml`, `uv.lock`, `.env.example`, `README.md` or `.gitignore`: you have yours from P13. So run the briefs' `uv add` lines like everyone else.

## What is included

| Path in `careline/` | What it is |
|---|---|
| `sql/02_notes.sql` | The two notes tables, named in comments (task 7) |
| `sql/03_ai.sql` | The `ai` schema in sections, one TODO per task (tasks 8 to 11) |
| `careline/mask.py` | `PHONE` (P13's pattern) and `EMAIL` given, `load_names(conn)` complete; `find_personal()`, `mask_text()`, `assert_masked()` to write |
| `careline/notes.py` | `NOTES_DIR` and `main()` with `--scan` given; `load_notes()`, `mask_new()`, `scan()` to write |
| `careline/chunk.py` | `main()` reading `CHUNK_MAX_WORDS` (default 60) given; `split_text()`, `chunk_notes()` to write |
| `careline/embed.py` | `VECTOR_SIZE = 768`, `BATCH_SIZE = 20`, `PAUSE_SECONDS = 7`, `document_text()`, `question_text()` and `main()` with `--limit` given; `embed_texts()`, `embed_chunks()` to write |
| `careline/search.py` | `QUESTIONS_FILE` given; `top_chunks()`, `main()` to write |
| `careline/ask.py` | `ask()` to write (task 9's AI move) |
| `careline/extract.py` | `BODY_AREAS` (the 13 values), `VisitFacts` and `FactsBatch` given as types; `extract_batch()`, `validate()`, `main()` to write |
| `careline/refresh.py` | `changed_notes()`, `main()` to write |
| `careline/evaluate.py` | `read_questions()` given; `hit_rate()`, `main()` to write |
| `tests/test_mask.py`, `test_chunk.py`, `test_extract.py`, `test_refresh.py`, `test_evaluate.py` | Skipped tests, each with a docstring saying what it checks |
| `evalset/questions.csv` | The header `id,question,expected_note` and one example row to replace |

`evidence.md` and `AI_LOG.md` live in each task folder, next to `careline/`.

## Lines you add to your own files

| Task | File | What to add |
|---|---|---|
| 8 | `.env` and `.env.example` | `CHUNK_MAX_WORDS=60`, and double quotes around the `_PIP_ADDITIONAL_REQUIREMENTS` value: `_PIP_ADDITIONAL_REQUIREMENTS="great_expectations pyyaml pandas psycopg[binary]"` |
| 9 | `pyproject.toml`, `uv.lock` | Run `uv add google-genai pgvector pydantic` |
| 9 | `.env` | `GEMINI_API_KEY=<your key>`, `EMBED_MODEL=gemini-embedding-2`, `CHAT_MODEL=gemini-3.5-flash-lite` |
| 9 | `.env.example` | The same three names, with **no key**: `GEMINI_API_KEY=` |
| 13 | `README.md` | The full README for both parts (the wrap-up) |

## How to run it

In `careline/`, with the data lab's core profile running (`docker compose --profile core up -d` in `~/de-kit/datalab`):

```bash
uv run pytest -q                                   # your P13 tests pass; the new ones are skipped
uv run ruff check
uv run python -m careline.db sql/02_notes.sql      # each SQL file, once you have written it
uv run python -m careline.notes                    # then --scan
uv run --env-file .env python -m careline.chunk    # and embed, search, extract, refresh, evaluate
```

Until you write a function, it stops with `NotImplementedError` and its task number. The modules import the database driver and `google-genai` only inside functions, so `uv run pytest` runs before task 9's `uv add` and on a laptop where Windows blocks the driver. Keep it that way in the code you write. If Windows says an Application Control policy blocked a file, read the kit's `setup/windows.md`; `uv run python -m pytest` runs the same tests.

## Your TODOs

Find them with `grep -rn "TODO(task" careline sql tests evalset` in `careline/`.

| Task | File | What you write |
|---|---|---|
| 7 | `sql/02_notes.sql` | `raw.visit_notes` and `clean.visit_notes` |
| 7 | `careline/mask.py` | `find_personal()`, `mask_text()` |
| 7 | `careline/notes.py` | `load_notes()`, `mask_new()`, `scan()` |
| 7 | `tests/test_mask.py` | The five masking tests |
| 8 | `sql/03_ai.sql` | Schema `ai` and `ai.chunks` |
| 8 | `careline/chunk.py` | `split_text()`, `chunk_notes()` |
| 8 | `tests/test_chunk.py` | The four tests |
| 9 | `sql/03_ai.sql` | `CREATE EXTENSION` and the `embedding vector(768)` column |
| 9 | `careline/mask.py` | `assert_masked()` |
| 9 | `careline/embed.py` | `embed_texts()`, `embed_chunks()` |
| 9 | `careline/search.py`, `careline/ask.py` | `top_chunks()`, `main()`, `ask()` |
| 9 | `tests/test_mask.py`, `evalset/questions.csv` | The two guard tests; your 10 questions |
| 10 | `sql/03_ai.sql` | `ai.visit_facts`, `ai.facts_rejected` |
| 10 | `careline/extract.py`, `tests/test_extract.py` | `extract_batch()`, `validate()`, `main()`; the four tests |
| 11 | `sql/03_ai.sql`, `careline/embed.py` | `embedded_at`, set with each vector |
| 11 | `careline/refresh.py`, `tests/test_refresh.py` | `changed_notes()`, `main()`; the three tests |
| 12 | `careline/evaluate.py`, `tests/test_evaluate.py` | `hit_rate()`, `main()`; the tests |
| 12 | `evalset/questions.csv` | 20 questions for 20 different story notes |

Task 13 (the wrap-up) has no TODO.

## What you still write yourself

- Every table, query, function body and test in the table above.
- Your questions, in your own words, in `evalset/questions.csv`.
- `evidence.md` and `AI_LOG.md` in each task folder, and in task 13 `careline/README.md`, the screenshots and `EXPLAIN.md`.

## Data and privacy

This add-on holds no data. Make the notes with `make_clinic.py --notes` (task 7). The names, phone numbers and email in `tests/` are made up. Only masked text from `clean.visit_notes` ever goes to a model; the kit's `data/clinic/models.md` says why.
