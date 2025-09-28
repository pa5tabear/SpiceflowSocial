from pathlib import Path
import sys
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from emit.daily_markdown import write_daily_markdowns
from util.timez import DEFAULT_TIMEZONE


def test_write_daily_markdowns(tmp_path: Path) -> None:
    today = datetime.now(DEFAULT_TIMEZONE).date().isoformat()
    events = [
        {
            "title": "Test Event",
            "start_local": f"{today}T18:00",
            "end_local": f"{today}T19:30",
            "location": "Venue",
            "url": "https://example.com",
            "cost": "Free",
            "tags": ["career"],
            "fit_rationale": "Supports goals.",
            "novelty_score": 0.5,
            "travel_minutes": 10,
            "score": 0.9,
        }
    ]
    info = write_daily_markdowns(events, {}, horizon_days=1, output_dir=tmp_path)
    assert info[0]["primary"]["title"] == "Test Event"
    assert (tmp_path / f"{today}.md").exists()
