# Kafka for one product

`compose.yaml` in this folder runs one Kafka broker (the server that stores topics) in KRaft mode, so it needs no ZooKeeper. A profile named `cdc` adds Kafka Connect with the Debezium connectors, for change data capture (reading a database's own log of changes). The course uses it in P8 EditStream.

Run every command in Git Bash, with Docker Desktop running.

## 1. Copy the file and start Kafka

Copy the kit's file into your product folder as `compose.yaml`, then start it there:

```bash
cp ~/de-kit/datalab/kafka/compose.yaml editstream/compose.yaml
cd editstream
docker compose up -d
docker compose ps
```

`ps` shows the service `kafka` with STATUS `Up` and, after about 15 seconds, `(healthy)`. The first start downloads the image once (about 240 MB).

The broker has no profile, so `docker compose up -d` starts it. To try the commands below without a product folder, run them in `~/de-kit/datalab/kafka` instead.

## 2. The broker's two addresses

| You connect from | Address |
|---|---|
| Your laptop (Python, a producer script) | `localhost:9092` |
| Inside the `kafka` container (the Kafka scripts below) | `localhost:9092` |
| Another container of the same Compose project, such as Spark | `kafka:19092` |

Inside a container, `localhost` is that container itself. So Spark, in its own container, uses the service name `kafka` and the inside port `19092`.

## 3. Topics

Kafka's scripts are on the `PATH` inside the container. Run them with `docker compose exec kafka`:

```bash
docker compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic try-log --partitions 3
docker compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
docker compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic try-log
```

The first command prints `Created topic try-log.`. `--describe` prints one line per partition.

This broker does **not** create topics by itself (`auto.create.topics.enable` is off). Writing to a topic that does not exist fails with `UNKNOWN_TOPIC_OR_PARTITION`: create the topic first.

Delete a topic with `--delete --topic try-log`.

## 4. The console producer and consumer

Send messages with a key. Type one message per line as `key:value`, then press Ctrl+C to stop:

```bash
docker compose exec kafka kafka-console-producer.sh --bootstrap-server localhost:9092 --topic try-log --reader-property parse.key=true --reader-property key.separator=:
```

```text
pune:a
mumbai:b
pune:c
```

Messages with the same key always go to the same partition.

To send a file instead of typing, use `-T` and `<`: `docker compose exec -T kafka kafka-console-producer.sh --bootstrap-server localhost:9092 --topic try-log < lines.txt`.

Read every message from the beginning, with its partition, offset (its position in the partition) and key:

```bash
docker compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic try-log --from-beginning --formatter-property print.partition=true --formatter-property print.offset=true --formatter-property print.key=true
```

It prints lines such as `Partition:2	Offset:0	pune	a` and waits for more. Press Ctrl+C to stop. Add `--max-messages 6` to stop after six messages.

Kafka 4.4 still accepts the older `--property` flag for both scripts, but prints a warning that it will be removed. Use `--reader-property` for the producer and `--formatter-property` for the consumer.

See the next free offset of each partition:

```bash
docker compose exec kafka kafka-get-offsets.sh --bootstrap-server localhost:9092 --topic try-log
```

It prints one line per partition, for example `try-log:2:4`: partition 2 holds offsets 0 to 3.

## 5. Consumer groups and offsets

Read as a group. The group remembers how far it has read:

```bash
docker compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic try-log --group try-group --from-beginning
```

Press Ctrl+C, then ask what the group has read:

```bash
docker compose exec kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group try-group
```

Look at `CURRENT-OFFSET` (what the group has read), `LOG-END-OFFSET` (what the topic holds) and `LAG` (the difference).

### Reset a group's offsets

Stop every consumer of the group first: a group with a running consumer cannot be reset. `--dry-run` shows the new offsets, `--execute` sets them:

```bash
docker compose exec kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group try-group --topic try-log --reset-offsets --to-earliest --dry-run
docker compose exec kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group try-group --topic try-log --reset-offsets --to-earliest --execute
```

`--shift-by -2` moves every partition back two messages. `--to-latest` skips everything that is there now.

## 6. From Python on your laptop

Use `localhost:9092`. Both common libraries work, for example:

```bash
uv add kafka-python
uv run python -c "from kafka import KafkaProducer; p = KafkaProducer(bootstrap_servers='localhost:9092'); p.send('try-log', key=b'kochi', value=b'hello'); p.flush()"
```

`confluent-kafka` works with `{"bootstrap.servers": "localhost:9092"}` too.

## 7. Stop, keep or delete

| To do this | Command |
|---|---|
| Stop Kafka, keep topics and messages | `docker compose down` |
| Stop it and delete every topic | `docker compose down -v` |

The topics live in the volume `<folder>_kafka-data`, for example `editstream_kafka-data`. Each folder where you start Kafka has its own volume, so the topics in `~/de-kit/datalab/kafka` are not the topics in `editstream/`.

Only one Kafka can use port 9092. Stop the one in the other folder first.

## 8. Kafka and Spark together (P8)

EditStream needs Kafka and Spark in one Compose project, so that Spark reaches the broker at `kafka:19092`. Use Compose's `include`: your `compose.yaml` (the Kafka file) includes the Spark file.

In your `editstream/` folder:

```bash
cp ~/de-kit/datalab/kafka/compose.yaml compose.yaml
cp ~/de-kit/datalab/spark/compose.yaml compose.spark.yaml
```

Open `compose.yaml` and add these two lines at the very top, before `services:`:

```yaml
include:
  - compose.spark.yaml
```

Then start both with the Spark profile:

```bash
docker compose --profile lite up -d
docker compose ps
```

`ps` shows `kafka` and `spark` running. The first start also builds the kit's Spark image (about 3 minutes, once). Run Spark jobs as [`../spark/README.md`](../spark/README.md) shows, for example `docker compose exec spark spark-submit stream/parse.py`. Inside a job, read the topic with `.option("kafka.bootstrap.servers", "kafka:19092")`.

Stop both with the same profile:

```bash
docker compose --profile lite down
```

`docker compose down` without the profile stops only Kafka. On a 16 GB laptop you may use `--profile full` instead of `--profile lite`, the same way.

## 9. Change data capture with Debezium (profile `cdc`)

Debezium reads the changes of a PostgreSQL table from the database's log and writes each change to a topic. The data lab's PostgreSQL is ready for it (`wal_level=logical`).

1. Start PostgreSQL in the data lab, then Kafka with Connect:

   ```bash
   (cd ~/de-kit/datalab && docker compose --profile core up -d)
   docker compose --profile cdc up -d
   ```

   Connect needs about a minute. `curl -s http://localhost:8083/connectors` prints `[]` when it is ready.

2. Make a table to watch, in the `clearair` database. `REPLICA IDENTITY FULL` makes the database log the whole old row, so updates and deletes carry `before`:

   ```bash
   docker exec -i datalab-postgres-1 psql -U de -d clearair -c "CREATE TABLE stations (id int PRIMARY KEY, name text, city text);" -c "ALTER TABLE stations REPLICA IDENTITY FULL;" -c "INSERT INTO stations VALUES (1, 'Anand Vihar', 'Delhi');"
   ```

3. Save the connector's settings as `connector.json`. The password is the data lab's local one:

   ```json
   {
     "name": "clearair-stations",
     "config": {
       "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
       "database.hostname": "host.docker.internal",
       "database.port": "5432",
       "database.user": "de",
       "database.password": "de",
       "database.dbname": "clearair",
       "topic.prefix": "clearair",
       "table.include.list": "public.stations",
       "plugin.name": "pgoutput",
       "slot.name": "clearair_stations",
       "publication.autocreate.mode": "filtered",
       "topic.creation.default.replication.factor": "1",
       "topic.creation.default.partitions": "1"
     }
   }
   ```

4. Register it and check its state:

   ```bash
   curl -s -X POST -H "Content-Type: application/json" --data @connector.json http://localhost:8083/connectors
   curl -s http://localhost:8083/connectors/clearair-stations/status
   ```

   The status shows `"state":"RUNNING"` for the connector and its task.

5. Change the table, then read the topic `clearair.public.stations`:

   ```bash
   docker exec -i datalab-postgres-1 psql -U de -d clearair -c "UPDATE stations SET name = 'Anand Vihar ISBT' WHERE id = 1;" -c "DELETE FROM stations WHERE id = 1;"
   docker compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic clearair.public.stations --from-beginning
   ```

   Each change is one JSON message with `before`, `after`, `source` and `op`: `r` for the first copy (snapshot), `c` for an insert, `u` for an update and `d` for a delete. After a delete comes one message whose value is `null` (a tombstone, which tells Kafka it may forget that key).

6. When you finish, remove the connector, then its replication slot. A slot that nobody reads makes PostgreSQL keep its log for ever and fill your disk:

   ```bash
   curl -s -X DELETE http://localhost:8083/connectors/clearair-stations
   docker exec -i datalab-postgres-1 psql -U de -d clearair -c "SELECT pg_drop_replication_slot('clearair_stations');"
   docker compose --profile cdc down
   ```

   If the last `psql` says the slot `is active`, wait ten seconds and run it again.

The kit's station database (`data/airquality/stationdb`, port 5433) can be the source too: use `"database.port": "5433"` and its database name.

## Memory

Measured idle on the course versions: the broker about 430 MB, Kafka Connect about 1.2 GB. On an 8 GB laptop, run Kafka alone, or use GitHub Codespaces for Kafka with Spark (see [`setup/codespaces.md`](../../setup/codespaces.md)).

## Troubleshooting

- **`Connection to node -1 (localhost/127.0.0.1:9092) could not be established`**: Kafka is not running, or not healthy yet. Run `docker compose ps` and wait for `(healthy)`.
- **`UNKNOWN_TOPIC_OR_PARTITION`**: the topic does not exist. Create it (step 3).
- **`port is already allocated` for 9092**: another Kafka runs, perhaps from another folder. Find it with `docker ps --format "table {{.Names}}\t{{.Ports}}"` and stop it with `docker compose down` in its folder.
- **An error shows a path such as `C:/Program Files/Git/opt/kafka/...`**: Git Bash changed a path. Put `MSYS_NO_PATHCONV=1` in front of that `docker` command.
- **`the input device is not a TTY`**: use VS Code's terminal, or add `-T` when you send a file with `<`.
- **Spark says `Failed to find data source: kafka`**: you started Spark from an old copy of the kit. Run `git pull` in `~/de-kit`, copy `spark/compose.yaml` again and run `docker compose --profile lite up -d --build`.

## Image versions

| Service | Image |
|---|---|
| Kafka | `apache/kafka:4.4.0` |
| Kafka Connect with Debezium | `quay.io/debezium/connect:3.7.1.Final` (Debezium 3.7.1) |
