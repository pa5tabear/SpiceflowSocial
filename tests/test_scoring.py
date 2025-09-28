from plan.score import attach_scores, score_event


SCORING_CONFIG = {
    "weights": {
        "goals.career_learning": 0.3,
        "novelty": 0.1,
        "travel_time_penalty": -0.1,
    },
    "goal_keywords": {
        "career_learning": ["climate", "energy"],
    },
    "category_weights": {"lecture": 0.05},
    "cost_preferences": {"free_bonus": 0.05},
    "novelty_sources": ["source-a"],
}

PREFERENCES = {
    "weights": {
        "goals": {"career_learning": 0.4},
        "must_see_bonus": 0.2,
    },
    "categories": {
        "map": {"Lecture": ["career_learning"]},
        "must_see_keywords": ["keynote"],
    },
    "preferences": {
        "start_time": {
            "late_start_penalty_after": "20:00",
            "late_start_penalty": -0.04,
        }
    },
}


def test_score_event_combines_keywords_and_categories() -> None:
    event = {
        "title": "Climate keynote",
        "notes": "",
        "category": "Lecture",
        "url": "https://example.com",
        "start_local": "2025-10-01T19:00",
        "source": "source-a",
        "cost": "Free",
    }
    score = score_event(event, SCORING_CONFIG, PREFERENCES)
    assert score > 0.5


def test_attach_scores_mutates_events() -> None:
    events = [
        {
            "title": "Energy meetup",
            "category": "Lecture",
            "start_local": "2025-10-01T19:00",
        }
    ]
    attach_scores(events, SCORING_CONFIG, PREFERENCES)
    assert "score" in events[0]
