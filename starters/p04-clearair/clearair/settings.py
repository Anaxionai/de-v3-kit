"""ClearAir's settings, read from environment variables.

Run every command with `uv run --env-file .env python -m clearair.cli ...`, so the
values in `.env` reach os.environ. `.env.example` lists every setting.
"""


def load_settings() -> dict:
    """Read every setting ClearAir needs from os.environ and return them in a dict.

    The settings, by the task that brings them in:
    - task 8: OPENAQ_API_URL, OPENAQ_API_KEY, CITY_NAME, CITY_COORDINATES,
      CITY_RADIUS_M, PARAMETER, MAX_SENSORS
    - task 10: DATABASE_URL
    - task 11: START_DAYS, LOOKBACK_HOURS
    - task 21: STATIONDB_URL

    When one or more are missing or empty, stop the program with a message that
    names every missing setting (SystemExit with a message does this), never with
    a KeyError traceback. Task 23 runs the image with no settings and pastes the
    message.

    CLEARAIR_FAIL_AFTER_CALLS (task 12) is optional, so it is not required here.
    """
    raise NotImplementedError("TODO(task 8): write load_settings()")
