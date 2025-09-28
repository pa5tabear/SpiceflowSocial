"""Generate a weekly review markdown for selected events.

The output is designed for fast human+LLM review with simple approval prompts.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from util.timez import DEFAULT_TIMEZONE


def _event_key(event: Dict[str, Any]) -> str:
    title = str(event.get("title", "")).strip()
    start = str(event.get("start_local", "")).strip()
    return f"{title}|{start}"


def _format_day_heading(day: datetime) -> str:
    return day.strftime("%A, %b %d")


def _format_time_range(event: Dict[str, Any]) -> str:
    start = str(event.get("start_local", ""))
    end = str(event.get("end_local", ""))
    if start and "T" in start:
        start_time = start.split("T")[1][:5]
    else:
        start_time = ""
    if end and "T" in end:
        end_time = end.split("T")[1][:5]
    else:
        end_time = ""
    if start_time and end_time:
        return f"{start_time} - {end_time}"
    return start_time or "(time TBD)"


def write_weekly_review(
    selected_events: Iterable[Dict[str, Any]],
    portfolio_data: Dict[str, Any],
    availability: Dict[str, Any],
    output_path: Path,
    *,
    previous_selected: Optional[Iterable[Dict[str, Any]]] = None,
) -> None:
    """Write a reviewer-friendly weekly overview markdown file.

    Args:
        selected_events: Events selected by the portfolio chooser
        portfolio_data: Full portfolio payload (for scores/summary)
        availability: Daily availability summary keyed by ISO date
        output_path: Path to write markdown file
        previous_selected: Previously selected events (to preserve approvals)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    prev_keys = {_event_key(ev) for ev in (previous_selected or [])}

    by_day: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for ev in selected_events:
        start = str(ev.get("start_local", ""))
        day_key = start.split("T")[0] if start else ""
        by_day[day_key].append(ev)

    today = datetime.now(DEFAULT_TIMEZONE).date()
    start_date = today
    end_date = today + timedelta(days=6)

    lines: List[str] = []
    lines.append(f"# Weekly Event Review - {start_date.isoformat()} - {end_date.isoformat()}")
    lines.append(f"**Status:** {len(list(selected_events))} events selected for next 7 days")
    lines.append(f"**Last Updated:** {datetime.now(DEFAULT_TIMEZONE).strftime('%Y-%m-%d %H:%M %Z')}")
    lines.append("**ICS File:** `data/out/winners.ics` (ready to import)")
    lines.append("")
    lines.append("## 📅 Daily Breakdown")
    lines.append("")

    for offset in range(7):
        day = today + timedelta(days=offset)
        day_key = day.isoformat()
        events = by_day.get(day_key, [])
        availability_info = availability.get(day_key, {}) if availability else {}

        lines.append(f"### { _format_day_heading(datetime.combine(day, datetime.min.time())) }")
        if not events:
            lines.append("**🔍 NEEDS REVIEW** No events currently selected")
            lines.append("- **Suggestions:** Check for late-added events, consider backup options")
            lines.append("- **Actions:** [ ] Find alternatives [ ] Keep open [ ] Add specific search")
            lines.append("")
            continue

        for ev in events:
            key = _event_key(ev)
            status = "✅ APPROVED" if key in prev_keys else "🔍 NEEDS REVIEW"
            title = str(ev.get("title", "(untitled)"))
            where = str(ev.get("location", "(location TBD)"))
            when = _format_time_range(ev)
            score = ev.get("score", None)
            score_str = f"{score:.2f}" if isinstance(score, (int, float)) else "n/a"
            rationale = ev.get("fit_rationale") or ev.get("score_breakdown") or ""

            lines.append(f"**{status}** {title}")
            lines.append(f"- **When:** {when}")
            lines.append(f"- **Where:** {where}")
            if rationale:
                lines.append(f"- **Why Selected:** {rationale}")
            lines.append(f"- **Score:** {score_str}")
            lines.append("- **Actions:** [ ] Keep [ ] Modify [ ] Cancel")
            lines.append("")

    lines.append("## 🎯 Weekly Overview")
    summary = portfolio_data.get("summary") or {}
    if summary:
        for key, value in summary.items():
            lines.append(f"- **{key}**: {value}")
    else:
        lines.append("- **Overview**: Summary not available")
    lines.append("")

    lines.append("## 📝 Quick Edit Commands")
    lines.append("**To approve all:** \"Approve all suggested events\"")
    lines.append("**To cancel specific:** \"Cancel [event name] on [day]\"")
    lines.append("**To modify:** \"Move [event name] to [new time] if possible\"")
    lines.append("**To add:** \"Find [type] event for [day] evening\"")
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


