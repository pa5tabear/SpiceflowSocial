"""Configurable HTML scraping fallback."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from bs4 import BeautifulSoup

from util.http_cache import fetch
from util.timez import DEFAULT_TIMEZONE, default_duration_for_event, parse_datetime, to_iso_local
from util.uid import generate_uid


def _extract_field(node, selector: str | None, *, attribute: str | None = None) -> str:
    if not selector:
        return ""
    target = node.select_one(selector)
    if not target:
        return ""
    if attribute:
        return target.get(attribute, "")
    return target.get_text(strip=True)


def pull(source: dict[str, Any], *, horizon_days: int) -> list[dict[str, Any]]:
    config = source.get("html") or {}
    item_selector = config.get("item")
    if not item_selector:
        raise ValueError(f"HTML scraper for {source['slug']} is missing item selector")

    response = fetch(source["url"])
    soup = BeautifulSoup(response.content, "html.parser")
    now = datetime.now(DEFAULT_TIMEZONE)
    horizon = now + timedelta(days=horizon_days)

    events: list[dict[str, Any]] = []
    for node in soup.select(item_selector):
        start_text = _extract_field(node, config.get("datetime"))
        if not start_text:
            continue
        try:
            start_dt = parse_datetime(start_text)
        except Exception:
            continue
        if start_dt > horizon:
            continue
        end_text = _extract_field(node, config.get("endtime"))
        if end_text:
            try:
                end_dt = parse_datetime(end_text)
            except Exception:
                end_dt = start_dt + default_duration_for_event(source.get("category"), False)
        else:
            end_dt = start_dt + default_duration_for_event(source.get("category"), False)

        title = _extract_field(node, config.get("title")) or source.get("name", "Untitled Event")
        location = _extract_field(node, config.get("location")) or source.get("city")
        url_selector = config.get("url")
        url_attr = None
        if url_selector and "::attr(" in url_selector:
            selector, attr = url_selector.split("::attr(")
            url_selector = selector
            url_attr = attr.rstrip(")")
        url = _extract_field(node, url_selector, attribute=url_attr) or source.get("url")

        uid = generate_uid(title, to_iso_local(start_dt), url or location)
        events.append(
            {
                "uid": uid,
                "title": title,
                "start_local": to_iso_local(start_dt),
                "end_local": to_iso_local(end_dt),
                "all_day": False,
                "timezone": "America/Detroit",
                "location": location,
                "city": source.get("city", "Ann Arbor, MI"),
                "cost": source.get("cost", ""),
                "category": source.get("category"),
                "org": source.get("name"),
                "url": url,
                "image": source.get("image"),
                "source": source.get("slug"),
                "notes": _extract_field(node, config.get("notes")),
            }
        )
    return events
