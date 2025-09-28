from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from util.dedupe import dedupe_events


def test_dedupe_collapses_same_day_variants(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    events = [
        {
            "title": "Laser Queen",
            "start_local": "2025-10-03T18:00",
            "location": "Planetarium",
            "uid": "laser-queen-1",
        },
        {
            "title": "Laser Queen",
            "start_local": "2025-10-03T19:00",
            "location": "Planetarium",
            "uid": "laser-queen-2",
        },
    ]
    unique, duplicates = dedupe_events(events, registry)
    assert len(unique) == 1
    assert len(duplicates) == 1
