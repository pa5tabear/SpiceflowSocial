"""Preference loading and helper utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml


def load_preferences(path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    return data or {}


def expand_goal_weights(scoring_config: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, float]:
    """Combine scoring weights with preference goal weights."""

    weights = dict(scoring_config.get("weights", {}))
    pref_weights = preferences.get("weights", {})
    goal_weights = pref_weights.get("goals", {}) if isinstance(pref_weights, dict) else {}
    for goal, value in goal_weights.items():
        weights[f"goals.{goal}"] = value
    # Copy non-goal weights, pref values take precedence.
    for key, value in pref_weights.items():
        if key == "goals":
            continue
        weights[key] = value
    return weights


def category_goals_map(preferences: Dict[str, Any]) -> Dict[str, List[str]]:
    mapping = preferences.get("categories", {}).get("map", {})
    normalised: Dict[str, List[str]] = {}
    for key, goals in mapping.items():
        key_lower = key.lower()
        if isinstance(goals, str):
            normalised[key_lower] = [goals]
        else:
            normalised[key_lower] = [g for g in goals if g]
    return normalised


def must_see_keywords(preferences: Dict[str, Any]) -> List[str]:
    return preferences.get("categories", {}).get("must_see_keywords", [])


def quiet_windows_from_preferences(preferences: Dict[str, Any]) -> List[tuple[str, str]]:
    quiet = preferences.get("time_windows", {}).get("quiet_hours")
    if not quiet:
        return []
    if isinstance(quiet, (list, tuple)) and len(quiet) == 2 and all(isinstance(v, str) for v in quiet):
        return [(quiet[0], quiet[1])]
    windows: List[tuple[str, str]] = []
    if isinstance(quiet, list):
        for entry in quiet:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                windows.append((str(entry[0]), str(entry[1])))
    return windows


def goal_keywords_from_config(scoring_config: Dict[str, Any]) -> Dict[str, Iterable[str]]:
    return scoring_config.get("goal_keywords", {})


__all__ = [
    "load_preferences",
    "expand_goal_weights",
    "category_goals_map",
    "must_see_keywords",
    "quiet_windows_from_preferences",
    "goal_keywords_from_config",
]
