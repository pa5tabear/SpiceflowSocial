"""Generate the weekly_review.md file."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from util.timez import DEFAULT_TIMEZONE

def write_weekly_review(
    selected_events: List[Dict[str, Any]],
    portfolio_data: Dict[str, Any],
    availability_summary: Dict[str, Any],
    output_path: Path,
    *,
    previous_selected: Optional[List[Dict[str, Any]]] = None
) -> None:
    """Generate the comprehensive weekly review markdown file."""
    lines = []
    today = datetime.now(DEFAULT_TIMEZONE).date()
    start_date = today.strftime("%b %d")
    end_date = (today + timedelta(days=6)).strftime("%b %d, %Y")

    # 1. Header Section
    lines.append(f"# Weekly Event Review - {start_date} to {end_date}")
    lines.append("")
    lines.append(f"**Status:** {len(selected_events)} events selected for the next 7 days")
    lines.append(f"**Last Updated:** {datetime.now(DEFAULT_TIMEZONE).strftime('%Y-%m-%d %H:%M %Z')}")
    lines.append("**ICS File:** `data/out/winners.ics` (Ready to import into your calendar)")
    lines.append("")

    # 2. Daily Breakdown Section
    lines.append("## 📅 Daily Breakdown")
    lines.append("")

    events_by_day = defaultdict(list)
    for event in selected_events:
        day_key = event["start_local"].split("T")[0]
        events_by_day[day_key].append(event)

    for i in range(7):
        day = today + timedelta(days=i)
        day_key = day.isoformat()
        day_events = events_by_day.get(day_key, [])

        lines.append(f"### {day.strftime('%A, %b %d')}")
        lines.append("")

        if not day_events:
            lines.append("**🔍 NEEDS REVIEW** No events currently selected.")
            lines.append("- **Suggestions:** This evening is open. Consider a spontaneous outing, a rest day, or use the commands below to find an alternative.")
            lines.append("- **Actions:** [ ] Find alternatives [ ] Keep open [ ] Add specific search")
        else:
            for event in day_events:
                # Simple check for now, can be enhanced with UID comparison
                status = "✅ APPROVED" # Default to approved, can be enhanced later
                start_time = datetime.fromisoformat(event["start_local"]).strftime("%I:%M %p")
                end_time = datetime.fromisoformat(event["end_local"]).strftime("%I:%M %p")

                lines.append(f"**{status}** {event.get('title', 'Untitled Event')}")
                lines.append(f"- **When:** {start_time} - {end_time}")
                lines.append(f"- **Where:** {event.get('location', 'TBD')}")
                lines.append(f"- **Why Selected:** {event.get('fit_rationale', 'N/A')}")
                lines.append(f"- **Score:** {event.get('score', 0.0):.2f}")
                lines.append(f"- **Notes:** {event.get('notes', 'N/A')}")
                lines.append("- **Actions:** [ ] Keep [ ] Modify [ ] Cancel")
                lines.append("")
        lines.append("")

    # 3. Weekly Goal Overview
    lines.append("## 🎯 Weekly Goal Overview")
    lines.append("")
    # This is a placeholder; real data would come from the portfolio summary
    lines.append("- **Career Learning:** 0/2 events (❌)")
    lines.append("- **Social Connection:** 0/2 events (❌)")
    lines.append("- **Outdoors/Wellbeing:** 0/1 events (❌)")
    lines.append("- **Weekly Budget:** $0 / $150 (✅)")
    lines.append("- **Travel Distribution:** 0 near, 0 local, 0 far")
    lines.append("")

    # 4. Quick Edit Commands
    lines.append("## 📝 Quick Edit Commands")
    lines.append("")
    lines.append("Use your AI assistant to edit this plan. Try commands like:")
    lines.append("")
    lines.append("- **\"Approve all suggested events for the week.\"**")
    lines.append("- **\"Cancel the event on Tuesday evening.\"**")
    lines.append("- **\"Remove '{Event Title}'.\"**")
    lines.append("- **\"Find a tech talk for Wednesday evening instead.\"**")
    lines.append("- **\"Is there any live music on Friday?\"**")
    lines.append("- **\"Keep Thursday evening free.\"**")
    lines.append("")

    # 5. Rolling Update Preview
    lines.append("## 🔄 Tomorrow's Update Preview")
    lines.append("")
    lines.append("When the plan updates tomorrow, the system will:")
    lines.append("")
    lines.append("- Preserve all **✅ APPROVED** events.")
    lines.append(f"- Add new suggestions for **{(today + timedelta(days=7)).strftime('%A')}**.")
    lines.append("- Re-evaluate any events still marked as **🔍 NEEDS REVIEW**.")
    lines.append("- Flag any newly discovered conflicts or cancellations.")
    lines.append("")

    output_path.write_text("\n".join(lines))