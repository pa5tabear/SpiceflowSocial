"""Run reporting helpers."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Dict

from util.timez import DEFAULT_TIMEZONE


def write_run_report(
    path: Path,
    *,
    events: list[dict],
    duplicates: list[dict],
    skipped_sources: list[str],
    portfolio_summary: Optional[dict] = None,
    research_summaries: Optional[List[dict]] = None,
    availability_summary: Optional[Dict[str, Dict[str, str]]] = None,
) -> None:
    now = datetime.now(DEFAULT_TIMEZONE)
    lines = [
        f"# Spiceflow Social Run — {now.strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        f"* Total events analysed: {len(events) + len(duplicates)}",
        f"* Unique events merged: {len(events)}",
        f"* Duplicate events skipped: {len(duplicates)}",
    ]
    if skipped_sources:
        lines.append("* Sources skipped: " + ", ".join(skipped_sources))

    if portfolio_summary:
        lines.extend([
            "",
            "## Portfolio Summary",
            f"- Selected events: {portfolio_summary.get('total_selected', 0)}",
            f"- Weeks scheduled: {portfolio_summary.get('weeks_scheduled', 0)}",
        ])
        quota_progress = portfolio_summary.get("quota_progress", {})
        if quota_progress:
            lines.append("- Quota Progress:")
            weekly = quota_progress.get("weekly", {})
            for goal, payload in weekly.items():
                lines.append(
                    f"  * Weekly {goal}: {payload.get('max_count', 0)}/{payload.get('target', 0)}"
                )
            monthly = quota_progress.get("monthly", {})
            for goal, payload in monthly.items():
                lines.append(
                    f"  * Monthly {goal}: {payload.get('count', 0)}/{payload.get('target', 0)}"
                )

    if availability_summary:
        free_days = [day for day, payload in availability_summary.items() if payload.get("status") == "free"]
        lines.extend(["", "## Availability Overview", f"- Free evenings: {len(free_days)}", f"- Total tracked evenings: {len(availability_summary)}"])

    if research_summaries:
        lines.extend(["", "## LLM Research Highlights"])
        for entry in research_summaries:
            lines.append(f"- {entry.get('slug')}: {entry.get('summary', 'n/a')}")

    if duplicates:
        lines.append('\n## Duplicate keys')
        for dup in duplicates:
            lines.append(f"- {dup.get('uid')} — {dup.get('title')}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines))
