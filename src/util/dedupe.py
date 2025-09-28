"""Deduplication helpers for event lists."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Tuple

from .uid import generate_uid, normalize


def load_registry(path: Path) -> dict[str, dict]:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_registry(path: Path, registry: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, sort_keys=True))


def dedupe_events(events: Iterable[dict], registry_path: Path) -> Tuple[list[dict], list[dict]]:
    """Return (unique_events, duplicates) updating the registry file."""

    registry = load_registry(registry_path)
    unique: dict[str, dict] = {}
    duplicates: list[dict] = []
    for event in events:
        uid = event.get("uid") or generate_uid(event.get("title"), event.get("start_local"), event.get("url") or event.get("location"))
        event["uid"] = uid
        if uid in unique:
            duplicates.append(event)
            continue
        if uid in registry:
            duplicates.append(event)
            continue
        unique[uid] = event
        registry[uid] = {"first_seen": event.get("start_local")}
    save_registry(registry_path, registry)
    return list(unique.values()), duplicates


def make_similarity_key(event: dict) -> str:
    """Return a fuzzy key useful for manual inspection of near-duplicates."""

    title = normalize(event.get("title", ""))
    date = (event.get("start_local") or "").split("T")[0]
    venue_or_url = normalize(event.get("location") or event.get("url") or "")
    return f"{title}|{date}|{venue_or_url}"
