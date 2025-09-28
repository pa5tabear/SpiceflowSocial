"""Minimal LLM research client scaffolding."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import httpx
from util.timez import DEFAULT_TIMEZONE
from preferences import load_preferences


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
    variable ``SPICEFLOW_LLM_PROVIDER=gemini`` together with
    ``GEMINI_API_KEY=...`` to activate live calls.
    """

    def __init__(self, *, provider: str | None = None, dry_run: bool | None = None) -> None:
        provider = provider or os.getenv("SPICEFLOW_LLM_PROVIDER", "dry")
        self.provider = provider
        self._client = None
        self._api_key: str | None = None
        self._gemini_model = os.getenv("SPICEFLOW_GEMINI_MODEL", "models/gemini-2.5-pro")

        if provider == "gemini":
            self._api_key = os.getenv("GEMINI_API_KEY") or self._load_gemini_key()
            self.dry_run = dry_run if dry_run is not None else not self._api_key
        elif provider == "dry":
            self.dry_run = True if dry_run is None else dry_run
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        if self.dry_run:
            self.provider = "dry"

    def summarize_source(self, source: Dict[str, Any], *, horizon_days: int, context: str = "") -> ResearchResult:
        slug = source.get("slug") or "unknown"
        prompt = self._build_prompt(source, horizon_days, context=context)
        if self.dry_run:
            summary = (
                "Dry-run LLM research placeholder. Configure LLM credentials to "
                "fetch live insights."
            )
            notes = {
                "prompt": prompt,
                "status": "dry-run",
            }
            return ResearchResult(slug=slug, summary=summary, events=[], notes=notes)

        if self.provider == "gemini":
            content = self._call_gemini(prompt)
            payload = self._parse_response(content)
            return ResearchResult(
                slug=slug,
                summary=payload.get("summary", ""),
                events=payload.get("events", []),
                notes={"provider": "gemini", "raw": content},
            )

        raise RuntimeError("Unsupported provider execution path")

    def _build_prompt(self, source: Dict[str, Any], horizon_days: int, *, context: str = "") -> str:
        horizon_limit = (datetime.now(DEFAULT_TIMEZONE).date() + timedelta(days=horizon_days)).isoformat()
        today = datetime.now(DEFAULT_TIMEZONE).date().isoformat()

        # Load real preferences for goal alignment
        try:
            preferences = load_preferences()
            goal_weights = preferences.get('weights', {}).get('goals', {})
        except Exception:
            goal_weights = {}

        lines = [
            "You are a research assistant for Spiceflow Social, finding REAL evening events in Ann Arbor, Michigan.",
            "",
            "CRITICAL RULES:",
            "- ONLY return events that actually exist on the source website",
            "- NEVER create fake, inferred, or plausible events",
            "- If no real events found, return empty events array",
            "- Use web search to find additional event details if needed",
            "- Events must have dates in 2025 (current year)",
            "",
            f"Search the provided source for ACTUAL upcoming events between {today} and {horizon_limit}.",
            "",
            "For each REAL event found, extract:",
            "- title: Exact event name from source",
            "- start_local: Actual start time in ISO format (America/Detroit timezone)",
            "- end_local: Actual end time or start + 90 minutes",
            "- location: Real venue address",
            "- url: Direct link to event page",
            "- cost: Actual price or 'Free' if stated",
            f"- category: {source.get('category', 'general')}",
            "- tags: Relevant keywords from content",
            "- fit_rationale: Why this aligns with goals (see goal priorities below)",
            "- novelty_score: 0.0-1.0 based on uniqueness",
            "- travel_minutes: Estimated from Ann Arbor",
            "- must_see: true only if exceptional/keynote speaker",
            "- notes: Key details from source",
            "",
            "GOAL ALIGNMENT PRIORITIES:",
            json.dumps(goal_weights, indent=2) if goal_weights else "No specific goal weights configured",
            "",
            f"Source to research: {source.get('url', 'unknown')}",
            f"Source name: {source.get('name', 'unknown')}",
            f"Expected category: {source.get('category', 'general')}",
        ]
        if context:
            lines.append("Content excerpt:")
            lines.append(context[:5000])
        else:
            lines.append("Content excerpt: (no page content available)")

        lines.extend([
            "",
            "Return JSON with summary and events array. Empty events array if no real events found.",
            "STRICT JSON only (no markdown, no prose)."
        ])
        return "\n".join(lines)

    def _parse_response(self, content: str) -> Dict[str, Any]:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            cleaned = content.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`\n")
                if cleaned.lower().startswith("json"):
                    cleaned = cleaned[4:].strip()
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                snippet = cleaned[start : end + 1]
                try:
                    payload = json.loads(snippet)
                except json.JSONDecodeError:
                    raise ValueError("LLM response was not valid JSON") from exc
            else:
                raise ValueError("LLM response was not valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("LLM response must be a JSON object")

        # Filter out fake/hallucinated events
        events = payload.get("events", [])
        validated_events = []
        for event in events:
            # Skip events with wrong year
            start_date = event.get("start_local", "")
            if start_date.startswith("2024") or start_date.startswith("2023"):
                continue
            # Skip events that mention inference/plausible
            notes = event.get("notes", "").lower()
            if any(word in notes for word in ["inferred", "plausible", "suggested", "example"]):
                continue
            validated_events.append(event)

        payload["events"] = validated_events
        payload.setdefault("notes", {})
        return payload

    def _load_gemini_key(self) -> str | None:
        secrets_path = Path(os.getenv("SPICEFLOW_SECRETS_PATH", "data/secrets/secrets.md"))
        if not secrets_path.exists():
            return None
        for line in secrets_path.read_text().splitlines():
            key, _, value = line.partition("=")
            if key.strip() == "gemini_api_key":
                return value.strip()
        return None

    def _call_gemini(self, prompt: str) -> str:
        if not self._api_key:
            raise RuntimeError("GEMINI_API_KEY not configured.")
        api_version = os.getenv("SPICEFLOW_GEMINI_API_VERSION", "v1beta")
        url = f"https://generativelanguage.googleapis.com/{api_version}/{self._gemini_model}:generateContent"
        max_tokens = int(os.getenv("SPICEFLOW_GEMINI_MAX_OUTPUT_TOKENS", "8192"))
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": max_tokens,
            },
        }
        # Note: Search grounding not supported in current API

        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, params={"key": self._api_key}, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Gemini API error: {exc.response.text}") from exc
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini response did not contain candidates")
        parts = candidates[0].get("content", {}).get("parts", [])
        texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
        if not texts:
            raise ValueError("Gemini response missing text content")
        return texts[0]


__all__ = ["LLMResearchClient", "ResearchResult"]
