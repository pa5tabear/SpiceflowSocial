"""Event scoring utilities."""
from __future__ import annotations

from typing import Dict, Iterable, List

from preferences import (
    category_goals_map,
    expand_goal_weights,
    goal_keywords_from_config,
    must_see_keywords,
)
from util.uid import normalize


def _text_matches_keywords(text: str, keywords: Iterable[str]) -> int:
    text_norm = normalize(text)
    count = 0
    for keyword in keywords:
        keyword_norm = normalize(keyword)
        if keyword_norm and keyword_norm in text_norm:
            count += 1
    return count


def _event_goal_keys(event: dict, category_map: Dict[str, List[str]]) -> List[str]:
    goal_keys: List[str] = []
    candidates: List[str] = []
    if category := event.get("category"):
        if isinstance(category, str):
            candidates.append(category)
        elif isinstance(category, Iterable):
            candidates.extend(str(item) for item in category)
    tags = event.get("tags")
    if tags:
        if isinstance(tags, str):
            candidates.append(tags)
        else:
            candidates.extend(str(tag) for tag in tags)
    for candidate in candidates:
        key = candidate.lower()
        if key in category_map:
            goal_keys.extend(category_map[key])
    return goal_keys


def _apply_must_see_bonus(event: dict, keywords: Iterable[str], weight: float) -> float:
    title = normalize(event.get("title", ""))
    notes = normalize(event.get("notes", ""))
    for keyword in keywords:
        keyword_norm = normalize(keyword)
        if keyword_norm in title or keyword_norm in notes:
            return weight
    return 0.0


def _late_start_penalty(event: dict, preferences: dict, weight: Dict[str, float]) -> float:
    start_str = event.get("start_local")
    if not start_str:
        return 0.0
    start_time_pref = preferences.get("preferences", {}).get("start_time", {})
    penalty_after = start_time_pref.get("late_start_penalty_after")
    penalty_value = start_time_pref.get("late_start_penalty", weight.get("evening_penalty", -0.05))
    if not penalty_after:
        return 0.0
    try:
        hour = int(start_str.split("T")[1].split(":")[0])
    except Exception:
        return 0.0
    penalty_hour = int(penalty_after.split(":")[0])
    if hour >= penalty_hour:
        return penalty_value
    return 0.0


def score_event(event: dict, config: dict, preferences: dict) -> float:
    weights = expand_goal_weights(config, preferences)
    goal_keywords = goal_keywords_from_config(config)
    category_map = category_goals_map(preferences)
    must_see_list = must_see_keywords(preferences)

    text = " ".join(
        filter(
            None,
            [
                event.get("title"),
                event.get("notes"),
                event.get("category"),
                event.get("org"),
                event.get("url"),
            ],
        )
    )

    score = 0.0

    # Goal keyword matches weigh heavily.
    for goal_key, keywords in goal_keywords.items():
        matches = _text_matches_keywords(text, keywords)
        weight_key = f"goals.{goal_key}"
        score += matches * weights.get(weight_key, 0.0)

    # Category-driven goal reinforcement.
    for derived_goal in _event_goal_keys(event, category_map):
        weight_key = f"goals.{derived_goal}"
        score += weights.get(weight_key, 0.0)

    category_weights = config.get("category_weights", {})
    if category := event.get("category"):
        if isinstance(category, str):
            score += category_weights.get(category.lower(), 0.0)

    # Travel penalty/bonus if travel minutes available.
    travel_minutes = event.get("travel_minutes")
    if isinstance(travel_minutes, (int, float)):
        if travel_minutes > 45:
            score += weights.get("travel_time_penalty", -0.1)
        elif travel_minutes <= 30:
            score += abs(weights.get("travel_time_penalty", -0.1)) * 0.3

    cost_text = event.get("cost", "")
    if cost_text:
        if "free" in cost_text.lower():
            score += config.get("cost_preferences", {}).get("free_bonus", 0.0)
        else:
            score += weights.get("cost_penalty", 0.0)

    if event.get("source") in config.get("novelty_sources", []):
        score += weights.get("novelty", 0.0)

    score += _late_start_penalty(event, preferences, weights)
    score += _apply_must_see_bonus(event, must_see_list, weights.get("must_see_bonus", 0.0))

    return round(score, 4)


def attach_scores(events: list[dict], config: dict, preferences: dict) -> list[dict]:
    for event in events:
        event["score"] = score_event(event, config, preferences)
    return events
