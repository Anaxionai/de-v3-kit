"""Shared test set-up: read the hand-made API pages in tests/fixtures/.

    def test_something(fixture_page):
        page = fixture_page("hours-001.json")

- locations-001.json: a /v3/locations page with 3 locations; two of them have a pm25 sensor.
- hours-001.json: a /v3/sensors/<id>/hours page with 5 hourly results, oldest first.

The values are made up; the shape follows the OpenAQ v3 documentation. Tests never
call the real API and never need a key or a database.
"""

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_page():
    def load(name: str) -> dict:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    return load
