# Spark for one product

`compose.yaml` in this folder runs Apache Spark for one product, with Delta Lake and the Kafka source already inside. The course uses it in P7 TaxiScale and P8 EditStream.

| Profile | What runs | For |
|---|---|---|
| `lite` | One container, `spark`. Jobs run in local mode (driver and executors in one process). The container may use 2 GB | 8 GB laptops |
| `full` | The `spark` container, plus a master (`spark-master`) and two workers (`spark-worker-1`, `spark-worker-2`), each worker with 1 core and 1 GB | 16 GB laptops |

In both profiles you run every command in the `spark` service. It also runs the history server, which shows finished jobs.

Run every command in Git Bash, with Docker Desktop running.

## 1. Copy the file and start Spark

```bash
cp ~/de-kit/datalab/spark/compose.yaml taxiscale/compose.yaml
cd taxiscale
docker compose --profile lite up -d
docker compose --profile lite ps
```

The **first** start builds the kit's Spark image, `de-kit-spark:4.2.1-r2`, once for your laptop: it downloads Spark (about 800 MB), then Delta Lake, the Kafka source and pytest. It takes about 3 minutes. Later starts, in any product folder, reuse the image and take seconds.

`ps` shows the service `spark` with STATUS `Up`.

For P8, where Kafka and Spark run together, see "Kafka and Spark together" in [`../kafka/README.md`](../kafka/README.md).

## 2. Where your files are

Your product folder is mounted as the container's working folder:

| On your laptop | Inside the container |
|---|---|
| `taxiscale/` | `/opt/spark/work-dir` (the working folder) |
| `taxiscale/jobs/clean.py` | `jobs/clean.py` |
| `taxiscale/data/` | `data/` |

The working folder is on `PYTHONPATH`, so a job or a test can `import` your own modules, for example `from stream.parse import parse_event`.

Inside the container, Python is version 3.10 (the version of the Spark image's Ubuntu), not 3.12. Write code that runs on both: the course's code does.

## 3. Run a job

Save this small job as `jobs/delta_check.py`:

```python
"""A small job: write a Delta table, read it back, show the table's history."""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("delta-check").getOrCreate()
spark.sparkContext.setLogLevel("WARN")
trips = spark.createDataFrame(
    [(1, "JFK", 52.0), (2, "LGA", 31.5), (3, "JFK", 48.25)], ["trip_id", "zone", "fare"])
trips.write.format("delta").mode("overwrite").save("data/delta/trips")
back = spark.read.format("delta").load("data/delta/trips")
print("rows:", back.count(), "| master:", spark.sparkContext.master, flush=True)
back.groupBy("zone").sum("fare").orderBy("zone").show()
spark.sql("DESCRIBE HISTORY delta.`/opt/spark/work-dir/data/delta/trips`").select("version", "operation").show()
spark.stop()
```

Run it in the `lite` profile:

```bash
docker compose exec spark spark-submit jobs/delta_check.py
```

It prints `rows: 3 | master: local[*]`, a table with `JFK 100.25` and `LGA 31.5`, and the table's history: version `0`, operation `WRITE`. The table's files are now in `taxiscale/data/delta/trips/` on your laptop, with its log in `_delta_log/`.

In the `full` profile, send the job to the master:

```bash
docker compose --profile full up -d
docker compose exec spark spark-submit --master spark://spark-master:7077 jobs/delta_check.py
```

It prints `master: spark://spark-master:7077` and the same results. The work now runs on the two workers.

- Spark prints many `INFO` and `WARN` lines. Add `spark.sparkContext.setLogLevel("WARN")` after you build the session, as above.
- For the interactive shell, run `docker compose exec spark pyspark`. Leave it with `exit()`.
- In a SQL path such as ``delta.`...` ``, write the full path inside the container (`/opt/spark/work-dir/...`). A short path such as `data/delta/trips` works in `.save()` and `.load()` but not there.

## 4. Tests with pytest

`pytest` is installed in the image. Put your tests in `tests/`, and give them a Spark session from `tests/conftest.py`:

```python
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    session = SparkSession.builder.master("local[1]").appName("tests").getOrCreate()
    yield session
    session.stop()
```

Run them in the container:

```bash
docker compose exec spark pytest tests -q
```

It ends with a line such as `1 passed in 13.93s`. The first test waits about 10 seconds while Spark starts.

## 5. Delta Lake and the Kafka source are built in

You add no `--packages` option and no configuration:

- Delta Lake 4.4.1 is on the class path, and the image's `spark-defaults.conf` switches on Delta's SQL extension and catalogue. `.format("delta")`, `MERGE INTO`, `DESCRIBE HISTORY` and time travel (`.option("versionAsOf", 0)`) work.
- The Kafka source and sink (`spark-sql-kafka-0-10`) are on the class path. Read a topic with `.format("kafka").option("kafka.bootstrap.servers", "kafka:19092")` when Kafka runs in the same Compose project (P8).

The image gets them when it is built: a `Dockerfile` written inside `compose.yaml` (the `dockerfile_inline` part) downloads the jars once from Maven Central and copies them into Spark's `jars` folder. Nothing is downloaded when a job runs.

In the course team's test, a stream on a one-partition topic with `.option("maxOffsetsPerTrigger", 25)` and `.trigger(availableNow=True)` read 100 messages in four micro-batches of 25. After 30 more messages, a restart from the same checkpoint read batch 4 (25 rows) and batch 5 (5 rows), and the Delta table held 130 rows.

## 6. The web pages

| Page | Address | When |
|---|---|---|
| Spark UI of the running job: jobs, stages, the SQL plan | http://localhost:4040 | only while a job runs |
| History server: every finished job | http://localhost:18080 | always |
| The master and its workers (`full` only) | http://localhost:8081 | always |

The history server reads the event logs that every job writes to the volume `<folder>_spark-events`. They stay after `docker compose --profile lite down`, so finished jobs are still there the next day. A job that ends very fast is easier to study in the history server than at port 4040.

## 7. Memory settings

| Setting | `lite` | `full` |
|---|---|---|
| The `spark` container's limit | 2 GB | 2 GB |
| Driver memory (`spark.driver.memory`) | 1 GB | 1 GB |
| Executors | inside the driver (local mode) | 1 per worker, 1 core and 1 GB each |
| Master and history server | — | 256 MB each |

Change a setting for one job with `--conf`, for example `docker compose exec spark spark-submit --conf spark.sql.shuffle.partitions=8 jobs/clean.py`. Keep the driver memory below the container's 2 GB.

Measured idle on the course versions: `lite` about 240 MB; `full` about 850 MB (`spark` 240 MB, master 180 MB, each worker 210 MB). A running job uses up to the limits above.

## 8. Stop and reset

| To do this | Command |
|---|---|
| Stop Spark (the job files and `data/` stay in your folder) | `docker compose --profile lite down` |
| Also delete the history server's event logs | `docker compose --profile lite down -v` |

Always name the profile: `docker compose down` on its own stops nothing here. Use `--profile full` if you started `full`.

## 9. Codespaces and Linux

The `spark` service runs as `root`, so jobs can write to `data/` on Windows and in Codespaces. On Linux and in Codespaces the files it writes then belong to `root`: delete them with `sudo rm -rf data/<folder>`.

## Troubleshooting

- **`pyspark: not found`** or **`service "spark" is not running`**: start Spark first: `docker compose --profile lite up -d`, then `docker compose --profile lite ps`.
- **The first `up` stops with a download error**: the network failed while the image was built. Run `docker compose --profile lite up -d` again: finished steps are not repeated.
- **`Failed to find data source: kafka`** or **`delta` is not a valid data source**: the container runs an image from before the kit had these jars. Run `git pull` in `~/de-kit`, copy `compose.yaml` again, then `docker compose --profile lite up -d --build`.
- **`Exited (137)`**, or the job stops with `OutOfMemoryError`: the job needs more memory than the container has. Read less data (one month), lower `spark.sql.shuffle.partitions`, or use Databricks Free Edition for the large run, as P7 does.
- **`port is already allocated` for 4040, 18080 or 8081**: another Spark runs in another folder. Stop it with `docker compose --profile lite down` (or `full`) in that folder.
- **`Initial job has not accepted any resources`** (`full`): the workers are not registered. Open http://localhost:8081: it must list two workers with state `ALIVE`. If not, run `docker compose --profile full up -d` again.
- **`TABLE_OR_VIEW_NOT_FOUND` for ``delta.`data/...` ``**: write the full path, ``delta.`/opt/spark/work-dir/data/...` ``.

## Versions

| Part | Version |
|---|---|
| Apache Spark | 4.2.1, from the image `apache/spark:4.2.1` (Scala 2.13, Java 21, Python 3.10) |
| Delta Lake | 4.4.1 (`io.delta:delta-spark_4.2_2.13:4.4.1`) |
| Kafka source | `org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.1` (with `kafka-clients` 3.9.2) |
| pytest | 9.2.0 |

The course uses Spark 4.2, not the newer 4.3, because Delta Lake 4.4 is built for Spark 4.2 and no Delta release supports Spark 4.3 yet. [`VERSIONS.md`](../../VERSIONS.md) has the details.
