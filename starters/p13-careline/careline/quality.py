"""CareLine's quality checks with Great Expectations (GX Core), at two levels.

- critical (blocking): a failure stops the day before clean and report.
- warning: a failure is saved in report.check_results, and the day is still published.

check_raw in dags/careline_daily.py calls validate_day(). Tests call validate_frame().

Two GX facts that save time:
- suite.add_expectation() needs an active data context: call
  gx.get_context(mode="ephemeral") once before you build a suite.
- Raw values are text, and an empty cell is "" (not null) when read with
  keep_default_na=False. Turn "" into None before a not-null check.
"""

import great_expectations as gx
import pandas as pd


def blocking_suite(day: str, doctor_ids: list[str]) -> gx.ExpectationSuite:
    """The critical Expectations for one day's raw appointments.

    At least: appointment_id not null and unique, doctor_id in `doctor_ids`
    (the ids in raw.doctors), and appointment_date equal to `day`. Give each
    Expectation severity="critical". Match your rules in checks/rules.md.
    """
    raise NotImplementedError("TODO(task 9): the critical suite")


def warning_suite(patient_ids: list[str]) -> gx.ExpectationSuite:
    """The warning Expectations, with severity="warning".

    At least the row-count range and the fee range from your profile. Use
    `mostly` where a few odd rows are allowed. Raw values are text: convert
    fee_rupees with pandas.to_numeric(..., errors="coerce") before a range check.
    If you add the converted values as a new column, add it only for this suite:
    the contract suite (task 10) checks the exact set of columns.
    """
    raise NotImplementedError("TODO(task 9): the warning suite")


def validate_frame(df: pd.DataFrame, suite: gx.ExpectationSuite):
    """Validate a DataFrame against a suite, without a database; return the GX result.

    Each item of result.results has .success, .expectation_config.severity and
    .result.get("unexpected_count").
    """
    raise NotImplementedError("TODO(task 12): move the GX part of validate_day() here")


def save_results(day: str, suite_name: str, result) -> int:
    """Save one row per Expectation to report.check_results; return the rows saved.

    Columns: day, suite, Expectation, success, unexpected count. Replace the
    day's earlier rows for this suite, so a re-run does not add rows.
    """
    raise NotImplementedError("TODO(task 9): save the results as rows")


def validate_day(day: str) -> list[str]:
    """Validate one day's raw appointments with both suites, save every result,
    and return the names of the failed critical Expectations.

    An empty list means the day may be published. Read the day's rows from
    raw.appointments (by source_file) into a DataFrame, and the doctor and
    patient ids from raw.doctors and raw.patients.
    """
    raise NotImplementedError("TODO(task 9): run both suites on one day")


def check_file_present(day: str) -> bool:
    """The completeness check: does the run's own day file exist?

    Return True when data/appointments/appointments_<day>.csv exists. When it
    is missing, save one failed row to report.check_results (suite
    "completeness", Expectation "file_present", unexpected count 1) and return
    False. load_raw then logs a warning and skips the run, so a missing file
    leaves a trace in report.check_results, not only a skipped run.
    """
    raise NotImplementedError("TODO(task 9): the file_present completeness check")
