"""ICS writing helpers."""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

from icalendar import Calendar, Event

from util.timez import DEFAULT_TIMEZONE, ensure_timezone


def _event_component(event: dict, *, cancelled: bool = False) -> Event:
    component = Event()
    component.add("uid", event["uid"])
    component.add("summary", event.get("title", "Untitled Event"))
    start = ensure_timezone(datetime.fromisoformat(event["start_local"]))
    component.add("dtstart", start)
    end_value = event.get("end_local")
    if end_value:
        end = ensure_timezone(datetime.fromisoformat(end_value))
    else:
        end = start + timedelta(hours=1, minutes=30)
    component.add("dtend", end)
    component.add("dtstamp", ensure_timezone(datetime.now(DEFAULT_TIMEZONE)))
    if location := event.get("location"):
        component.add("location", location)
    if url := event.get("url"):
        component.add("url", url)
    if description := event.get("notes"):
        component.add("description", description)
    if cancelled:
        component.add("status", "CANCELLED")
    elif event.get("all_day"):
        component.add("transp", "TRANSPARENT")
    return component


def write_ics(events: Iterable[dict], path: Path, *, calendar_name: str = "Spiceflow Social", cancelled: bool = False) -> None:
    calendar = Calendar()
    calendar.add("prodid", "-//Spiceflow Social//EN")
    calendar.add("version", "2.0")
    calendar.add("X-WR-CALNAME", calendar_name)
    for event in events:
        calendar.add_component(_event_component(event, cancelled=cancelled))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(calendar.to_ical())
