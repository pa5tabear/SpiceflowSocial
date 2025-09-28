"""ICS source ingestion."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from icalendar import Calendar

from util.http_cache import fetch
from util.timez import DEFAULT_TIMEZONE, ensure_all_day_bounds, to_iso_local
from util.uid import generate_uid


def pull(source: dict[str, Any], *, horizon_days: int) -> list[dict[str, Any]]:
    response = fetch(source["url"])
    calendar = Calendar.from_ical(response.content)

    now = datetime.now(DEFAULT_TIMEZONE)
    horizon = now + timedelta(days=horizon_days)
    events: list[dict[str, Any]] = []

    for component in calendar.walk("VEVENT"):
        start_raw = component.get("dtstart")
        end_raw = component.get("dtend") or component.get("dtstart")
        if not start_raw:
            continue
        start_dt, end_dt, all_day = ensure_all_day_bounds(start_raw.dt, end_raw.dt if hasattr(end_raw, "dt") else end_raw)
        if end_dt < now or start_dt > horizon:
            continue
        title = str(component.get("summary", "Untitled Event"))
        location = str(component.get("location", "")) or source.get("city")
        notes = str(component.get("description", "")).strip()
        url = str(component.get("url", ""))
        uid = component.get("uid")
        if uid:
            uid_value = str(uid)
        else:
            uid_value = generate_uid(title, to_iso_local(start_dt), url or location)

        events.append(
            {
                "uid": uid_value,
                "title": title,
                "start_local": to_iso_local(start_dt),
                "end_local": to_iso_local(end_dt),
                "all_day": all_day,
                "timezone": "America/Detroit",
                "location": location,
                "city": source.get("city", "Ann Arbor, MI"),
                "cost": str(component.get("cost", source.get("cost", ""))),
                "category": source.get("category"),
                "org": source.get("name"),
                "url": url,
                "image": source.get("image"),
                "source": source.get("slug"),
                "notes": notes,
            }
        )
    return events
