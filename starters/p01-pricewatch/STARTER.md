# PriceWatch Guided starter (P1)

This folder is the start of your `pricewatch/` product folder. It saves you the set-up
work: the uv project, the file layout, the function names with what each must do, and
empty tests. It holds no solutions. Every function stops with
`NotImplementedError("TODO(task NN): ...")` until you write it.

## What is included

| Path | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A uv project on Python 3.12 with no packages yet. pytest and ruff are dev tools; pytest is set up to find `tests/` and your package. |
| `.gitignore`, `.env.example` | Keeps `data/`, `.env` and caches out of Git. `.env.example` names the settings, never their values. |
| `DATA.md` | The headings for the data's source and attribution. |
| `fetch.py`, `load.py`, `clean.py`, `units.py` | Week 1: one file per task, at the top of `pricewatch/`, as the briefs describe. |
| `later/` | Week 2 files, waiting to be moved into your package (see below). |
| `tests/` | Empty tests for task 22. They are skipped, so `uv run pytest` passes now. |

No data is included. Use your own download, or the kit's sample month `~/de-kit/data/prices/sample`.

## How to copy it in

In task 8, step 1, run these in Git Bash inside the task 8 folder, instead of
`mkdir pricewatch`, `cd pricewatch` and `uv init --bare --python 3.12`:

```bash
cp -r ~/de-kit/starters/p01-pricewatch pricewatch
cd pricewatch
```

Run `git pull` in `~/de-kit` first, as the brief says. Then carry on with step 2. From task 9 on, copy your `pricewatch/` folder forward as
each brief says (without `.venv/`).

## How to run it

From the `pricewatch/` folder:

```bash
uv sync                         # installs Python 3.12 and the dev tools
uv run pytest                   # 11 skipped: the tests wait for task 22
uv run ruff check               # checks your code for mistakes
uv run python fetch.py ~/de-kit/data/prices/sample   # TODO(task 8) until you write it
```

`uv run python -m pytest` does the same as `uv run pytest`.

## Week 1 files, then the package

In week 1 the four modules sit at the top of `pricewatch/` and import each other by
file name, for example `from load import read_all`. Run each one as the brief says,
such as `uv run python load.py data/raw`.

Task 12 makes them a package. Do the brief's steps, and use the starter's `cli.py`
instead of creating a new one. Move each `later/` file in when its task starts:

| Task | Move |
|---|---|
| 12 | `mv later/cli.py pricewatch/` (after you create `pricewatch/pricewatch/` and move the four modules in) |
| 19 | `mv later/frame.py pricewatch/` (after `uv add pandas`) |
| 20 | `mv later/report.py pricewatch/` |
| 23 | `mv later/settings.py pricewatch/` and `mv later/settings.toml .` |
| 24 | `mv later/chart.py pricewatch/` (after `uv add matplotlib`), then `rmdir later` |

The paths in the table are from the product folder. After the move, change the imports
to the package form: `from pricewatch.load import read_all`.

In task 22, step 1 is done: pytest, `pythonpath` and `testpaths` are already in
`pyproject.toml`, and `tests/` exists. Start at step 2.

## Every TODO

Files are named where the starter puts them.

| Task | File | What you write |
|---|---|---|
| 8 | `fetch.py` | `fetch_month(source, raw_dir)` and the printout under `__main__` |
| 8 | `DATA.md` | Dataset, publisher, page, month and attribution |
| 9 | `load.py` | `parse_row`, `read_prices`, `read_all` and the printout (`BadRow` is given) |
| 10 | `clean.py` | `tidy`, `name_key`, `clean_market`, `clean_commodity`, `clean_records`, your alias tables, the checks and five `assert` lines |
| 11 | `units.py` | `UNITS`, `MIN_QUINTAL_PRICE`, `to_rupees_per_kg`, `convert_record`, `convert_all`, `save_clean`, the printout and three `assert` lines |
| 12 | `later/cli.py` | `main()` with `fetch`, `load` and `report`, and the usage line |
| 19 | `later/frame.py`, `later/cli.py` | `load_frame`, `clean_frame`, the `CompareResult` fields, `compare`, the `compare` command |
| 20 | `later/report.py`, `later/cli.py` | `MIN_DAYS`, `daily_prices`, `weekly_prices`, `weekly_extremes`, the new `report` |
| 21 | `later/report.py`, `later/cli.py` | `FILL_LIMIT`, `JUMP_LIMIT`, `series_table`, `fill_gaps`, `find_jumps`, gaps and jumps in `report` |
| 22 | `tests/test_clean.py`, `tests/test_units.py`, `tests/test_load.py` | Every test and the `bad_file` fixture |
| 23 | `later/settings.py`, `later/settings.toml`, `.env.example`, `later/cli.py` | `load_settings`, the six settings, `PRICEWATCH_LOG_LEVEL`, logging and the run report |
| 24 | `later/chart.py`, `later/cli.py` | `chart_table`, the chart itself and the `chart` command |

Run `grep -rn "TODO(task" .` to see what is left. Task 25 (the wrap-up) has no TODO: it
is your README, your demo and your answers.

## What you still write yourself

- Every function body, every printout and every rule. The docstrings say what each
  function takes and returns, and the cases the reviewer checks.
- Your choices: the alias tables, the unclear-unit threshold, and the limits.
- The tests in task 22.
- `sample/raw_head.csv`, `sample/clean_head.csv` and everything in `reports/`.
- In the task folder: `evidence.md`, `NOTES.md`, `AI_LOG.md` and `EXPLAIN.md`.
- `pricewatch/README.md`, in task 25.
