# Sprint Coaching Advice #11 — Gemini Critical-Path Execution

Prepared by: Cursor (Programming Lead)
Audience: Google/Gemini Programming Agent
Date: 2025-09-28

---

## Mission
Deliver real, verifiable artifacts that unblock the end-to-end evening planning workflow. Avoid side quests. Every task must ship a file or code edit that improves the daily 7-day plan.

## What “Critical Path” Means Here
- Real event discovery → structured JSON → portfolio → weekly_review.md → winners.ics
- Each step should produce a tangible artifact that the runner consumes on the next run.

## Non-Negotiable Rules
1. Real events only. If you can’t verify on the source website, return none.
2. Use the web search tool every time; include the exact event URL for each entry.
3. Follow the prompt spec in `docs/prompt_spec.md` strictly; if unknown, return null.
4. Keep PRs small and artifact-driven. One PR = one clear improvement.
5. Never block Cursor’s work. Prefer additive docs/config/samples over refactors.

## This Sprint’s Deliverables (Gemini-Owned)
1. docs/prompt_spec.md — Keep it current with fields needed for ICS + scoring.
2. docs/examples/research_samples/*.json — 3 verified samples matching the schema.
3. src/sources.yaml — Add 10–15 Ann Arbor sources (with categories and hints).
4. scripts/daily_research.sh — Non-interactive daily run; archive outputs; print status.
5. docs/automation.md — One-page usage + troubleshooting for daily runs.

## Definition of Done per PR
- Ships an artifact that the runner immediately uses (schema, samples, sources, script).
- Does not break existing runs; dry-run remains safe.
- Includes a 3-line test note (how you verified locally) in the PR description.

## Anti-Patterns (Avoid)
- Broad refactors that touch Cursor-owned files (`src/research/*`, `src/emit/*`, `src/run_all.py`).
- Adding speculative fields not consumed by scoring/ICS.
- Long memos without code or data artifacts.

## Daily Checklist (≤20 minutes)
1. Pull main and diff yesterday’s changes.
2. Add/update 2–3 sources in `src/sources.yaml`; run a local dry scan.
3. Update or add one sample JSON under `docs/examples/research_samples/`.
4. If prompt spec changed, align `docs/prompt_spec.md` and note deltas.
5. Open a small PR with before/after notes and quick verification steps.

## Success Metrics
- New, verified sources merged per day.
- Research samples conform to schema and import cleanly into the pipeline.
- `weekly_review.md` gains richer, verified content after your changes.

## When in Doubt
Ask: “What file will my change produce that improves tomorrow’s 7-day plan?” If no clear artifact, it’s a side quest—skip it.


