"""Time handling utilities for Spiceflow Social."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Iterable, Tuple
from zoneinfo import ZoneInfo

from dateutil import parser

DEFAULT_TIMEZONE = ZoneInfo("America/Detroit")


def ensure_timezone(dt: datetime, tz: ZoneInfo | None = None) -> datetime:
    """Ensure that ``dt`` has timezone information.

    If ``dt`` is naive the provided timezone (default America/Detroit) is
    attached. When ``dt`` already has tzinfo it is converted to the desired
    timezone for consistent downstream comparison.
    """

    tz = tz or DEFAULT_TIMEZONE
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def parse_datetime(value: str, tz: ZoneInfo | None = None) -> datetime:
    """Parse a wide variety of datetime strings.

    The scraper inputs are intentionally flexible: ICS timestamps, ISO-8601
    strings, or free-form text from HTML calendars. ``dateutil`` provides the
    best compromise between robustness and size for this use case.
    """

    tz = tz or DEFAULT_TIMEZONE
    dt = parser.parse(value)
    return ensure_timezone(dt, tz)


def default_duration_for_event(category: str | None, all_day: bool) -> timedelta:
    """Provide a reasonable fallback duration when an end time is missing."""

    if all_day:
        return timedelta(hours=12)
    if not category:
        return timedelta(hours=2)
    category_lower = category.lower()
    if "conference" in category_lower or "fair" in category_lower:
        return timedelta(hours=4)
    if "workshop" in category_lower or "seminar" in category_lower:
        return timedelta(hours=2)
    if "fitness" in category_lower or "outdoor" in category_lower:
        return timedelta(hours=1, minutes=30)
    return timedelta(hours=1, minutes=15)


def in_quiet_hours(start: datetime, end: datetime, quiet_windows: Iterable[Tuple[str, str]] | None) -> bool:
    """Return True if the event overlaps configured quiet hours."""

    if not quiet_windows:
        return False
    for start_str, end_str in quiet_windows:
        quiet_start = parser.parse(start_str).time()
        quiet_end = parser.parse(end_str).time()
        if quiet_start <= quiet_end:
            if quiet_start <= start.time() < quiet_end:
                return True
        else:
            # Window wraps midnight.
            if start.time() >= quiet_start or start.time() < quiet_end:
                return True
        if quiet_start <= end.time() < quiet_end:
            return True
    return False


def week_key(dt: datetime) -> Tuple[int, int]:
    """Return (year, ISO week number) for grouping constraints."""

    iso = dt.isocalendar()
    return iso.year, iso.week


def to_iso_local(dt: datetime) -> str:
    """Return an ISO formatted string without timezone suffix."""

    dt = ensure_timezone(dt)
    return dt.strftime("%Y-%m-%dT%H:%M")


def ensure_all_day_bounds(start: datetime | date, end: datetime | date) -> tuple[datetime, datetime, bool]:
    """Normalize VEVENT start/end pairs to timezone-aware datetimes."""

    tz = DEFAULT_TIMEZONE
    if isinstance(start, date) and not isinstance(start, datetime):
        start_dt = datetime.combine(start, datetime.min.time(), tz)
        if isinstance(end, date) and not isinstance(end, datetime):
            # DTEND for all-day events points to the next day per RFC5545.
            end_dt = datetime.combine(end, datetime.min.time(), tz)
        else:
            end_dt = ensure_timezone(end, tz)
        return start_dt, end_dt, True
    start_dt = ensure_timezone(start if isinstance(start, datetime) else datetime.combine(start, datetime.min.time()), tz)
    if isinstance(end, datetime):
        end_dt = ensure_timezone(end, tz)
    elif isinstance(end, date):
        end_dt = ensure_timezone(datetime.combine(end, datetime.min.time()), tz)
    else:
        raise TypeError("Unsupported end value type")
    return start_dt, end_dt, False
