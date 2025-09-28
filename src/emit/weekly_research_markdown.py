"""Generate weekly LLM research summary markdown."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from util.timez import DEFAULT_TIMEZONE


def write_weekly_research_markdown(
    research_dir: Path,
    output_path: Path,
    title: str = "Weekly LLM Research Summary"
) -> None:
    """Generate a comprehensive markdown summary of LLM research results."""

    # Find all research files (use non-timestamped versions)
    research_files = []
    for file_path in research_dir.glob("*.json"):
        if "-2025-" not in file_path.name:  # Skip timestamped versions
            research_files.append(file_path)

    research_files.sort()

    lines = [
        f"# {title}",
        f"**Generated:** {datetime.now(DEFAULT_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"**Sources Analyzed:** {len(research_files)}",
        "",
        "## Executive Summary",
        ""
    ]

    # Load and categorize research results
    successful_research = []
    no_events_found = []
    context_failures = []

    for file_path in research_files:
        try:
            data = json.loads(file_path.read_text())
            slug = data.get("slug", file_path.stem)
            summary = data.get("summary", "No summary available")
            events = data.get("events", [])
            notes = data.get("notes", {})

            if events:
                successful_research.append((slug, summary, events, notes))
            elif "no page content available" in summary.lower():
                context_failures.append((slug, summary, notes))
            else:
                no_events_found.append((slug, summary, notes))

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Executive summary stats
    lines.extend([
        f"- **Events Discovered:** {sum(len(events) for _, _, events, _ in successful_research)}",
        f"- **Sources with Events:** {len(successful_research)}",
        f"- **Sources with No Current Events:** {len(no_events_found)}",
        f"- **Sources with Access Issues:** {len(context_failures)}",
        ""
    ])

    # Successful Research Section
    if successful_research:
        lines.extend([
            "## 🎯 Sources with Events Discovered",
            ""
        ])

        for slug, summary, events, notes in successful_research:
            lines.extend([
                f"### {slug.replace('_', ' ').title()}",
                f"**Events Found:** {len(events)}",
                "",
                f"**LLM Analysis:** {summary}",
                ""
            ])

            for event in events[:3]:  # Show first 3 events max
                title = event.get('title', 'Untitled')
                start = event.get('start_local', 'TBD')
                location = event.get('location', 'TBD')
                rationale = event.get('fit_rationale', event.get('notes', ''))

                lines.extend([
                    f"**{title}**",
                    f"- When: {start}",
                    f"- Where: {location}",
                    f"- Why it fits: {rationale}",
                    ""
                ])

            if len(events) > 3:
                lines.append(f"*...and {len(events) - 3} more events*")
                lines.append("")

    # No Events Section
    if no_events_found:
        lines.extend([
            "## 📋 Sources Analyzed (No Current Events)",
            ""
        ])

        for slug, summary, notes in no_events_found:
            lines.extend([
                f"### {slug.replace('_', ' ').title()}",
                f"**LLM Analysis:** {summary}",
                ""
            ])

    # Context Failures Section
    if context_failures:
        lines.extend([
            "## ⚠️ Sources with Access Issues",
            ""
        ])

        for slug, summary, notes in context_failures:
            lines.extend([
                f"### {slug.replace('_', ' ').title()}",
                f"**Issue:** {summary}",
                ""
            ])

    # Technical Details
    lines.extend([
        "## 🔧 Technical Details",
        "",
        f"- **LLM Provider:** Gemini 2.5 Pro",
        f"- **Research Mode:** Live website content analysis",
        f"- **Content Fetching:** {'✅ Working' if len(context_failures) < len(research_files) / 2 else '⚠️ Issues detected'}",
        f"- **Event Validation:** Anti-hallucination filters active",
        ""
    ])

    # Quality Assessment
    total_sources = len(research_files)
    working_sources = len(successful_research) + len(no_events_found)
    quality_score = (working_sources / total_sources * 100) if total_sources > 0 else 0

    lines.extend([
        "## 📊 Research Quality Assessment",
        "",
        f"- **Source Accessibility:** {quality_score:.1f}% ({working_sources}/{total_sources} sources accessible)",
        f"- **Event Discovery Rate:** {len(successful_research)}/{working_sources} sources with events",
        f"- **LLM Performance:** {'✅ Excellent' if quality_score > 80 else '⚠️ Needs attention' if quality_score > 60 else '❌ Critical issues'}",
        "",
        "---",
        "",
        f"*Generated by SpiceflowSocial LLM Research Pipeline - {datetime.now(DEFAULT_TIMEZONE).isoformat()}*"
    ])

    # Write the file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\\n".join(lines))

    print(f"Weekly research markdown written to: {output_path}")
    print(f"- {len(successful_research)} sources with events")
    print(f"- {len(no_events_found)} sources analyzed (no events)")
    print(f"- {len(context_failures)} sources with access issues")


if __name__ == "__main__":
    from pathlib import Path

    research_dir = Path("data/research")
    output_path = Path("data/out/weekly_llm_research.md")

    write_weekly_research_markdown(research_dir, output_path)