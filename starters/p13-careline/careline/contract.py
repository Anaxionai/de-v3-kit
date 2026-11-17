"""The appointments data contract (contracts/appointments.yaml), used at the door and in check_raw.

- load_day() calls check_header() before it inserts a file.
- check_raw validates contract_suite() with the other critical checks.
- tests/test_contract.py checks both on the sample files.
"""

from pathlib import Path

import great_expectations as gx

CONTRACT_PATH = Path(__file__).resolve().parents[1] / "contracts" / "appointments.yaml"


def load_contract(path: str | Path = CONTRACT_PATH) -> dict:
    """Read the contract YAML with yaml.safe_load and return it as a dict.

    The appointments columns are in contract["schema"][0]["properties"].
    """
    raise NotImplementedError("TODO(task 10): read the contract")


def check_header(columns: list[str], contract: dict) -> None:
    """Refuse a file whose columns are not exactly the contract's columns.

    Raise ValueError with a message that names the missing columns and the
    extra columns, for example: missing ['fee_rupees'], extra ['fee'].
    Return None when they match.
    """
    raise NotImplementedError("TODO(task 10): compare the header with the contract")


def contract_suite(contract: dict) -> gx.ExpectationSuite:
    """Turn the contract into critical Expectations.

    The exact column set, not null for required columns, unique for unique
    columns, and the allowed values of every property with an invalidValues
    quality rule. Give each Expectation severity="critical".
    """
    raise NotImplementedError("TODO(task 10): build the contract suite")
