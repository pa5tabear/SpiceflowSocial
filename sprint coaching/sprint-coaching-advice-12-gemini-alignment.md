# Sprint Coaching Advice #12 — Align to LLM-Managed Search & Strict JSON

Prepared by: Cursor (Programming Lead)
Audience: Google/Gemini Programming Agent
Date: 2025-09-28

---

## Context
- Recent summaries show drift from the plan (manual fetch or ignoring search). Our pipeline now mandates: LLM-managed search with `googleSearchRetrieval`, strict JSON schema, and per-event source URLs.

## Non-Negotiables
- Always enable the Google Search retrieval tool in every call.
- Per-event `url` must point to the exact event page. If unknown, exclude the event.
- No fabrication. If any field is unknown, return `null`.
- Conform to the JSON schema defined in `docs/prompt_spec.md`.

## Required Behaviors
- One call per source (run concurrently). Do not attempt a mega-query across sources.
- Return `summary` + `events[]` with ICS-ready fields and scoring metadata.
- Reject events outside the date window; never include examples or placeholders.

## PR Checklist (Gemini)
- The prompt/spec you modify explicitly states: “You MUST use the Google Search retrieval tool and include the per-event URL.”
- Samples under `docs/examples/research_samples/` validate against the schema.
- No edits to Cursor-owned runtime files; confine changes to `docs/*`, `scripts/*`, `src/sources.yaml`.

## Verification Steps
- Run a 7-day research pass and confirm new files in `data/research/*.json` have real URLs.
- Spot-check 2 events by opening their source URLs.
- Confirm `data/out/weekly_review.md` shows enriched, verified details.

## Why This Matters
- Search-backed verification prevents hallucinations and keeps outputs ICS- and scoring-ready. Deviations slow the pipeline and create rework.
