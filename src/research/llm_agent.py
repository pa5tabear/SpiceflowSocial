"""Minimal LLM research client scaffolding."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

try:  # Optional dependency, only required when LLM access is enabled.
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore


@dataclass
class ResearchResult:
    slug: str
    summary: str
    events: List[Dict[str, Any]] = field(default_factory=list)
    notes: Dict[str, Any] = field(default_factory=dict)


class LLMResearchClient:
    """Wrap access to an internet-enabled LLM provider.

    By default the client runs in ``dry_run`` mode so the pipeline keeps working
    locally without network access or API credentials. Set the environment
    variable ``SPICEFLOW_LLM_PROVIDER=openai`` together with
    ``OPENAI_API_KEY=...`` (or a compatible key) to activate real calls.
    """

    def __init__(self, *, provider: str | None = None, dry_run: bool | None = None) -> None:
        provider = provider or os.getenv("SPICEFLOW_LLM_PROVIDER", "dry")
        api_key = os.getenv("OPENAI_API_KEY")
        self.provider = provider
        self.dry_run = dry_run if dry_run is not None else provider == "dry" or not api_key
        self._client = None

        if not self.dry_run:
            if provider != "openai":
                raise ValueError(f"Unsupported LLM provider: {provider}")
            if OpenAI is None:
                raise RuntimeError("openai package not installed. Install `openai>=1.0`." )
            self._client = OpenAI(api_key=api_key)

    def summarize_source(self, source: Dict[str, Any], *, horizon_days: int) -> ResearchResult:
        slug = source.get("slug") or "unknown"
        if self.dry_run:
            summary = (
                "Dry-run LLM research placeholder. Configure OPENAI_API_KEY to "
                "fetch live insights."
            )
            notes = {
                "prompt": self._build_prompt(source, horizon_days),
                "status": "dry-run",
            }
            return ResearchResult(slug=slug, summary=summary, events=[], notes=notes)

        assert self._client is not None  # noqa: S101
        prompt = self._build_prompt(source, horizon_days)
        response = self._client.responses.create(  # type: ignore[attr-defined]
            model=os.getenv("SPICEFLOW_LLM_MODEL", "gpt-4.1-mini"),
            input=prompt,
            temperature=0.2,
        )
        content = response.output_text  # type: ignore[attr-defined]
        payload = self._parse_response(content)
        return ResearchResult(slug=slug, summary=payload.get("summary", ""), events=payload.get("events", []), notes={"raw": content})

    def _build_prompt(self, source: Dict[str, Any], horizon_days: int) -> str:
        lines = [
            "You are the research copilot for Spiceflow Social.",
            "Study the event source below and return:",
            "1. A short summary of why the source matters.",
            "2. A JSON list of upcoming events (<= horizon days) with fields: title, start_local, end_local, location, description, url, tags, category, cost.",
            "3. Highlight whether the source is Ann Arbor-focused and note any travel requirements.",
            "If information is unavailable, leave the list empty but explain what additional investigation is required.",
            "Return **only** JSON in the shape {\"summary\": str, \"events\": [...], \"notes\": {...}}.",
            "Source details:",
            f"- name: {source.get('name', 'unknown')}",
            f"- url: {source.get('url', 'n/a')}",
            f"- category: {source.get('category', 'n/a')}",
            f"- venue: {source.get('venue', 'n/a')}",
            f"- tags: {source.get('tags', [])}",
            f"- horizon_days: {horizon_days}",
        ]
        return "\n".join(lines)

    def _parse_response(self, content: str) -> Dict[str, Any]:
        import json

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("LLM response was not valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("LLM response must be a JSON object")
        payload.setdefault("events", [])
        payload.setdefault("notes", {})
        return payload


__all__ = ["LLMResearchClient", "ResearchResult"]
