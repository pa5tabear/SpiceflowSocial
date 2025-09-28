## Sprint #4 — Final Plan (Production Workflow, Anti‑Hallucination, Scale)

**Date:** 2025-09-28  
**Owner:** Codex (Programming Lead)  
**Sources:** Coaching #7 (Production Optimization), #8 (Prompt Enhancement), #9 (ICS Workflow), Sprint Coaching Memo

### Objectives
- Eliminate LLM hallucinations end‑to‑end and enrich event details for ICS.  
- Ship a smooth daily planning workflow: one importable ICS, rich review markdown, rolling updates.  
- Begin scale: expand sources, automate daily runs, add light monitoring.

### Scope (What we will deliver this sprint)
1) Anti‑Hallucination + Prompt Upgrade in `src/research/llm_agent.py`
- Replace prompt with “real events only” spec and full ICS + scoring fields.  
- Always enable search tools for Gemini.  
- Load real preferences (`src/preferences.yaml`) and reflect weights/quotas/time windows in prompt.  
- Strengthen `_parse_response` validation to drop any fake/old/ambiguous events.

2) Daily Workflow & Review Artifacts
- Use `data/out/winners.ics` as the single import file.  
- Generate reviewer‑friendly markdown summarizing selected events and weekly goal progress.  
- Prepare rolling update mode to preserve approved events and append the new day.

3) Scale & Automation (Starter Set)
- Add 10–15 Ann Arbor sources to `src/sources.yaml`; tag/categorize for better analysis.  
- Add simple daily script and minimal run summary for health checks.

### Deliverables
- Updated `src/research/llm_agent.py` with enhanced prompt, preference loading, and stricter validation.  
- `data/out/winners.ics` (selected events only) and `data/out/weekly_review.md` (LLM‑friendly review).  
- Optional: `data/out/run_summary.json` (counts, cache hits, basic timings).  
- `src/emit/weekly_research_markdown.py` retained for research reporting.

### Implementation Details
1) Prompt + Validation (Critical)
- Prompt additions: title, description, start/end, location, organizer, url, cost, registration_required, capacity_limited, accessibility_notes.  
- Scoring fields: intensity_level, social_type, learning_format, venue_tier, speaker_quality, follow_up_potential, seasonal_fit.  
- Preference integration: travel minutes/bin, budget category + weekly cap check, time window match, quota categories, must‑see keywords.  
- Validation: reject events with wrong year, missing required fields, or hallucination keywords (e.g., “inferred”, “plausible”, “example”, “realistic suggestion”).

2) Review Markdown
- Generate `data/out/weekly_review.md` with:  
  - Daily breakdown (approved/needs review), when/where/why, score summary.  
  - Weekly overview (goal quotas, budget, travel).  
  - Quick edit actions the LLM can apply.  
- Keep `data/out/winners.ics` as the single source of truth for import.

3) Rolling Updates (Lightweight this sprint)
- Add CLI flags in `src/run_all.py`: `--rolling-update` and `--full-refresh`.  
- When rolling: load previous portfolio to preserve approvals, add a new day, and summarize changes.  
- Archive previous portfolios to enable comparisons.

4) Source Expansion & Automation (Starter)
- Add 10–15 sources across libraries, venues, museums, community centers, networking groups.  
- Script: `scripts/daily_research.sh` runs pipeline, archives artifacts, and prints a short status.

### Acceptance Criteria
- Zero hallucinations across consecutive runs; no events outside 2025; no “inferred/plausible/example” language.  
- `winners.ics` imports cleanly; events contain rich details (venue/address/desc).  
- `weekly_review.md` lists 7‑day plan with goal overview and action prompts.  
- Rolling update preserves previously approved events and appends day 8 suggestions.  
- At least 10 new sources added; run summary shows counts and no fatal errors.

### Test/Run Commands
```bash
# Research with Gemini (live)
SPICEFLOW_LLM_PROVIDER=gemini python src/run_all.py --use-llm-research --horizon-days 7

# Hallucination scan
grep -r "inferred\|plausible\|realistic suggestion" data/research/*.json || echo "OK: no hallucination keywords"
grep -r "2024-\|2023-\|2026-" data/research/*.json && echo "BAD: wrong year present" || echo "OK: 2025 only"

# Rolling vs full
python src/run_all.py --full-refresh --horizon-days 7
python src/run_all.py --rolling-update --horizon-days 7

# Check outputs
ls -la data/out/winners.ics data/out/weekly_review.md
```

### Out of Scope (Defer)
- Advanced weather coupling and travel‑time routing.  
- Complex monitoring dashboards; keep to a minimal JSON summary this sprint.  
- Preference learning loop; collect approvals first.

### Risks & Mitigations
- Prompt length vs. cost: start verbose; trim if latency/cost spike.  
- Change detection false positives: conservative rules; require manual review for edge cases.  
- Source variability: add retries/backoff and capture failures in run summary.

### Definition of Done
- All acceptance criteria met; three clean runs in a row.  
- `winners.ics` and `weekly_review.md` reviewed and imported successfully.  
- Push all changes to `main` with test evidence captured in `data/out/`.


