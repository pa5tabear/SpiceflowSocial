from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from preferences import (
    category_goals_map,
    expand_goal_weights,
    load_preferences,
    must_see_keywords,
)


def test_load_preferences(tmp_path: Path) -> None:
    sample = """
meta:
  home_city: Ann Arbor
weights:
  goals:
    career: 0.3
categories:
  map:
    Lecture: [career]
    Arts: [social]
"""
    path = tmp_path / "preferences.yaml"
    path.write_text(sample)
    data = load_preferences(path)
    assert data["meta"]["home_city"] == "Ann Arbor"


def test_expand_goal_weights_merges_preferences() -> None:
    config = {"weights": {"goals.career": 0.1, "novelty": 0.05}}
    preferences = {"weights": {"goals": {"career": 0.3}, "novelty": 0.02}}
    merged = expand_goal_weights(config, preferences)
    assert merged["goals.career"] == 0.3
    assert merged["novelty"] == 0.02


def test_category_map_lowercases_keys() -> None:
    mapping = category_goals_map({"categories": {"map": {"Lecture": ["career"]}}})
    assert mapping["lecture"] == ["career"]


def test_must_see_keywords_returns_list() -> None:
    keywords = must_see_keywords({"categories": {"must_see_keywords": ["keynote"]}})
    assert "keynote" in keywords
