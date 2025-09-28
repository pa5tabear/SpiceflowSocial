from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

icalendar = pytest.importorskip('icalendar')

from availability import load_calendar_events, summarise_evenings

ICS_SAMPLE = """BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART:20250929T223000Z\nDTEND:20250929T233000Z\nSUMMARY:Late Meeting\nEND:VEVENT\nEND:VCALENDAR"""


def test_load_calendar_events(tmp_path: Path) -> None:
    ics_path = tmp_path / "fixture.ics"
    ics_path.write_text(ICS_SAMPLE)
    events = load_calendar_events(ics_path)
    assert len(events) == 1


def test_summarise_evenings_flags_busy_slot(tmp_path: Path) -> None:
    ics_path = tmp_path / "fixture.ics"
    ics_path.write_text(ICS_SAMPLE)
    events = load_calendar_events(ics_path)
    prefs = {
        "time_windows": {
            "evenings": {"weekdays": ["17:30", "23:30"]}
        }
    }
    summary = summarise_evenings(events, preferences=prefs, horizon_days=1)
    assert any(payload["status"] == "busy" for payload in summary.values())
