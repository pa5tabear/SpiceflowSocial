"""Helpers for writing LLM research summaries."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable


def write_research_summary(path: Path, results: Iterable[dict]) -> None:
    lines = ["# Research Summary", ""]
    had_entries = False
    for result in results:
        slug = result.get("slug") or "unknown"
        summary = result.get("summary") or "(no summary)"
        notes = result.get("notes") or {}
        lines.append(f"## {slug}")
        lines.append(summary)
        if notes:
            lines.append("")
            lines.append("**Notes**")
            if isinstance(notes, dict):
                for key, value in notes.items():
                    lines.append(f"- {key}: {value}")
            else:
                lines.append(f"- {notes}")
        lines.append("")
        had_entries = True
    if not had_entries:
        lines.append("No research results captured. Enable --use-llm-research to populate this report.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).strip() + "\n")


__all__ = ["write_research_summary"]
