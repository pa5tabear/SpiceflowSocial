"""LLM research orchestration."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from dateutil import parser

from .context_fetcher import fetch_context_for_source
from .llm_agent import LLMResearchClient, ResearchResult
from util.uid import generate_uid
from util.timez import DEFAULT_TIMEZONE, ensure_timezone, parse_datetime

logger = logging.getLogger(__name__)


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
        # The new agent fetches context internally, so we just call it directly.
        result = client.summarize_source(source, horizon_days=horizon_days)
        sanitized_events: list[dict[str, Any]] = []
        for event in result.events:
            cleaned = _clean_event_dict(event, default_source=result.slug, horizon_days=horizon_days)
            if cleaned:
                sanitized_events.append(cleaned)

        # Log fallback when no events are found
        if not sanitized_events:
            logger.warning(
                "Source '%s' returned zero events. LLM provider: %s. "
                "Consider manual review or scraper fallback for URL: %s",
                result.slug,
                client.provider,
                source.get("url", "unknown")
            )

        pipeline_note = {"status": "ok" if sanitized_events else "no-events"}
        result.notes = {**(result.notes or {}), "pipeline": pipeline_note}
        result.events = sanitized_events
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

        for event in sanitized_events:
            all_events.append(event)

    return all_events, results


def _clean_event_dict(event: Dict[str, Any], *, default_source: str, horizon_days: int) -> Dict[str, Any] | None:
    data = dict(event)
    data.setdefault("source", default_source)

    title = (data.get("title") or "").strip()
    start_value = data.get("start_local") or data.get("start")
    if not title or not start_value:
        return None

    try:
        start_dt = parse_datetime(str(start_value))
    except Exception:
        return None

    today = datetime.now(DEFAULT_TIMEZONE).date()
    horizon_limit = today + timedelta(days=horizon_days)
    if start_dt.date() < today or start_dt.date() > horizon_limit:
        return None

    end_value = data.get("end_local") or data.get("end")
    if end_value:
        try:
            end_dt = parse_datetime(str(end_value))
        except Exception:
            end_dt = start_dt + timedelta(minutes=90)
    else:
        end_dt = start_dt + timedelta(minutes=90)

    data["start_local"] = ensure_timezone(start_dt, DEFAULT_TIMEZONE).isoformat(timespec="minutes")
    data["end_local"] = ensure_timezone(end_dt, DEFAULT_TIMEZONE).isoformat(timespec="minutes")

    location = data.get("location") or "TBD"
    data["location"] = location

    url = data.get("url") or ""
    data["url"] = url

    cost = data.get("cost") or "Unknown"
    data["cost"] = cost

    category = data.get("category") or "general"
    data["category"] = category

    tags = data.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    elif isinstance(tags, list):
        tags = [str(tag) for tag in tags if tag]
    else:
        tags = []
    data["tags"] = tags

    notes = data.get("notes") or data.get("fit_rationale") or ""
    data["notes"] = notes

    if "fit_rationale" not in data and notes:
        data["fit_rationale"] = notes

    try:
        novelty = float(data.get("novelty_score", 0.0))
    except Exception:
        novelty = 0.0
    data["novelty_score"] = max(0.0, min(novelty, 1.0))

    try:
        travel = float(data.get("travel_minutes", 0.0))
    except Exception:
        travel = 0.0
    data["travel_minutes"] = travel

    must_see = data.get("must_see")
    if isinstance(must_see, str):
        must_see = must_see.strip().lower() in {"true", "yes", "1", "must", "y"}
    data["must_see"] = bool(must_see)

    data.setdefault(
        "uid",
        generate_uid(
            title,
            data["start_local"],
            url or location,
        ),
    )

    return data


__all__ = ["gather_llm_research"]
