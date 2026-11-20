"""Calls to the OpenAQ v3 API: one request, the page loop, and saving the raw pages.

The address is OPENAQ_API_URL (the host, https://api.openaq.org) and every path
starts with /v3/. The key goes in the X-API-Key header. The limits are 60 calls a
minute and 2,000 an hour. The kit's data/airquality/README.md has the endpoints,
the paging rules and the time rules.

tests/fixtures/ holds a hand-made /v3/locations page and a /v3/sensors/<id>/hours
page with the same shape as the API's answers.
"""

from pathlib import Path


class ApiError(Exception):
    """The API answered with a status other than 200.

    ApiError(503) keeps the status as `.status` (an int), so that
    retry.is_retryable() (task 12) can decide whether to try again.
    """

    def __init__(self, status: int, message: str = "") -> None:
        raise NotImplementedError(
            "TODO(task 8): keep status as self.status, then call super().__init__()"
        )


def get_json(path: str, params: dict) -> dict:
    """GET OPENAQ_API_URL + path with params, and return the answer's JSON.

    - Read OPENAQ_API_URL and OPENAQ_API_KEY from the settings.
    - Send the key in the X-API-Key header, with a 30-second timeout (httpx).
    - Raise ApiError(status) for any status other than 200.
    - Wait 1 second after every call, to stay under 60 calls a minute.
    - Log each call: the path and the params, never the key.

    Example: get_json("/v3/locations", {"coordinates": "51.5072,-0.1276", "radius": 25000, "limit": 100})

    Task 12 adds a practice switch: when the setting CLEARAIR_FAIL_AFTER_CALLS
    holds a number N, every call after the first N raises ApiError(503).
    """
    # TODO(task 12): add the CLEARAIR_FAIL_AFTER_CALLS practice switch.
    raise NotImplementedError("TODO(task 8): write get_json()")


def find_sensors(settings: dict, run_dir: Path | None = None) -> list[tuple[int, int]]:
    """Return up to MAX_SENSORS pairs (location_id, sensor_id) whose sensor
    measures PARAMETER.

    Call /v3/locations with coordinates=CITY_COORDINATES (latitude first),
    radius=CITY_RADIUS_M (at most 25000) and limit=100. Each location has "id"
    and "sensors"; each sensor has "id" and "parameter" ({"name": "pm25", ...}).

    When run_dir is given, save each /locations page in it with save_page(), as
    locations-001.json, locations-002.json and so on.

    An empty list is a valid answer: some cities report pm10 or no2 but not pm25.
    Tip: keep the choosing in a small function of the pages, so load-api --raw
    (task 10) can choose the same sensors from the saved locations pages.
    """
    # TODO(task 9): read every page of /locations with fetch_pages(), not only page 1.
    # TODO(task 12): wrap these get_json() calls in call_with_retries() too. retry.py
    #   imports ApiError from this module, so import call_with_retries inside this
    #   function, not at the top of the file (a circular import otherwise).
    raise NotImplementedError("TODO(task 8): write find_sensors()")


def save_page(run_dir: Path, name: str, page: dict) -> Path:
    """Write one raw page as JSON to run_dir / name, and return the file's path.

    - run_dir is data/raw/<run-id>; <run-id> is the UTC run start rounded down
      to the hour, like 20261112T0800Z.
    - name is "locations-001.json" or "<sensor-id>/page-001.json": create the
      sensor's folder when it is missing.
    - Save the page exactly as the API sent it, so load-api --raw (task 10) can
      load it again without calling the API.
    """
    raise NotImplementedError("TODO(task 8): write save_page()")


def fetch_pages(get_page, limit: int = 100, max_pages: int = 50) -> list[dict]:
    """Call get_page(1), get_page(2), get_page(3) ... and return the list of pages.

    get_page(page_no) returns one page as the API sends it: a dict with "meta"
    and "results".
    - Stop after the first page with fewer than `limit` results (it may have 0).
    - Never let meta["found"] decide: on a full page it can be the text ">100".
    - Raise an error when max_pages pages were read and the last one was still
      full, so a source that never ends cannot loop for ever.

    tests/test_client.py checks 250 rows (3 calls), exactly 200 rows (3 calls, the
    last page empty), 0 rows (1 call) and a source that never ends.
    """
    raise NotImplementedError("TODO(task 9): write fetch_pages()")


def summarise_pages(pages: list[dict]) -> dict:
    """Summarise one sensor's /hours pages for the log.

    Return a dict with:
    - "rows": the number of results on all the pages;
    - "first" and "last": the earliest and the latest period.datetimeTo.utc
      (None when there are no rows);
    - "repeats": how many period.datetimeTo.utc values appear more than once.
    """
    raise NotImplementedError("TODO(task 9): write summarise_pages()")
