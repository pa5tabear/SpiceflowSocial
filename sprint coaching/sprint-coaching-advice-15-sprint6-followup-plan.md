# Sprint Coaching Advice #15 — Sprint 6 Follow‑Up: Perplexity 7‑Day to Weekly Calendar

Prepared by: Cursor (Programming Lead)
Audience: SpiceflowSocial‑Gemini branch programming team
Date: 2025‑09‑28

---

## Objectives (This Sprint)
- Increase event yield from Perplexity 7‑day sweeps so every day has ≥1 viable candidate.
- Produce reliable weekly artifacts end‑to‑end: `weekly_review.md` and `winners.ics` with at least one must‑see anchor.
- Make the seven‑day refresh a daily habit (single command, archived outputs, quick QA).

## Critical Path Tasks
1) Research Runs (Perplexity)
- Confirm wrapper works from repo root:
  ```bash
  PERPLEXITY_API_KEY=... SPICEFLOW_PERPLEXITY_MODEL=sonar \
  bash scripts/perplexity_seven_day.sh --sources src/sources.yaml --out data/research/perplexity_7day
  ```
- Ensure each `<slug>.json` includes: `summary`, `events[]`, and `notes.evidence` (snippets + citations).

2) Pipeline Ingestion
- Run:
  ```bash
  python src/run_all.py --use-perplexity --perplexity-dir data/research/perplexity_7day --horizon-days 7
  ```
- Verify outputs:
  - `data/out/weekly_review.md`
  - `data/out/winners.ics` and `data/out/winners-REMOVE.ics`
  - `data/out/portfolio.json`, `data/out/shortlist.md`

3) Source Coverage Expansion
- Add 10–15 sources with stable event detail pages; categorize by type (lecture, arts, performance, networking, wellbeing).
- Preference for sources with clear per‑event URLs and upcoming evening content.
- Re‑run 7‑day sweep; aim for ≥3 candidates total and ≥1 must‑see.

4) Evidence & QA Tightening
- For each accepted event, persist `notes.evidence` and verify the `url` opens the exact event page.
- Reject events with missing `url` or outside the 7‑day horizon.
- Run a smoke check:
  ```bash
  grep -r '"events": \[\]' data/research/perplexity_7day | wc -l
  ```

5) Automation & Docs
- Ensure `scripts/perplexity_seven_day.sh` archives outputs by date and prints a one‑line summary (#sources, #events).
- Update `docs/automation.md` with the 7‑day workflow and troubleshooting tips.

## Checkpoints
- Day 1: 7‑day sweep completes; weekly artifacts generated; a must‑see appears in `winners.ics`.
- Day 2: Source expansion merged; event yield increases; artifacts re‑generated.
- Day 3: Automation docs complete; daily run stable; QA checks green.

## Metrics
- Discovery: ≥3 total candidates per sweep; ≥1 must‑see.
- Verification: ~100% events have valid URLs.
- Calendaring: `winners.ics` imports without errors; weekly review complete.
- Ops: Daily run < 5 minutes; cost estimate <$1/day at current scale.

## Guardrails
- Small, focused PRs (adapter/flag/docs/sources). No refactors to scoring/ICS this sprint.
- Single command to produce weekly artifacts; avoid manual multi‑step sequences.
- Keep the Gemini path intact; Perplexity remains a pluggable research engine.

---

Execute quickly, validate artifacts, and iterate on sources. The goal is a dependable 7‑day plan delivered daily with minimal friction.

## Operational Workflow — Critical Path (Artifact‑First)

- Daily run (single flow)
  - Research (7‑day):
    ```bash
    PERPLEXITY_API_KEY=... SPICEFLOW_PERPLEXITY_MODEL=sonar \
    bash scripts/perplexity_seven_day.sh --sources src/sources.yaml --out data/research/perplexity_7day
    ```
  - Ingest + emit:
    ```bash
    python src/run_all.py --use-perplexity --perplexity-dir data/research/perplexity_7day --horizon-days 7
    ```
  - Must produce:
    - `data/out/weekly_review.md`
    - `data/out/winners.ics` and `data/out/winners-REMOVE.ics`
    - `data/out/portfolio.json`, `data/out/shortlist.md`
    - `data/research/perplexity_7day/*.json` (with `notes.evidence`)

- PR rules (artifact‑first)
  - One focused change per PR (adapter/flag/sources/docs).
  - Include paths to updated artifacts; no merge without `weekly_review.md` + `winners.ics` present.
  - No scoring/ICS refactors this sprint.

- Acceptance criteria (DoD)
  - ≥1 verified event in the 7‑day window; ≥3 total candidates per sweep.
  - 100% winners have valid event URLs.
  - `winners.ics` imports without errors; `weekly_review.md` shows a full week or clearly flags gaps.

- Scope guardrails (avoid side quests)
  - In‑scope: Perplexity adapter/flag, source additions, daily script, minimal docs.
  - Out‑of‑scope: scoring redesign, UI work, speculative prompts or integrations.

- Fast feedback loop
  - If a day is empty, first add/adjust sources; then rerun the two commands above.
  - Keep prompts lean; prefer source coverage over prompt complexity.

- Optional enforcement (recommended)
  - Add a post‑run check that fails CI/local run if `data/out/weekly_review.md` or `data/out/winners.ics` is missing, to enforce artifact discipline.
