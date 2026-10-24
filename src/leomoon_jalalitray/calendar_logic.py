"""Pure calendar, formatting, and tray helpers for LeoMoon JalaliTray."""

from __future__ import annotations

import calendar
from datetime import date, datetime

from persiantools.jdatetime import JalaliDate


GREGORIAN_YEAR_START = 1800
JALALI_YEAR_START = 1200
FUTURE_YEAR_WINDOW = 100
JALALI_WEEKDAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
JALALI_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
GREGORIAN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def future_gregorian_year(today: date | None = None) -> int:
    return (today or date.today()).year + FUTURE_YEAR_WINDOW


def gregorian_year_choices(today: date | None = None) -> list[str]:
    return [str(year) for year in range(GREGORIAN_YEAR_START, future_gregorian_year(today) + 1)]


def jalali_year_choices(today: date | None = None) -> list[str]:
    upper_date = date(future_gregorian_year(today), 12, 31)
    upper_year = gregorian_to_jalali(upper_date)[0]
    return [str(year) for year in range(JALALI_YEAR_START, upper_year + 1)]


def gregorian_to_jalali(value: date) -> tuple[int, int, int]:
    converted = JalaliDate(value)
    return converted.year, converted.month, converted.day


def jalali_to_gregorian(year: int, month: int, day: int) -> date:
    return JalaliDate(year, month, day).to_gregorian()


def date_to_unpadded_iso(value: date | tuple[int, int, int]) -> str:
    year, month, day = value if isinstance(value, tuple) else (value.year, value.month, value.day)
    return f"{year}-{month}-{day}"


def date_to_padded_iso(value: date | tuple[int, int, int]) -> str:
    year, month, day = value if isinstance(value, tuple) else (value.year, value.month, value.day)
    return f"{year:04d}-{month:02d}-{day:02d}"


def jalali_weekday(value: date) -> str:
    return JALALI_WEEKDAYS[value.weekday()]


def is_gregorian_leap_year(year: int) -> bool:
    return calendar.isleap(year)


def is_jalali_leap_year(year: int) -> bool:
    return year % 33 in {1, 5, 9, 13, 17, 22, 26, 30}


def age_years(born: date, today: date | None = None) -> int:
    return int(((today or date.today()) - born).days / 365.2425)


def tray_icon_resource(day: int) -> str:
    if not 1 <= day <= 31:
        raise ValueError("Tray icon day must be between 1 and 31.")
    return f":/res/tray/{day:02d}.svg"


def seconds_until_midnight(now: datetime | None = None) -> int:
    value = now or datetime.now()
    return ((24 - value.hour - 1) * 60 * 60) + ((60 - value.minute - 1) * 60) + (60 - value.second)


def windows_startup_command(executable: str) -> str:
    return f'"{executable}"'
