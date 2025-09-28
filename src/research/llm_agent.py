"Minimal LLM research client scaffolding."
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
    """Wrap access to an internet-enabled LLM provider (LLM-managed search)."""

    def __init__(self, *, provider: str | None = None, dry_run: bool | None = None) -> None:
        provider = provider or os.getenv("SPICEFLOW_LLM_PROVIDER", "dry")
        self.provider = provider
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

    def summarize_source(self, source: Dict[str, Any], *, horizon_days: int) -> ResearchResult:
        slug = source.get("slug") or "unknown"
        # Build a prompt that instructs the LLM to use its search tool to analyze the source URL
        prompt = self._build_prompt(source, horizon_days, context="")

        if self.dry_run:
            summary = "Dry-run LLM research placeholder."
            notes = {"prompt": prompt, "status": "dry-run"}
            return ResearchResult(slug=slug, summary=summary, events=[], notes=notes)

        if self.provider == "gemini":
            # Let the LLM use googleSearchRetrieval to fetch and verify details
            content = self._call_gemini(prompt)
            payload = self._parse_response(content)
            return ResearchResult(
                slug=slug,
                summary=payload.get("summary", ""),
                events=payload.get("events", []),
                notes={"provider": "gemini", "raw": content},
            )

        raise RuntimeError("Unsupported provider execution path")

    def _build_prompt(self, source: Dict[str, Any], horizon_days: int, *, context: str) -> str:
        horizon_limit = (datetime.now(DEFAULT_TIMEZONE).date() + timedelta(days=horizon_days)).isoformat()
        today = datetime.now(DEFAULT_TIMEZONE).date().isoformat()

        source_url = source.get("url", "unknown")
        source_name = source.get("name", "unknown")

        lines = [
            "You are an expert events research assistant for Spiceflow Social.",
            "Use your Google Search retrieval tool to verify details and extract ONLY real events.",
            "",
            "CRITICAL RULES:",
            f"- Events must occur between {today} and {horizon_limit}.",
            "- You MUST verify each event from the source website and include its direct event URL in 'url'.",
            "- NEVER invent, infer, or guess details. If unknown, return null.",
            "- If no real events are found, return an empty 'events' array.",
            "",
            f"SOURCE TO RESEARCH: {source_url}",
            f"SOURCE NAME: {source_name}",
            "",
            "For each verified event, extract fields for ICS and scoring:",
            "- title, description, start_local, end_local, location, url, organizer, cost,",
            "  registration_required, capacity_limited, accessibility_notes,",
            "  intensity_level, social_type, learning_format, venue_tier, speaker_quality,",
            "  follow_up_potential, seasonal_fit, travel_minutes,",
            "  budget_category, exceeds_weekly_budget, time_preference_match,",
            "  category, tags, must_see, must_see_rationale, novelty_score",
            "",
            "RESPONSE FORMAT:",
            "- STRICT JSON with keys: summary, events (array of objects)",
            "- If a field is unknown, use null.",
        ]
        return "\n".join(lines)

    def _parse_response(self, content: str) -> Dict[str, Any]:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            cleaned = content.strip().strip("```json").strip("`\n")
            try:
                payload = json.loads(cleaned)
            except json.JSONDecodeError as exc:
                raise ValueError(f"LLM response was not valid JSON despite cleaning: {content[:200]}...") from exc

        if not isinstance(payload, dict):
            raise ValueError("LLM response must be a JSON object")

        events = payload.get("events", [])
        validated_events = []
        for event in events:
            if not event.get("title") or not event.get("start_local"):
                continue
            validated_events.append(event)

        payload["events"] = validated_events
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

        response_schema = {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": ["string", "null"]},
                            "start_local": {"type": "string"},
                            "end_local": {"type": ["string", "null"]},
                            "location": {"type": "string"},
                            "url": {"type": ["string", "null"]},
                            "organizer": {"type": ["string", "null"]},
                            "cost": {"type": ["string", "null"]},
                            "registration_required": {"type": ["boolean", "null"]},
                            "capacity_limited": {"type": ["boolean", "null"]},
                            "accessibility_notes": {"type": ["string", "null"]}
                        },
                        "required": ["title", "start_local", "location"]
                    }
                }
            },
            "required": ["summary", "events"]
        }

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": max_tokens,
                "responseMimeType": "application/json",
                "responseSchema": response_schema,
            },
            "tools": [{"googleSearchRetrieval": {}}],
            "systemInstruction": {
                "role": "system",
                "parts": [{
                    "text": (
                        "You are an events research assistant. You MUST use Google Search retrieval to verify each event and include the event page URL. "
                        "Return STRICT JSON per schema. Never fabricate or infer unknown fields; use null instead."
                    )
                }],
            },
        }

        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, params={"key": self._api_key}, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Gemini API error: {exc.response.text}") from exc

        candidates = response.json().get("candidates", [])
        if not candidates:
            return '{"summary": "No candidates returned from LLM.", "events": []}'
        
        text_part = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if not text_part:
            return '{"summary": "No valid text content returned from LLM.", "events": []}'
        return text_part


__all__ = ["LLMResearchClient", "ResearchResult"]