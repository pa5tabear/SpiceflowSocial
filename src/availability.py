"""Availability parsing and summarisation utilities."""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from icalendar import Calendar

from preferences import load_preferences
from util.timez import DEFAULT_TIMEZONE, ensure_timezone


def _iter_events(cal: Calendar) -> Iterable[Tuple[datetime, datetime, str]]:
    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        summary = component.get("summary", "")
        if not dtstart:
            continue
        start = _to_datetime(dtstart.dt)
        if dtend is not None:
            end = _to_datetime(dtend.dt)
        else:
            end = start + timedelta(hours=1)
        yield start, end, str(summary)


def _to_datetime(value: datetime | date) -> datetime:
    if isinstance(value, datetime):
        return ensure_timezone(value, DEFAULT_TIMEZONE)
    return ensure_timezone(datetime.combine(value, datetime.min.time()))


def load_calendar_events(path: Path) -> List[Dict[str, datetime]]:
    if not path.exists():
        return []
    cal = Calendar.from_ical(path.read_bytes())
    events: List[Dict[str, datetime]] = []
    for start, end, summary in _iter_events(cal):
        events.append({"start": start, "end": end, "summary": summary})
    return events


def summarise_evenings(
    events: List[Dict[str, datetime]],
    *,
    preferences: Dict,
    horizon_days: int,
) -> Dict[str, Dict[str, str]]:
    today = datetime.now(DEFAULT_TIMEZONE).date()
    windows = _evening_windows(preferences)

    by_day: Dict[date, List[Tuple[datetime, datetime, str]]] = defaultdict(list)
    for entry in events:
        start = entry["start"]
        end = entry["end"]
        if start.date() < today or start.date() > today + timedelta(days=horizon_days):
            continue
        by_day[start.date()].append((start, end, entry.get("summary", "")))

    summary: Dict[str, Dict[str, str]] = {}
    for offset in range(horizon_days + 1):
        current = today + timedelta(days=offset)
        window = windows.get(current.weekday())
        if not window:
            continue
        window_start, window_end = window
        free = True
        notes: List[str] = []
        for start, end, title in by_day.get(current, []):
            if _overlaps_window(start, end, window_start, window_end):
                free = False
                notes.append(title or "Busy")
        summary[current.isoformat()] = {
            "status": "free" if free else "busy",
            "notes": "; ".join(notes) if notes else "",
        }
    return summary


def _evening_windows(preferences: Dict) -> Dict[int, Tuple[datetime, datetime]]:
    result: Dict[int, Tuple[datetime, datetime]] = {}
    evenings = preferences.get("time_windows", {}).get("evenings", {})
    weekday_window = evenings.get("weekdays")
    if isinstance(weekday_window, (list, tuple)) and len(weekday_window) == 2:
        start = _parse_time(weekday_window[0])
        end = _parse_time(weekday_window[1])
        for idx in range(0, 5):
            result[idx] = (start, end)
    for key in ("saturday", "sunday"):
        value = evenings.get(key)
        if isinstance(value, (list, tuple)) and len(value) == 2:
            result[_weekday_index(key)] = (_parse_time(value[0]), _parse_time(value[1]))
    return result


def _parse_time(label: str) -> datetime:
    hour, minute = map(int, label.split(":"))
    return ensure_timezone(datetime.now(DEFAULT_TIMEZONE).replace(hour=hour, minute=minute, second=0, microsecond=0))


def _weekday_index(name: str) -> int:
    mapping = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    return mapping[name.lower()]


def _overlaps_window(start: datetime, end: datetime, w_start: datetime, w_end: datetime) -> bool:
    start_minutes = start.hour * 60 + start.minute
    end_minutes = end.hour * 60 + end.minute
    w_start_minutes = w_start.hour * 60 + w_start.minute
    w_end_minutes = w_end.hour * 60 + w_end.minute
    if w_start_minutes <= w_end_minutes:
        return not (end_minutes <= w_start_minutes or start_minutes >= w_end_minutes)
    return start_minutes >= w_start_minutes or end_minutes <= w_end_minutes


def write_availability_markdown(path: Path, summary: Dict[str, Dict[str, str]]) -> None:
    lines = ["# Evening Availability Snapshot", ""]
    for day, payload in sorted(summary.items()):
        status = payload.get("status", "free")
        notes = payload.get("notes")
        line = f"- {day}: **{status.upper()}**"
        if notes:
            line += f" — {notes}"
        lines.append(line)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


__all__ = [
    "load_calendar_events",
    "summarise_evenings",
    "write_availability_markdown",
]
