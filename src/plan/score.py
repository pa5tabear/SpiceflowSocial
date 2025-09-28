"""Event scoring utilities."""
from __future__ import annotations

import math
from typing import Iterable

from util.uid import normalize


def _text_matches_keywords(text: str, keywords: Iterable[str]) -> int:
    text_norm = normalize(text)
    count = 0
    for keyword in keywords:
        keyword_norm = normalize(keyword)
        if keyword_norm and keyword_norm in text_norm:
            count += 1
    return count


def score_event(event: dict, config: dict) -> float:
    weights = config.get("weights", {})
    text = " ".join(filter(None, [event.get("title"), event.get("notes"), event.get("category"), event.get("org"), event.get("url")]))

    score = 0.0

    goal_keywords = config.get("goal_keywords", {})
    for goal_key, keywords in goal_keywords.items():
        matches = _text_matches_keywords(text, keywords)
        weight_key = f"goals.{goal_key}"
        score += matches * weights.get(weight_key, 0.0)

    category_weights = config.get("category_weights", {})
    if category := event.get("category"):
        score += category_weights.get(category.lower(), 0.0)

    if city := event.get("city"):
        if normalize(city) != normalize(config.get("home_location", "Ann Arbor, MI")):
            score += weights.get("travel_time_penalty", 0.0)

    cost_text = event.get("cost", "")
    if cost_text:
        if "free" in cost_text.lower():
            score += config.get("cost_preferences", {}).get("free_bonus", 0.0)
        else:
            score += weights.get("cost_penalty", 0.0)

    if event.get("source") in config.get("novelty_sources", []):
        score += weights.get("novelty", 0.0)

    # Light penalty for late-evening events.
    if start_str := event.get("start_local"):
        try:
            hour = int(start_str.split("T")[1].split(":")[0])
        except Exception:
            hour = 0
        if hour >= 21:
            score += weights.get("evening_penalty", -0.05)

    return round(score, 4)


def attach_scores(events: list[dict], config: dict) -> list[dict]:
    for event in events:
        event["score"] = score_event(event, config)
    return events
