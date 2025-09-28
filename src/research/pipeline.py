"""LLM research orchestration."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from .llm_agent import LLMResearchClient, ResearchResult


def gather_llm_research(
    sources: Iterable[Dict[str, Any]],
    *,
    horizon_days: int,
    output_dir: Path,
    overwrite: bool = False,
    client: LLMResearchClient | None = None,
) -> Tuple[List[Dict[str, Any]], List[ResearchResult]]:
    """Use an LLM to research each source and return candidate events.

    Each result is persisted to ``output_dir`` as ``<slug>.json`` for auditing.
    The function returns a tuple ``(events, results)`` where ``events`` is a
    flattened list of structured event dicts suitable for downstream scoring.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    client = client or LLMResearchClient()
    all_events: List[Dict[str, Any]] = []
    results: List[ResearchResult] = []

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")

    for source in sources:
        result = client.summarize_source(source, horizon_days=horizon_days)
        results.append(result)
        archive_path = output_dir / f"{result.slug}-{timestamp}.json"
        if overwrite:
            archive_path = output_dir / f"{result.slug}.json"
        payload = {
            "slug": result.slug,
            "summary": result.summary,
            "notes": result.notes,
            "events": result.events,
        }
        archive_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

        for event in result.events:
            event = dict(event)
            event.setdefault("source", result.slug)
            all_events.append(event)

    return all_events, results


__all__ = ["gather_llm_research"]
