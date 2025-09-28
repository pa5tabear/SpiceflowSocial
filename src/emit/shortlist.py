"""Shortlist report emitter."""
from __future__ import annotations

from pathlib import Path
from typing import List


def write_shortlist_report(path: Path, events: List[dict], *, limit: int = 10) -> None:
    lines = ["# Event Shortlist", ""]
    if not events:
        lines.append("No events selected. Add sources or enable research mode with API access.")
    else:
        for idx, event in enumerate(events[:limit], start=1):
            title = event.get("title", "Untitled")
            start = event.get("start_local", "?")
            location = event.get("location") or event.get("venue") or "TBD"
            score = event.get("score", 0.0)
            reason = event.get("notes") or event.get("summary") or ""
            lines.extend(
                [
                    f"## {idx}. {title}",
                    f"- When: {start}",
                    f"- Where: {location}",
                    f"- Score: {score}",
                ]
            )
            if event.get("url"):
                lines.append(f"- URL: {event['url']}")
            if reason:
                lines.append(f"- Notes: {reason}")
            lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


__all__ = ["write_shortlist_report"]
