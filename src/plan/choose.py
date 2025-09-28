"""Portfolio selection logic."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from util.timez import ensure_timezone, in_quiet_hours, week_key


def _overlaps(existing: list[tuple[datetime, datetime]], start: datetime, end: datetime) -> bool:
    for other_start, other_end in existing:
        latest_start = max(start, other_start)
        earliest_end = min(end, other_end)
        if latest_start < earliest_end:
            return True
    return False


def choose_portfolio(events: list[dict], config: dict) -> dict:
    hard_rules = config.get("hard_rules", {})
    quiet_pairs: list[tuple[str, str]] = []
    for window in hard_rules.get("evening_quiet_hours", []):
        if isinstance(window, (list, tuple)) and len(window) == 2:
            quiet_pairs.append((window[0], window[1]))

    max_events_per_week = hard_rules.get("max_events_per_week", 6)
    selections: list[dict] = []
    per_week_counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    scheduled_windows: list[tuple[datetime, datetime]] = []

    for event in sorted(events, key=lambda e: e.get("score", 0.0), reverse=True):
        start = ensure_timezone(datetime.fromisoformat(event["start_local"]))
        end_str = event.get("end_local")
        end = ensure_timezone(datetime.fromisoformat(end_str)) if end_str else start + timedelta(hours=1, minutes=30)

        if hard_rules.get("no_overlap") and _overlaps(scheduled_windows, start, end):
            continue

        if quiet_pairs and in_quiet_hours(start, end, quiet_pairs):
            continue

        wk = week_key(start)
        if per_week_counts[wk] >= max_events_per_week:
            continue

        selections.append(event)
        per_week_counts[wk] += 1
        scheduled_windows.append((start, end))

    return {
        "selected": selections,
        "summary": {
            "total_selected": len(selections),
            "weeks_scheduled": len({week for week, count in per_week_counts.items() if count}),
        },
    }


def write_portfolio(portfolio: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(portfolio, indent=2, sort_keys=True))
