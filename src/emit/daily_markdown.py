"""Daily markdown agenda emitter."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List

from util.timez import DEFAULT_TIMEZONE


def write_daily_markdowns(
    events: Iterable[dict],
    availability: Dict[str, Dict[str, str]] | None,
    *,
    horizon_days: int,
    output_dir: Path,
) -> List[dict]:
    availability = availability or {}
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now(DEFAULT_TIMEZONE).date()
    events_by_day: Dict[str, List[dict]] = defaultdict(list)
    for event in events:
        start = event.get("start_local")
        if not start:
            continue
        day = start.split("T")[0]
        events_by_day[day].append(event)

    daily_summaries: List[dict] = []

    for offset in range(horizon_days):
        day = today + timedelta(days=offset)
        day_key = day.isoformat()
        slate = sorted(events_by_day.get(day_key, []), key=lambda e: e.get("score", 0), reverse=True)

        primary = slate[0] if slate else None
        alternatives = slate[1:3] if slate else []
        availability_info = availability.get(day_key, {})

        path = output_dir / f"{day_key}.md"
        lines = [f"# {day.strftime('%A, %B %d, %Y')}", ""]
        lines.append(f"Availability: {availability_info.get('status', 'unknown').upper() if availability_info else 'UNKNOWN'}")
        if availability_info.get("notes"):
            lines.append(f"Existing events: {availability_info['notes']}")
        lines.append("")

        if primary:
            lines.extend(_format_slot("Primary Evening Plan", primary))
        else:
            lines.append("## Primary Evening Plan")
            lines.append("No high-confidence recommendation today. Consider reviewing alternatives or adding a manual plan.\n")

        lines.append("## Alternatives")
        if alternatives:
            for idx, alt in enumerate(alternatives, 1):
                lines.extend(_format_slot(f"Option {idx}", alt, heading=False))
        else:
            lines.append("- None available\n")

        lines.append("## Rationale")
        if primary:
            rationale = primary.get("fit_rationale") or primary.get("notes") or "Balances goals based on current preferences."
            lines.append(f"- Primary: {rationale}")
        if alternatives:
            for alt in alternatives:
                rationale = alt.get("fit_rationale") or alt.get("notes") or "Goal-aligned fallback."
                lines.append(f"- Alt: {alt.get('title')}: {rationale}")
        if not primary and not alternatives:
            lines.append("No events returned for this day. Consider sourcing new options or adjusting preferences.")
        lines.append("")

        path.write_text("\n".join(lines))

        daily_summaries.append(
            {
                "date": day_key,
                "primary": primary,
                "alternatives": alternatives,
                "availability": availability_info,
            }
        )

    return daily_summaries


def _format_slot(title: str, event: dict, *, heading: bool = True) -> List[str]:
    lines: List[str] = []
    if heading:
        lines.append(f"## {title}")
    else:
        lines.append(f"- **{title}:** {event.get('title', 'Untitled')}" )
        details = []
        start = event.get("start_local")
        if start:
            details.append(start)
        if event.get("location"):
            details.append(event["location"])
        if details:
            lines.append(f"  - When/Where: {', '.join(details)}")
        if event.get("url"):
            lines.append(f"  - Link: {event['url']}")
        if event.get("cost"):
            lines.append(f"  - Cost: {event['cost']}")
        if event.get("travel_minutes") not in (None, ""):
            lines.append(f"  - Travel: {event['travel_minutes']} minutes")
        if event.get("tags"):
            lines.append(f"  - Tags: {', '.join(event['tags'])}")
        rationale = event.get("fit_rationale") or event.get("notes")
        if rationale:
            lines.append(f"  - Why it fits: {rationale}")
        lines.append("")
        return lines

    lines.append(f"### {event.get('title', 'Untitled')}" )
    details = []
    if event.get("start_local"):
        details.append(event["start_local"])
    if event.get("location"):
        details.append(event["location"])
    if details:
        lines.append(f"- When/Where: {', '.join(details)}")
    if event.get("url"):
        lines.append(f"- Link: {event['url']}")
    if event.get("cost"):
        lines.append(f"- Cost: {event['cost']}")
    if event.get("travel_minutes") not in (None, ""):
        lines.append(f"- Travel: {event['travel_minutes']} minutes")
    if event.get("tags"):
        lines.append(f"- Tags: {', '.join(event['tags'])}")
    if event.get("novelty_score") not in (None, ""):
        lines.append(f"- Novelty score: {event['novelty_score']}")
    rationale = event.get("fit_rationale") or event.get("notes")
    if rationale:
        lines.append(f"- Why it fits: {rationale}")
    lines.append("")
    return lines


def write_changes_summary(path: Path, daily_summaries: List[dict]) -> None:
    lines = ["# Suggested Adjustments", ""]
    for entry in daily_summaries:
        primary = entry.get("primary")
        date = entry["date"]
        if not primary:
            lines.append(f"- {date}: No primary event selected. Investigate new options or revisit sources.")
        elif entry.get("availability", {}).get("status", "free").lower() == "busy":
            lines.append(f"- {date}: Primary suggestion conflicts with a busy evening; consider rescheduling or picking an alternative.")
    if len(lines) == 2:
        lines.append("All days have primary suggestions aligned with current availability.")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


__all__ = ["write_daily_markdowns", "write_changes_summary"]
