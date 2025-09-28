"""JSON-LD Event ingestion."""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

from bs4 import BeautifulSoup

from util.http_cache import fetch
from util.timez import DEFAULT_TIMEZONE, parse_datetime, to_iso_local
from util.uid import generate_uid


def _extract_events(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        if payload.get("@type") in {"Event", ["Event"]}:
            return [payload]
        if "@graph" in payload:
            return [item for item in payload["@graph"] if isinstance(item, dict)]
    if isinstance(payload, list):
        events: list[dict[str, Any]] = []
        for item in payload:
            events.extend(_extract_events(item))
        return events
    return []


def pull(source: dict[str, Any], *, horizon_days: int) -> list[dict[str, Any]]:
    response = fetch(source["url"])
    soup = BeautifulSoup(response.content, "html.parser")
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})

    now = datetime.now(DEFAULT_TIMEZONE)
    horizon = now + timedelta(days=horizon_days)

    events: list[dict[str, Any]] = []
    for script in scripts:
        try:
            payload = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue
        for item in _extract_events(payload):
            if item.get("@type") not in ("Event", ["Event"]):
                continue
            start = item.get("startDate")
            if not start:
                continue
            start_dt = parse_datetime(start)
            end_dt = parse_datetime(item.get("endDate")) if item.get("endDate") else None
            if end_dt and end_dt < now:
                continue
            if start_dt > horizon:
                continue
            location = item.get("location", {})
            if isinstance(location, dict):
                location_str = location.get("name") or location.get("address", {}).get("streetAddress")
            else:
                location_str = str(location)
            title = item.get("name", "Untitled Event")
            url = item.get("url") or source.get("url")
            uid = generate_uid(title, to_iso_local(start_dt), url or location_str)
            events.append(
                {
                    "uid": uid,
                    "title": title,
                    "start_local": to_iso_local(start_dt),
                    "end_local": to_iso_local(end_dt) if end_dt else None,
                    "all_day": False,
                    "timezone": "America/Detroit",
                    "location": location_str,
                    "city": source.get("city", "Ann Arbor, MI"),
                    "cost": item.get("offers", {}).get("price") if isinstance(item.get("offers"), dict) else "",
                    "category": source.get("category") or item.get("eventType"),
                    "org": item.get("organizer", {}).get("name") if isinstance(item.get("organizer"), dict) else item.get("organizer"),
                    "url": url,
                    "image": item.get("image"),
                    "source": source.get("slug"),
                    "notes": item.get("description", ""),
                }
            )
    return events
