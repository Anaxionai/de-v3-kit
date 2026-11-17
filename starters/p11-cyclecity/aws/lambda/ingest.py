"""CycleCity ingest: land the live station feed and the monthly trip files in the raw bucket.

It runs as the Lambda function cyclecity-<your-id>-ingest (handler ingest.handler), and on your
laptop against the emulator or AWS, from cyclecity/:

    uv run python aws/lambda/ingest.py                 # one hourly run: handler({}, None)
    uv run python aws/lambda/ingest.py trips 202401    # land one month: land_month("202401")

Settings come from environment variables, read at run time:
- RAW_BUCKET       the raw bucket, cyclecity-<your-id>-raw
- ALERT_SECRET_ID  the name of the secret that holds the alert webhook address (task 13)

Layout in the raw bucket:
- stations/status/dt=<UTC date>/<UTC time>.json   one station per line (JSON Lines)
- stations/state/watermark.json                   the highest last_reported landed so far
- trips/month=YYYYMM/JC-YYYYMM-citibike-tripdata.csv   the operator's CSV, unchanged
"""

import sys

GBFS_URL = "https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json"
TRIPS_URL = "https://s3.amazonaws.com/tripdata/"
STATUS_PREFIX = "stations/status/"
WATERMARK_KEY = "stations/state/watermark.json"
TRIPS_PREFIX = "trips/"


class FeedUnavailable(Exception):
    """The address could not be reached, or answered HTTP 5xx. Worth a retry (task 23)."""


class FeedNotFound(Exception):
    """The file does not exist: HTTP 404 under every name tried. Never retried (task 23)."""


def fetch(url: str) -> dict:
    """Download url with urllib.request and return the parsed JSON.

    Used for the discovery file and for the station_status feed.
    """
    # TODO(task 23): raise FeedUnavailable for network errors and HTTP 5xx. HTTPError is a
    #   subclass of URLError, so catch HTTPError first.
    raise NotImplementedError("TODO(task 9): download url and parse the JSON")


def find_feed(discovery: dict, name: str) -> str:
    """Return the url of the feed called name in a GBFS discovery file.

    The feeds are a list of {"name": ..., "url": ...} under data.en.feeds. Raise an error
    with a clear message if name is not there.
    """
    raise NotImplementedError("TODO(task 9): find the feed's url in data.en.feeds")


def select_new(stations: list[dict], watermark: int) -> tuple[list[dict], int]:
    """Keep the stations that reported since the last run.

    Return the stations whose last_reported (Unix seconds) is above watermark, and the new
    watermark: the highest last_reported among them, or watermark itself when none is new.
    A station exactly at the watermark is not new.
    """
    raise NotImplementedError("TODO(task 9): keep the stations above the watermark")


def read_watermark() -> int:
    """Return the watermark saved at WATERMARK_KEY in RAW_BUCKET, or 0 when there is none yet.

    A missing key is NoSuchKey. After task 10 the role has no s3:ListBucket, and S3 then
    answers a missing key with AccessDenied instead.
    """
    raise NotImplementedError("TODO(task 9): read the watermark")


def write_watermark(value: int) -> None:
    """Save value as JSON at WATERMARK_KEY in RAW_BUCKET."""
    raise NotImplementedError("TODO(task 9): write the watermark")


def land_month(month: str, base_url: str = TRIPS_URL) -> dict:
    """Land one month of trips, such as "202401", in RAW_BUCKET as plain CSV.

    Download f"{base_url}JC-{month}-citibike-tripdata.csv.zip" over HTTPS. On HTTP 404, try
    f"{base_url}JC-{month}-citibike-tripdata.zip"; if that is 404 too, raise FeedNotFound.
    The zip holds the CSV and a __MACOSX/ entry: put_object only the .csv, read from the zip
    in memory, at f"{TRIPS_PREFIX}month={month}/<the CSV's file name>". Return the month, the
    key written and its size in bytes.
    """
    # TODO(task 23): raise FeedUnavailable for network errors and HTTP 5xx, as in fetch().
    raise NotImplementedError("TODO(task 11): download, unzip and land one month")


def send_alert(message: str) -> None:
    """Post message to the alert webhook as JSON: {"text": message}.

    Read the address at run time from the secret named by ALERT_SECRET_ID (Secrets Manager,
    get_secret_value), then POST to it with urllib.request. The address never appears in
    code, logs or files.
    """
    raise NotImplementedError("TODO(task 13): read the secret and post the alert")


def handler(event: dict, context) -> dict:
    """The Lambda entry point.

    Find station_status in the discovery file at GBFS_URL, fetch it, and keep the new
    stations. Write them one JSON object per line to
    f"{STATUS_PREFIX}dt=<UTC date>/<UTC time>.json" in RAW_BUCKET, then, and only then,
    save the new watermark. A run with nothing new writes no file. Return the counts, the
    key written and the watermark.
    """
    # TODO(task 13): when event.get("action") == "alert", call send_alert(event["message"]) and
    #   return. When fetch fails, call send_alert, then raise the error again.
    # TODO(task 23): when the event has "month", return land_month(event["month"]), with
    #   event["base_url"] when present. Its result includes the month.
    raise NotImplementedError("TODO(task 9): the handler, as the docstring says")


if __name__ == "__main__":
    if sys.argv[1:2] == ["trips"]:
        print(land_month(sys.argv[2]))
    else:
        print(handler({}, None))
