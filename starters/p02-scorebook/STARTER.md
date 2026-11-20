# Scorebook Guided starter (P2)

This folder is the start of your `scorebook/` product folder. It saves you the set-up
work: the uv project, the folders, `psql.sh`, the loader's function names with what each
must do, and SQL files with their headings. It holds no solutions: no column types, no
keys you must choose, no query and no loading code.

## What is included

| Path | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A uv project on Python 3.12 with `psycopg[binary]` already added. |
| `.gitignore`, `.env.example` | Keeps `data/` and `.env` out of Git. `.env.example` holds `DATABASE_URL`. |
| `psql.sh` | The one line from task 7, step 4: psql on the `scorebook` database in the data lab. |
| `sql/schema.sql` | The drop line, `players` written out as an example, and the other three tables as shells with their column names. |
| `sql/checks.sql` | The six check headings for task 9. |
| `sql/indexes.sql`, `sql/views.sql`, `sql/rollback_demo.sql` | Headings for tasks 22, 23 and 24. |
| `sql/queries/` | Empty. Each query file is an answer, so you create them all. |
| `load/load_matches.py` | The loader's six functions, `DATABASE_URL`, `DELIVERY_COLUMNS`, and the row-count printout. |
| `load/reload_match.py` | The reload's three functions for task 24. |
| `docs/design.md` | The headings for task 7's design notes. |

No data is included. Task 7 step 2 downloads it into `data/matches/`.

## How to copy it in

In task 7, run this in Git Bash inside the task 7 folder, instead of step 1
(`scorebook/`, its folders and `uv init` are already done):

```bash
cp -r ~/de-kit/starters/p02-scorebook scorebook
cd scorebook
```

Do not run `uv init` in it: `pyproject.toml` exists, so uv would stop with an error.
Then carry on with step 2. From task 8 on, copy your `scorebook/` folder forward as each
brief says (without `.venv/`).

## How to run it

From the `scorebook/` folder, with the data lab's `core` profile running:

```bash
uv sync                                   # installs Python 3.12 and psycopg
bash psql.sh < sql/schema.sql             # creates players and three empty shells
bash psql.sh -a < sql/checks.sql          # prints the headings: no checks yet
uv run python load/load_matches.py data/matches   # TODO(task 8) until you write it
```

Every `.sql` file runs as shipped. Task 8, step 1 is done for you: `psycopg[binary]` is
in `pyproject.toml` and `.env.example` exists. Start task 8 at step 2.

## Every TODO

| Task | File | What you write |
|---|---|---|
| 7 | `sql/schema.sql` | Types, `NOT NULL`, keys and the check for `matches`, `innings` and `deliveries` |
| 7 | `docs/design.md` | One row per table, and your four reasons |
| 8 | `load/load_matches.py` | `read_match`, `player_rows`, `match_row`, `innings_rows`, `delivery_rows`, and the load inside `main` |
| 9 | `sql/checks.sql` | The six checks |
| 22 | `sql/indexes.sql` | The index and `ANALYZE` |
| 23 | `sql/views.sql` | The drops, three views and the materialised view |
| 24 | `load/reload_match.py` | `count_rows`, `reload_match` and `main` |
| 24 | `sql/rollback_demo.sql` | The transaction you undo by hand |

These build tasks have no TODO in the starter, on purpose:

- Tasks 11, 19, 20 and 21: every file in `sql/queries/` (`q01` to `q15`) is an answer.
  The brief names each file and its question. Create each one yourself.
- Task 12: you rewrite your own three longest queries and copy the old ones to `sql/before/`.
- Task 22: `sql/queries/q16_batter_seasons.sql` and `sql/explain_q16.sql` are your query.

Run `grep -rn "TODO(task" .` to see what is left. Task 25 (the wrap-up) has no TODO: it
is your README, your demo and your answers.

## What you still write yourself

- Every column type and key, every check, every query, every view, and every function body.
- `docs/checks.md`, `docs/rewrites.md`, `docs/run-rate.md`, `docs/partnerships.md`,
  `docs/streaks.md`, `docs/performance.md`, `docs/leaderboards.md` and `docs/reload.md`.
- In the task folder: `evidence.md`, `AI_LOG.md` and `EXPLAIN.md`.
- `scorebook/README.md`, in task 25.
