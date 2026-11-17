# Guided starter: P8 EditStream

This folder is the start of your `editstream/` product folder for module 10 (streaming with Kafka). It saves you the set-up: the uv project, the folder layout, the Spark test session, the function signatures and the test files. The producer, the consumer, the parsing, the windows, the deduplication and the Delta sink are still yours to write.

## What is included

| File | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | The uv project: Python 3.12, `confluent-kafka` and `requests-sse`, plus `pytest` and `ruff` for your laptop. `pythonpath = ["."]` is set for pytest |
| `.gitignore` | Complete: keeps `data/`, `.env`, `.venv/` and caches out of Git |
| `producer.py` | Constants (stream address, Kafka address, topic, User-Agent) and stubs |
| `consumer.py` | Constants (group, commit interval, log file) and stubs |
| `stream/__init__.py` | Empty, so `stream` is a package |
| `stream/parse.py` | `EVENT_SCHEMA`, `parse_events()`, `read_topic()` and `main()` as stubs |
| `stream/window_counts.py` | `count_per_language()`, `parse_args()` and `main()` as stubs, and the names of the memory table, the Delta table and the checkpoint |
| `stream/show_counts.py` | The stub of `main()` |
| `tests/conftest.py` | Complete: the `spark` fixture (a small local session) |
| `tests/test_parse.py`, `tests/test_window_counts.py` | Skipped tests with a docstring each |

There is no `compose.yaml` and no `compose.spark.yaml` here: tasks 8 and 10 tell every student to copy them from the kit's `datalab/kafka/` and `datalab/spark/`.

## Copy it in (task 8)

Task 8 says "start from `starters/p08-editstream` instead of an empty folder". In Git Bash, inside the task folder:

```bash
git -C ~/de-kit pull
cp -r ~/de-kit/starters/p08-editstream editstream
cp ~/de-kit/datalab/kafka/compose.yaml editstream/compose.yaml
cd editstream
```

Then follow task 8 from step 2. At step 5, run `uv sync` instead of `uv init` and `uv add`, as the brief says. From task 9 on, copy your `editstream/` folder forward as each brief says.

**Task 10, step 6:** `pythonpath = ["."]` and the `spark` fixture are already there. Go on to step 7.

## How to run it

On your laptop, in `editstream/`:

```bash
uv sync                      # confluent-kafka and requests-sse into .venv/
uv run pytest -q             # the Spark tests are skipped here: no PySpark on Windows
uv run ruff check            # lint
uv run python producer.py --seconds 60
uv run python consumer.py
```

In the Spark container, once task 10 has added `compose.spark.yaml` and you started the lab with `docker compose --profile lite up -d`:

```bash
docker compose exec spark pytest tests -q
docker compose exec spark spark-submit stream/parse.py
docker compose exec spark spark-submit stream/window_counts.py
```

Two Kafka addresses: `localhost:9092` from your laptop (`producer.py`, `consumer.py`), `kafka:19092` from the Spark container (`stream/`).

## Your TODOs

Find them with `grep -rn "TODO(task" .` in `editstream/`.

| Task | File | What you write |
|---|---|---|
| 8 | `producer.py` | `parse_args()` (`--seconds`), `is_canary()`, `main()` |
| 9 | `consumer.py` | `parse_args()` (`--crash-after`), `make_consumer()`, `process()`, `main()` |
| 10 | `stream/parse.py` | `EVENT_SCHEMA`, `parse_events()`, `read_topic()`, `main()` |
| 10 | `tests/test_parse.py` | The parsing test |
| 11 | `stream/window_counts.py` | `count_per_language()`, `parse_args()`, `main()` with the console sink |
| 11 | `tests/test_window_counts.py` | The window test |
| 12 | `stream/parse.py` | `replay` in `read_topic()` |
| 12 | `stream/window_counts.py` | The deduplication, and `--replay` with the memory sink |
| 12 | `tests/test_window_counts.py` | The duplicate test |
| 13 | `stream/window_counts.py` | `--sink delta` with the checkpoint |
| 13 | `stream/show_counts.py` | `main()` |

Tasks 8 and 10 also add the two Compose files and the `include:` lines in `compose.yaml`. Those are copies of the kit's files, so there is no TODO for them here. Task 14 is the wrap-up.

## What you still write yourself

- Every function body and test in the table above.
- The two Compose files: copies from the kit, and the `include:` lines (task 10, step 1).
- `NOTES.md` (tasks 9, 11, 12, 13), `AI_LOG.md` (task 12) and `evidence.md` in each task folder.
- In the wrap-up: `editstream/README.md`, `docs/screenshots/` and `EXPLAIN.md`.

## Data and licence

This starter holds no data. Your producer reads Wikimedia's EventStreams live into your own Kafka, and `data/` stays out of Git. Edit data from Wikimedia projects via EventStreams, CC BY-SA 4.0; the kit's `data/edits/README.md` gives the credit line.
