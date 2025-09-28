"""Portfolio selection logic."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from preferences import category_goals_map, quiet_windows_from_preferences
from util.timez import ensure_timezone, in_quiet_hours, week_key

WEEKDAY_INDICES = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def _overlaps(existing: list[tuple[datetime, datetime]], start: datetime, end: datetime) -> bool:
    for other_start, other_end in existing:
        latest_start = max(start, other_start)
        earliest_end = min(end, other_end)
        if latest_start < earliest_end:
            return True
    return False


def _build_evening_windows(preferences: dict) -> Dict[int, Tuple[str, str]]:
    windows: Dict[int, Tuple[str, str]] = {}
    evenings = preferences.get("time_windows", {}).get("evenings", {})
    weekdays = evenings.get("weekdays")
    if isinstance(weekdays, (list, tuple)) and len(weekdays) == 2:
        for day in range(0, 5):
            windows[day] = (str(weekdays[0]), str(weekdays[1]))
    for key in ("saturday", "sunday"):
        value = evenings.get(key)
        if isinstance(value, (list, tuple)) and len(value) == 2:
            windows[WEEKDAY_INDICES[key]] = (str(value[0]), str(value[1]))
    return windows


def _within_window(start: datetime, windows: Dict[int, Tuple[str, str]]) -> bool:
    if not windows:
        return True
    day_index = start.weekday()
    if day_index not in windows:
        return True
    start_str, end_str = windows[day_index]
    start_hour, start_minute = map(int, start_str.split(":"))
    end_hour, end_minute = map(int, end_str.split(":"))
    start_minutes = start.hour * 60 + start.minute
    window_start = start_hour * 60 + start_minute
    window_end = end_hour * 60 + end_minute
    if window_start <= window_end:
        return window_start <= start_minutes <= window_end
    # Window wraps around midnight.
    return start_minutes >= window_start or start_minutes <= window_end


def choose_portfolio(events: list[dict], config: dict, preferences: dict) -> dict:
    hard_rules = config.get("hard_rules", {})
    prefs_caps = preferences.get("caps", {})
    evening_windows = _build_evening_windows(preferences)
    quiet_pairs = quiet_windows_from_preferences(preferences)
    if not quiet_pairs:
        quiet_pairs = hard_rules.get("evening_quiet_hours", [])

    max_events_per_week = prefs_caps.get("max_per_week", hard_rules.get("max_events_per_week", 6))
    max_events_per_day = prefs_caps.get("max_per_day", 2)
    max_weekend_total = prefs_caps.get("max_weekend_total", 4)

    selections: list[dict] = []
    per_week_counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    per_day_counts: defaultdict[str, int] = defaultdict(int)
    weekend_counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    scheduled_windows: list[tuple[datetime, datetime]] = []

    weekly_goal_targets = preferences.get("quotas", {}).get("weekly", {})
    monthly_goal_targets = preferences.get("quotas", {}).get("monthly", {})
    goal_map = category_goals_map(preferences)
    weekly_goal_counts: defaultdict[tuple[int, int], defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    monthly_goal_counts: defaultdict[str, int] = defaultdict(int)

    for event in sorted(events, key=lambda e: e.get("score", 0.0), reverse=True):
        start = ensure_timezone(datetime.fromisoformat(event["start_local"]))
        end_str = event.get("end_local")
        end = ensure_timezone(datetime.fromisoformat(end_str)) if end_str else start + timedelta(hours=1, minutes=30)

        if hard_rules.get("no_overlap") and _overlaps(scheduled_windows, start, end):
            continue

        if quiet_pairs and in_quiet_hours(start, end, quiet_pairs):
            continue

        if not _within_window(start, evening_windows):
            continue

        wk = week_key(start)
        day_key = start.date().isoformat()
        if per_week_counts[wk] >= max_events_per_week:
            continue
        if per_day_counts[day_key] >= max_events_per_day:
            continue
        if start.weekday() >= 5 and weekend_counts[wk] >= max_weekend_total:
            continue

        selections.append(event)
        per_week_counts[wk] += 1
        per_day_counts[day_key] += 1
        if start.weekday() >= 5:
            weekend_counts[wk] += 1
        scheduled_windows.append((start, end))

        mapped_goals = goal_map.get(event.get("category", "").lower(), [])
        if not mapped_goals and event.get("tags"):
            tags = event.get("tags")
            tag_list = tags if isinstance(tags, (list, tuple)) else [tags]
            for key, goals in goal_map.items():
                if any(key in str(tag).lower() for tag in tag_list):
                    mapped_goals = goals
                    break
        for goal in mapped_goals:
            weekly_goal_counts[wk][goal] += 1
            monthly_goal_counts[goal] += 1

    quota_progress = {
        "weekly": {
            goal: {
                "target": weekly_goal_targets.get(goal, 0),
                "max_count": max((counts.get(goal, 0) for counts in weekly_goal_counts.values()), default=0),
            }
            for goal in weekly_goal_targets
        },
        "monthly": {
            goal: {
                "target": monthly_goal_targets.get(goal, 0),
                "count": monthly_goal_counts.get(goal, 0),
            }
            for goal in monthly_goal_targets
        },
    }

    return {
        "selected": selections,
        "summary": {
            "total_selected": len(selections),
            "weeks_scheduled": len({week for week, count in per_week_counts.items() if count}),
            "quota_progress": quota_progress,
        },
    }


def write_portfolio(portfolio: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    import json

    path.write_text(json.dumps(portfolio, indent=2, sort_keys=True))
