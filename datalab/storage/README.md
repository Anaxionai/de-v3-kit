# The S3 emulator: Floci

Floci is a free AWS emulator (a program that imitates AWS on your laptop). It answers AWS calls at `http://localhost:4566`, so the AWS CLI, DuckDB, `boto3` and PyIceberg work against it as if it were Amazon S3. Nothing costs money, and nothing reaches the real AWS.

The course uses it as S3 in P5 PageLake, and for the first AWS steps of P11 CycleCity (part 2) before the real account.

| Setting | Value |
|---|---|
| Address (endpoint) | `http://localhost:4566` from your laptop, `http://host.docker.internal:4566` from a container |
| Redshift clusters (P11) | `localhost`, ports 7100 to 7104 |
| Access key | `test` |
| Secret key | `test` |
| Region | `ap-south-1` |
| Account ID | `000000000000` |

The keys are fake. They work only on the emulator, so they are safe in a file on your laptop. Never put real AWS keys in the places this file uses.

Run every command in Git Bash. Work in your product folder, not inside the kit.

## 1. Start the emulator

```bash
cd ~/de-kit/datalab
docker compose --profile storage up -d
curl -s http://localhost:4566/_floci/health
```

The last command prints JSON that contains `"version":"2.4.0"` and `"s3":"running"`.

Buckets and objects stay when you stop the emulator with `docker compose --profile storage down`: the emulator keeps them on disk, in the Docker volume `datalab_floci-data`, not in memory. A 300 MB object added only about 35 MB to the emulator's memory in the course team's test. `docker compose --profile storage down -v` deletes every bucket.

## 2. The AWS CLI

Install the AWS CLI version 2 once, in PowerShell or Git Bash:

```bash
winget install -e --id Amazon.AWSCLI
```

Close VS Code and open it again, so Git Bash finds the new `aws` command. `aws --version` prints `aws-cli/2.` and more numbers.

### The `emulator` profile

A profile (a named set of settings) keeps the emulator's fake keys apart from a real AWS account. Run:

```bash
aws configure --profile emulator
```

Answer the four questions like this:

```text
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: ap-south-1
Default output format [None]: json
```

Then add the emulator's address to the profile:

```bash
aws configure set endpoint_url http://localhost:4566 --profile emulator
```

Check that you reach the emulator:

```bash
aws sts get-caller-identity --profile emulator
```

The `Account` is `000000000000`. If you see any other 12-digit number, you reached a real AWS account: stop and check your profile.

Keep the two names apart: `emulator` is always this local emulator with fake keys. In P11 the real AWS account gets its own profile, `cyclecity` (see the kit's `cloud/aws/README.md`). Never put real keys in the `emulator` profile.

**One switch for every tool (P11).** Instead of typing `--profile emulator` on each command, run:

```bash
export AWS_PROFILE=emulator
```

Until you close the terminal, the AWS CLI, your `boto3` code and Terraform's AWS provider all use this profile, including its `endpoint_url`, so they all talk to the emulator. Check it with `echo $AWS_PROFILE` and `aws sts get-caller-identity` (`Account` `000000000000`). To work on your real account again, run `export AWS_PROFILE=cyclecity`.

### Buckets and files

Use your own GitHub user name in lower case in place of `<your-id>`:

```bash
aws --profile emulator s3 ls
aws --profile emulator s3 mb s3://pagelake-<your-id>
echo "hello from Pune" > hello.txt
aws --profile emulator s3 cp hello.txt s3://pagelake-<your-id>/bronze/hello.txt
aws --profile emulator s3 ls s3://pagelake-<your-id>/ --recursive
aws --profile emulator s3 cp s3://pagelake-<your-id>/bronze/hello.txt -
```

`s3 mb` prints `make_bucket: pagelake-<your-id>`. The `ls --recursive` lists `bronze/hello.txt` with its size, 16 bytes. `cp ... -` prints the file's text in the terminal (the `-` means "to the screen").

Delete a bucket with everything in it: `aws --profile emulator s3 rb s3://pagelake-<your-id> --force`. It prints one `delete:` line per file, then `remove_bucket:`.

### Environment variables instead of a profile

Your Python code, DuckDB scripts and PyIceberg read the same four settings from environment variables. Set them for the current terminal (they last until you close it):

```bash
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=ap-south-1 AWS_ENDPOINT_URL=http://localhost:4566
aws s3 ls
```

`AWS_ENDPOINT_URL` alone is not enough: the CLI also needs keys and a region.

In a product folder, keep them in `.env` (never committed; commit `.env.example` with the same fake values):

```text
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=ap-south-1
AWS_ENDPOINT_URL=http://localhost:4566
```

Load the file into the terminal with:

```bash
set -a; source .env; set +a
```

`set -a` exports every variable the file sets. Save `.env` with LF line endings (VS Code shows `LF` at the bottom right): Docker and Python's `.env` readers keep the invisible CR character of a CRLF file in every value.

## 3. DuckDB

DuckDB reads and writes the bucket with its `httpfs` extension. A secret (DuckDB's name for a set of keys and settings) tells it where the emulator is. Save this as `duck_s3.py`:

```python
import duckdb

con = duckdb.connect()
con.sql("INSTALL httpfs")
con.sql("LOAD httpfs")
con.sql("""
CREATE OR REPLACE SECRET lab (
    TYPE s3,
    KEY_ID 'test',
    SECRET 'test',
    REGION 'ap-south-1',
    ENDPOINT 'localhost:4566',
    URL_STYLE 'path',
    USE_SSL false
)""")
con.sql("COPY (SELECT range AS id, 'city ' || range AS name FROM range(1000)) "
        "TO 's3://pagelake-<your-id>/silver/demo.parquet' (FORMAT parquet)")
print(con.sql("SELECT count(*) AS n, max(id) AS top FROM read_parquet('s3://pagelake-<your-id>/silver/demo.parquet')").fetchall())
print(con.sql("SELECT file FROM glob('s3://pagelake-<your-id>/**')").fetchall())
```

Run it:

```bash
uv run --python 3.12 --with duckdb python duck_s3.py
```

It prints `[(1000, 999)]`, then the two files in the bucket. The first run downloads the `httpfs` extension once.

- `ENDPOINT` has no `http://`. `USE_SSL false` makes DuckDB use plain `http`.
- `URL_STYLE 'path'` puts the bucket name in the path (`localhost:4566/pagelake-<your-id>/...`), which the emulator needs.
- The same `CREATE SECRET` and queries work in the DuckDB command-line program.

## 4. Python with boto3

`boto3` is the AWS library for Python. Save this as `boto_s3.py`:

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="ap-south-1",
    aws_access_key_id="test",          # fake key: works only on the emulator
    aws_secret_access_key="test",
)
s3.put_object(Bucket="pagelake-<your-id>", Key="bronze/note.txt", Body=b"written by boto3")
for obj in s3.list_objects_v2(Bucket="pagelake-<your-id>", Prefix="bronze/")["Contents"]:
    print(obj["Key"], obj["Size"])
```

```bash
uv run --python 3.12 --with boto3 python boto_s3.py
```

It prints `bronze/hello.txt 16` and `bronze/note.txt 16`.

In your own code, read the address and keys from environment variables (`AWS_ENDPOINT_URL` and the others above, set in `.env`), so the same code runs against the real AWS later with other settings.

## 5. Iceberg tables with PyIceberg

### Try it: `try_iceberg.py`

This script makes a small Iceberg table, appends to it twice and shows its snapshots (P5, the table-formats card). Set the four environment variables (section 2) and make the bucket:

```bash
aws --profile emulator s3 mb s3://try-<your-id>
```

Save this as `try_iceberg.py` in a practice folder, and change `MY_ID`:

```python
"""Try Iceberg on the S3 emulator: make a table, append twice, and look at its snapshots."""
import os
import sys

import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.types import DoubleType

MY_ID = "your-id"  # change this to your GitHub user name in lower case
BUCKET = f"try-{MY_ID}"

catalog = SqlCatalog(
    "try",
    uri="sqlite:///try_catalog.db",  # the catalogue: a SQLite file in this folder
    warehouse=f"s3://{BUCKET}/warehouse",  # the table's files: in the bucket
    **{
        "s3.endpoint": os.environ["AWS_ENDPOINT_URL"],
        "s3.access-key-id": os.environ["AWS_ACCESS_KEY_ID"],
        "s3.secret-access-key": os.environ["AWS_SECRET_ACCESS_KEY"],
        "s3.region": os.environ["AWS_DEFAULT_REGION"],
        "s3.path-style-access": "true",
    },
)

if sys.argv[1:] == ["add-column"]:
    table = catalog.load_table("demo.cities")
    with table.update_schema() as update:
        update.add_column("area_km2", DoubleType())
    print(table.schema())
    sys.exit(0)

cities = pa.table({"city": ["Pune", "Kochi", "Jaipur"], "population": [7_400_000, 2_100_000, 4_100_000]})
catalog.create_namespace_if_not_exists("demo")
if catalog.table_exists("demo.cities"):
    catalog.drop_table("demo.cities")
table = catalog.create_table("demo.cities", schema=cities.schema)
table.append(cities)
table.append(cities)

print(table.inspect.snapshots().select(["committed_at", "snapshot_id", "operation"]))
for snapshot in table.snapshots():
    print("snapshot", snapshot.snapshot_id, "has", table.scan(snapshot_id=snapshot.snapshot_id).count(), "rows")
```

Run it, then run it again with `add-column`:

```bash
uv run --python 3.12 --with "pyiceberg[sql-sqlite,pyarrow]" python try_iceberg.py
uv run --python 3.12 --with "pyiceberg[sql-sqlite,pyarrow]" python try_iceberg.py add-column
aws --profile emulator s3 ls s3://try-<your-id>/warehouse/ --recursive
```

- The first run prints two snapshots, both `append`, then `has 3 rows` for the first snapshot and `has 6 rows` for the second. Each run starts the table again from nothing.
- `add-column` prints the schema with a third field, `area_km2: optional double`. No data file changes: only a new metadata file.
- The listing shows `data/*.parquet` (the rows), `metadata/*.metadata.json` (one per change of the table), `metadata/snap-*.avro` (one manifest list per snapshot) and `metadata/*-m0.avro` (manifests).

### Your own tables

PyIceberg writes Iceberg tables (P5). It needs a catalogue (the list of tables and where each one's newest metadata file is). On your laptop, the simplest catalogue is a SQL catalogue in a small SQLite file. The table's data and metadata files go in the bucket.

Save this as `iceberg_s3.py`:

```python
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

catalog = SqlCatalog(
    "lab",
    uri="sqlite:///data/catalog.db",                  # the catalogue: a SQLite file in data/
    warehouse="s3://pagelake-<your-id>/iceberg",      # the table files: in the bucket
    **{
        "s3.endpoint": "http://localhost:4566",
        "s3.access-key-id": "test",
        "s3.secret-access-key": "test",
        "s3.region": "ap-south-1",
        "s3.path-style-access": "true",
    },
)
catalog.create_namespace_if_not_exists("silver")
rows = pa.table({"page": ["Pune", "Mumbai"], "views": [120, 340]})
table = catalog.create_table_if_not_exists("silver.views", schema=rows.schema)
table.append(rows)
print(table.scan().to_arrow().num_rows, "rows")
print(table.metadata_location)
```

```bash
mkdir -p data
uv run --python 3.12 --with "pyiceberg[sql-sqlite,pyarrow]" python iceberg_s3.py
```

It prints `2 rows` and the address of the table's metadata file, which ends in `.metadata.json`. Each run appends two more rows and adds a snapshot.

DuckDB reads the same table with its `iceberg` extension. Give it the metadata file's address:

```python
con.sql("INSTALL iceberg")
con.sql("LOAD iceberg")
print(con.sql("SELECT * FROM iceberg_scan('s3://pagelake-<your-id>/iceberg/silver/views/metadata/<file>.metadata.json')").fetchall())
```

If the import of `pyarrow` fails with `An Application Control policy has blocked this file`, Windows Smart App Control blocks it. Read "Smart App Control" in [`setup/windows.md`](../../setup/windows.md).

## 6. Other AWS services on the emulator

Floci imitates many AWS services, not only S3. P11 practises the services in the table below here, before the real account. This table shows what the course team tried on Floci 2.4.0, and what it does not do.

| Service | What works | What is different from AWS |
|---|---|---|
| IAM | Users, roles, policies and access keys. The policy simulator (`aws iam simulate-principal-policy`) answers `allowed` or `implicitDeny` | Policies are **not checked** unless you start the emulator with `FLOCI_IAM_ENFORCEMENT=true` (see below). The `test` key is the account's root and may always do everything |
| Lambda | A Python 3.12 function is created, runs in its own container and returns its result | The first call downloads the runtime image (about 1 minute). The emulator needs the Docker socket, which the Compose file gives it |
| EventBridge | A rule with a schedule (`rate(1 hour)`) and a Lambda target is stored | The course team did not wait for a scheduled rule to fire |
| Step Functions | A state machine runs: a Lambda task with a retry, then a pass state | — |
| Glue Data Catalog | Databases and tables, which Athena then reads | — |
| Glue jobs and crawlers | A job run reaches `SUCCEEDED` | **The job's script is not run**, and a crawler does not read data or create tables. Run Glue job code on the real AWS |
| Athena | Real SQL over a Glue table (JSON, CSV, Parquet or Iceberg files in a bucket), run by DuckDB in a helper container | `DataScannedInBytes` is always 0, so measure the bytes a query scans on the real AWS. The first query downloads the helper image |
| Kinesis Data Streams | Create a stream, put a record, read it back with a shard iterator | — |
| Data Firehose | A delivery stream writes records to a bucket after its buffer time (60 seconds in the test) | — |
| Redshift | A cluster is a real PostgreSQL 15 container on `localhost`, port 7100 (the next clusters get 7101 to 7104). `COPY ... FROM 's3://...' IAM_ROLE '...' FORMAT AS CSV` or `FORMAT AS JSON 'auto'` loads files from a bucket | It is PostgreSQL underneath: sort and distribution keys are ignored. `COPY` works only over a PostgreSQL connection (psql, psycopg), and only with a role given to the cluster (`--iam-roles` at `create-cluster`). The Redshift Data API runs a `SELECT` but rejects `COPY` |
| Secrets Manager | Create a secret and read its value | — |

Read a Redshift cluster's address from the emulator:

```bash
aws --profile emulator redshift describe-clusters --query "Clusters[].Endpoint"
```

It prints `"Address": "localhost"` and the port. Connect with psql or psycopg to that address, with the user and password you gave `create-cluster`.

To make IAM policies count, start the emulator like this. Requests signed with a user's own access key are then checked against that user's policies:

```bash
docker compose --profile storage down
FLOCI_IAM_ENFORCEMENT=true docker compose --profile storage up -d
```

In the course team's test, a user allowed only `s3:PutObject` on `raw/*` could write `raw/ok.json` and got `AccessDenied` for `clean/no.json` and for listing the bucket.

### Helper containers

Lambda, Athena and Redshift each start a helper container, named `floci-aws-...`. A Redshift container goes away when you delete its cluster. The others can keep running after `docker compose --profile storage down`. Remove the ones on the lab's network when you finish:

```bash
docker rm -f $(docker ps -aq --filter network=datalab_default)
```

If `down` says `Network datalab_default Resource is still in use`, a helper container still runs: run the command above, then `down` again.

## Memory

Floci uses about 85 MB when idle. After the service tests above it used about 200 MB, plus 40 MB for the Athena helper, 100 MB for a Redshift cluster and up to 128 MB for each Lambda function while it runs.

## Troubleshooting

- **`Could not connect to the endpoint URL`**: the emulator is not running. Run `docker compose --profile storage ps` in `~/de-kit/datalab`.
- **`InvalidAccessKeyId` or `SignatureDoesNotMatch` from a real AWS address**: the endpoint is missing, so the call went to the real AWS. Check `endpoint_url` in your profile or `AWS_ENDPOINT_URL`.
- **DuckDB says `HTTP 403` or cannot find the bucket**: check `URL_STYLE 'path'`, `USE_SSL false`, and that `ENDPOINT` has no `http://`.
- **`NoSuchBucket`**: bucket names are per emulator. After `down -v`, make the bucket again.
