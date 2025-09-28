"""Write a simple source performance report Markdown."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable


def write_source_performance_report(
    counts_by_slug: Dict[str, int], skipped_slugs: Iterable[str], output_path: Path
) -> None:
    lines = ["# Source Performance Report", ""]
    if counts_by_slug:
        lines.append("## Event Discovery Counts")
        for slug, count in sorted(counts_by_slug.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- **{slug}**: {count} events")
        lines.append("")
    if skipped_slugs:
        lines.append("## Skipped/Empty Sources")
        for slug in sorted(set(skipped_slugs)):
            lines.append(f"- {slug}")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


