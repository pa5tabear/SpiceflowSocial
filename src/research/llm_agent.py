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

        # Load comprehensive preferences (fallback to defaults on error)
        try:
            pref_path = Path(os.getenv("SPICEFLOW_PREFERENCES_PATH", "src/preferences.yaml"))
            preferences = load_preferences(pref_path)
            goal_weights = preferences.get("weights", {}).get("goals", {})
            travel_bins = preferences.get("travel", {}).get("bins", [])
            time_windows = preferences.get("time_windows", {})
            budget_caps = preferences.get("budgets", {})
            quotas = preferences.get("quotas", {})
            categories = preferences.get("categories", {})
            must_see = categories.get("must_see_keywords", [])
        except Exception:
            goal_weights = {}
            travel_bins = []
            time_windows = {}
            budget_caps = {}
            quotas = {}
            must_see = []

        lines = [
            "You are an expert event curator for Spiceflow Social, analyzing REAL evening events in Ann Arbor, Michigan.",
            "Extract complete event details for Apple Calendar integration and sophisticated scoring analysis.",
            "",
            "CRITICAL RULES:",
            "- ONLY return events that actually exist on the source website",
            "- NEVER create fake, inferred, or plausible events",
            "- Events must have dates in 2025 (current year)",
            f"- Events must occur between {today} and {horizon_limit}",
            "- Focus on evening events (typically 17:00-22:00)",
            "",
            "FOR EACH REAL EVENT, EXTRACT COMPLETE DETAILS:",
            "",
            "== ICS CALENDAR FIELDS ==",
            "- title: Exact event name from source",
            "- description: Rich 2-3 sentence description for calendar",
            "- start_local: Precise start time (America/Detroit timezone, ISO format)",
            "- end_local: Precise end time or estimated duration if not stated",
            "- location: Full venue name and address (street, city, state, zip if available)",
            "- url: Direct link to event page or registration",
            "- organizer: Contact name/email/phone if mentioned",
            "- cost: Exact price with $ symbol or 'Free'",
            "- registration_required: true/false for advance registration needed",
            "- capacity_limited: true/false if limited seating/tickets mentioned",
            "- accessibility_notes: Any wheelchair/accommodation info mentioned",
            "",
            "== SCORING ANALYSIS FIELDS ==",
            "- intensity_level: 1-5 scale (1=passive viewing, 5=intensive workshop)",
            "- social_type: 'networking'|'passive'|'interactive'|'presentation'",
            "- learning_format: 'lecture'|'hands-on'|'discussion'|'performance'|'exhibition'",
            "- venue_tier: 'tier1'|'tier2'|'tier3'",
            "- speaker_quality: 'keynote'|'expert'|'local'|'student'|'unknown'",
            "- follow_up_potential: 1-5 scale",
            "- seasonal_fit: 'indoor'|'outdoor'|'weather_dependent'",
            "",
            "== PREFERENCE ALIGNMENT ==",
            "Travel Distance Analysis (from Ann Arbor, MI):",
            json.dumps(travel_bins, indent=2) if travel_bins else "Standard distance analysis",
            "- travel_minutes: Estimated travel time from downtown Ann Arbor",
            "- travel_category: 'near'|'local'|'far'|'too_far' based on minutes",
            "",
            f"Budget Analysis (weekly cap: ${budget_caps.get('weekly_spend_cap_usd', 150)}):",
            "- budget_category: 'free'|'low'|'medium'|'high' (low <$25, medium $25-75, high >$75)",
            "- exceeds_weekly_budget: true/false if over weekly cap",
            "",
            "Time Window Preferences:",
            json.dumps(time_windows, indent=2) if time_windows else "Evening preference analysis",
            "- time_preference_match: 0.0-1.0 score for optimal time alignment",
            "",
            "== DEEP GOAL ANALYSIS ==",
            f"Goal Weights: {json.dumps(goal_weights, indent=2) if goal_weights else 'Equal weighting'}",
            "",
            "CAREER LEARNING (keywords: ai, machine learning, sustainability, climate, energy, entrepreneurship):",
            "- career_keyword_matches: List specific matched keywords",
            "- career_alignment_score: 0.0-1.0",
            "- career_rationale: Why this advances career goals",
            "",
            "SOCIAL CONNECTION (keywords: networking, mixer, community, social, reception, meetup):",
            "- social_keyword_matches: List specific matched keywords",
            "- social_alignment_score: 0.0-1.0",
            "- social_rationale: What social opportunities exist",
            "",
            "WELLBEING FITNESS (keywords: wellbeing, mental health, fitness, yoga, run):",
            "- wellbeing_keyword_matches: List specific matched keywords",
            "- wellbeing_alignment_score: 0.0-1.0",
            "- wellbeing_rationale: Physical or mental health component",
            "",
            "OUTDOORS NATURE (keywords: outdoor, nature, farm, hike, garden):",
            "- outdoors_keyword_matches: List specific matched keywords",
            "- outdoors_alignment_score: 0.0-1.0",
            "- outdoors_rationale: Natural environment component",
            "",
            "== MUST-SEE DETECTION ==",
            f"Must-See Keywords: {must_see}",
            "- must_see: true only if contains must-see keywords or exceptional speaker/content",
            "- must_see_rationale: Why this is exceptional (e.g., keynote, rare opportunity)",
            "",
            "== CATEGORY QUOTAS ==",
            f"Weekly Quotas: {json.dumps(quotas.get('weekly', {}), indent=2) if quotas else 'Standard variety'}",
            "- quota_categories: List which quotas this event helps fulfill",
            "- novelty_score: 0.0-1.0 based on uniqueness",
            "",
            f"SOURCE INFORMATION:",
            f"- Source URL: {source.get('url', 'unknown')}",
            f"- Source Name: {source.get('name', 'unknown')}",
            f"- Expected Category: {source.get('category', 'general')}",
        ]

        if context:
            lines.extend([
                "",
                "WEBSITE CONTENT TO ANALYZE:",
                "=" * 50,
                context[:8000],
                "=" * 50,
            ])
        else:
            lines.append("WEBSITE CONTENT: (no page content available)")

        lines.extend([
            "",
            "RESPONSE FORMAT: Return JSON with 'summary' and 'events' array.",
            "Each event must include ALL fields specified above.",
            "Empty events array if no real events found in date range.",
            "STRICT JSON only (no markdown, no prose).",
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

        # Filter out fake/hallucinated or incomplete events
        events = payload.get("events", [])
        validated_events = []
        hallucination_keywords = [
            "inferred",
            "plausible",
            "suggested",
            "example",
            "realistic suggestion",
            "likely",
            "probable",
            "estimated event",
            "typical",
            "might",
            "could be",
            "potentially",
            "presumably",
            "hypothetical",
        ]
        for event in events:
            start_date = str(event.get("start_local", ""))
            if not start_date.startswith("2025"):
                continue
            # Aggregate text fields for hallucination scan
            text_fields = [
                str(event.get("notes", "")),
                str(event.get("description", "")),
                str(event.get("title", "")),
                str(event.get("career_rationale", "")),
                str(event.get("social_rationale", "")),
            ]
            all_text = " ".join(text_fields).lower()
            if any(keyword in all_text for keyword in hallucination_keywords):
                continue
            # Require essential ICS fields
            if not event.get("title") or not event.get("start_local") or not event.get("location"):
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
        # Enable Google Search tool for retrieval grounding (supported in Gemini API)
        payload["tools"] = [{"googleSearchRetrieval": {}}]

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
