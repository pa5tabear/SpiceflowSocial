from datetime import datetime

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from plan.choose import choose_portfolio

SCORING_CONFIG = {
    "hard_rules": {"no_overlap": True},
}

PREFERENCES = {
    "time_windows": {
        "evenings": {"weekdays": ["17:30", "21:30"]},
        "quiet_hours": ["22:30", "07:00"],
    },
    "caps": {"max_per_day": 1, "max_per_week": 2},
    "quotas": {
        "weekly": {"career_learning_min": 1},
        "monthly": {"major_flagship_min": 1},
    },
    "categories": {"map": {"Lecture": ["career_learning_min"]}},
}


def _event(start_str: str, title: str = "Event") -> dict:
    end = datetime.fromisoformat(start_str).replace(hour=19, minute=0)
    return {
        "title": title,
        "start_local": start_str,
        "end_local": end.isoformat(timespec="minutes"),
        "category": "Lecture",
        "score": 1.0,
    }


def test_choose_portfolio_respects_daily_cap() -> None:
    events = [
        _event("2025-10-01T18:00", "One"),
        _event("2025-10-01T19:00", "Two"),
    ]
    portfolio = choose_portfolio(events, SCORING_CONFIG, PREFERENCES)
    assert len(portfolio["selected"]) == 1
