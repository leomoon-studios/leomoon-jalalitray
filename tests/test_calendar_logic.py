from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path

import pytest

from calendar_logic import FUTURE_YEAR_WINDOW, age_years, date_to_padded_iso, date_to_unpadded_iso, gregorian_to_jalali, gregorian_year_choices, is_gregorian_leap_year, is_jalali_leap_year, jalali_to_gregorian, jalali_weekday, jalali_year_choices, seconds_until_midnight, tray_icon_resource, windows_startup_command


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "calendar_cases.json"
CALENDAR_CASES = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CALENDAR_CASES, ids=lambda case: case["name"])
def test_calendar_conversion_round_trip(case: dict[str, object]) -> None:
    gregorian = date.fromisoformat(str(case["gregorian"]))
    jalali_date = tuple(case["jalali"])
    assert gregorian_to_jalali(gregorian) == jalali_date
    assert jalali_to_gregorian(*jalali_date) == gregorian
    assert jalali_weekday(gregorian) == case["weekday"]


def test_year_choices_include_a_rolling_hundred_year_future_window() -> None:
    today = date(2026, 10, 24)
    assert gregorian_year_choices(today)[0] == "1800"
    assert gregorian_year_choices(today)[-1] == str(today.year + FUTURE_YEAR_WINDOW)
    assert jalali_year_choices(today)[0] == "1200"
    assert int(jalali_year_choices(today)[-1]) >= 1500


def test_date_formatting_and_persian_weekday() -> None:
    value = date(2024, 3, 20)
    assert date_to_unpadded_iso((1403, 1, 1)) == "1403-1-1"
    assert date_to_padded_iso((1403, 1, 1)) == "1403-01-01"
    assert jalali_weekday(value) == "چهارشنبه"


def test_leap_years_and_age_calculation() -> None:
    assert is_gregorian_leap_year(2024)
    assert not is_gregorian_leap_year(2100)
    assert is_jalali_leap_year(1403)
    assert age_years(date(2000, 1, 1), date(2024, 1, 1)) == 24


def test_tray_icon_and_startup_command_boundaries() -> None:
    assert tray_icon_resource(1) == ":/res/tray/01.svg"
    assert tray_icon_resource(31) == ":/res/tray/31.svg"
    executable = r"C:\Program Files\LeoMoon JalaliTray\LeoMoon JalaliTray.exe"
    assert windows_startup_command(executable) == f'"{executable}"'
    with pytest.raises(ValueError):
        tray_icon_resource(32)


def test_seconds_until_midnight() -> None:
    assert seconds_until_midnight(datetime(2026, 10, 24, 23, 59, 59)) == 1


def test_invalid_jalali_date_is_rejected() -> None:
    with pytest.raises(Exception, match="Incorrect Date"):
        jalali_to_gregorian(1403, 13, 1)
