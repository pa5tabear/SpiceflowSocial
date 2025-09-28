"""Run reporting helpers."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

from util.timez import DEFAULT_TIMEZONE


def write_run_report(path: Path, *, events: list[dict], duplicates: list[dict], skipped_sources: list[str]) -> None:
    now = datetime.now(DEFAULT_TIMEZONE)
    lines = [
        f"# Spiceflow Social Run — {now.strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        f"* Total events scraped: {len(events) + len(duplicates)}",
        f"* Unique events merged: {len(events)}",
        f"* Duplicate events skipped: {len(duplicates)}",
    ]
    if skipped_sources:
        lines.append("* Sources skipped: " + ", ".join(skipped_sources))
    if duplicates:
        lines.append("\n## Duplicate keys")
        for dup in duplicates:
            lines.append(f"- {dup.get('uid')} — {dup.get('title')}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))
