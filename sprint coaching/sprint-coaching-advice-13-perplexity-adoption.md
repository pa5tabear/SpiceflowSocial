# Sprint Coaching Advice #13 — Adopt Perplexity for 7-Day Research

Prepared by: Cursor (Programming Lead)
Audience: SpiceflowSocial-Gemini branch programming team
Date: 2025-09-28

---

## Context
- Gemini tool-calling is constrained; manual fetch works but is fetch-limited (403/404) and sparse over a 1-day horizon.
- Perplexity run (sonar) returned a verified 7-day event (Wege Lecture) with rich metadata. This aligns with weekly planning needs.

## Decision
Shift the Gemini branch’s research stage to Perplexity for the next sprint while retaining the existing scoring/ICS/reporting layers unchanged.

## Critical Path (Do These Now)
1) Research Adapter
- Create `scripts/perplexity_one_day.py` CLI:
  - Args: `--sources`, `--horizon-days`, `--output-dir`
  - Env: `PERPLEXITY_API_KEY`, `SPICEFLOW_PERPLEXITY_MODEL=sonar`
  - For each source, query Perplexity, write JSON `{summary, events[]}` to output dir `<slug>.json`.
- Add `scripts/perplexity_seven_day.sh` wrapper (non-interactive) for daily runs.

2) Schema Compatibility
- Ensure Perplexity JSON matches `_clean_event_dict` expectations:
  - Required: `title`, `start_local`, `location`, `url` (preferably); `end_local` optional.
  - Include `description`, `cost`, `must_see`, `travel_minutes` when known.
- Keep fields minimal and reliable; enrich later.

3) Pipeline Ingestion
- Add a code path in `src/research/pipeline.py` to read Perplexity outputs from `data/research/perplexity_7day/` when `--use-perplexity` is present.
- Merge Perplexity events into the usual flow: dedupe → score → choose → emit.

4) Horizon & Coverage
- Default horizon to 7 days for Perplexity runs.
- Expand `src/sources.yaml` to cover diverse local venues so each day has ≥1 candidate.

5) Evidence & Reporting
- Store Perplexity evidence (answer text + citations) as `notes.evidence` in each `<slug>.json` for auditability.
- Generate `data/out/research_summary.md` and `data/out/weekly_review.md` as usual.

## Definition of Done
- `data/research/perplexity_7day/*.json` contains verified events for multiple sources within 7 days.
- Running scoring + ICS produces `data/out/winners.ics` with at least one must-see anchor.
- `weekly_review.md` shows a complete 7-day slate or clear gaps with suggestions.

## Guardrails
- Small PRs only (adapter, flag, docs). No refactors of scoring/ICS.
- If Perplexity returns no URL for an event, exclude it from winners.
- Keep Gemini code path intact (do not delete); the branch may dual-track.

## Next 48 Hours Plan
- Day 1: Implement adapter + `--use-perplexity` flag, run a 7-day sweep, commit outputs.
- Day 2: Expand sources, tune prompts, validate ICS and review markdown, and document daily run steps.

## Success Metrics
- ≥1 verified event per 7-day window; ≥3 total candidates discovered.
- Clean `winners.ics` import; weekly review reflects Perplexity results.
- Evidence snippets saved per event.

---

Focus on artifacts: Perplexity JSON → portfolio → weekly_review → winners.ics. Keep cycle time short and PRs atomic.
