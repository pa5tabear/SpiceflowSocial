# Sprint Coaching Advice #14 — Consolidate Perplexity Integration & Weekly Outputs

Prepared by: Cursor (Programming Lead)
Audience: SpiceflowSocial‑Gemini branch programming team
Date: 2025‑09‑28

---

## Context & Progress
- Sprint 6 added Perplexity 7‑day research and documented results in:
  - `sprint summaries/sprint-summary-6.md`
  - `sprint summaries/sprint-6-plan.md`
- A verified anchor event (Wege Lecture) was returned with rich metadata. This is materially better than Gemini’s constrained tool‑calling in this environment.

## Critical Path (Next 3–5 days)
1) Ingestion Path (Perplexity → Pipeline)
- Implement/verify `--use-perplexity` flag in `src/research/pipeline.py` that loads JSON from `data/research/perplexity_7day/` and emits normalized events.
- Keep schema minimal: required `title`, `start_local`, `location`, strong preference for `url`; optional `end_local`, `description`, `cost`, `must_see`.

2) Weekly Artifacts End‑to‑End
- Run a 7‑day Perplexity sweep and feed into scoring/selection.
- Confirm generation of:
  - `data/out/portfolio.json`, `data/out/shortlist.md`
  - `data/out/weekly_review.md`
  - `data/out/winners.ics` and `data/out/winners-REMOVE.ics`

3) Source Coverage Expansion
- Add sources to ensure ≥1 plausible evening candidate per day; diversify (lectures, culture, networking, wellbeing).
- Prefer sources with stable detail pages (URL per event) to ease verification.

4) Evidence & QA
- Persist Perplexity answer/citations as `notes.evidence` alongside events.
- Add a smoke check that rejects events lacking a valid event URL or outside horizon.

5) Automation & Cost Guardrails
- Create `scripts/perplexity_seven_day.sh` (non‑interactive) with horizon=7, archival output, and a summary line.
- Log token estimates per run; target <$1/day at current source counts with lean prompts.

## Definition of Done
- Perplexity JSON under `data/research/perplexity_7day/` ingests via `--use-perplexity` and flows through scoring/selection.
- `winners.ics` imports cleanly; at least one must‑see anchor selected in the 7‑day window.
- `weekly_review.md` reflects the 7‑day slate with clear gaps/suggestions.
- Evidence snippets saved per event; smoke checks pass.

## Guardrails
- Small, artifact‑driven PRs (adapter/flag/docs). No scoring/ICS refactors.
- Exclude events without a verifiable `url`.
- Keep the Gemini manual‑fetch path intact; avoid cross‑branch coupling.

## Metrics to Track
- Discovery rate per 7‑day sweep (targets: ≥3 candidates, ≥1 must‑see).
- Verified URL ratio (goal: ~100%).
- ICS validity (imports without errors).
- Daily run success and approximate token cost.

## Today’s Checklist (90 minutes)
- Run 7‑day Perplexity sweep; commit JSON outputs and a brief `research_summary.md`.
- Generate `weekly_review.md` and `winners.ics`; import ICS to validate.
- Open a PR with artifacts (file paths + screenshots) and a 3‑line test note.
