## Sprint 5A — Parallel Plan (Cursor + Gemini)

**Date:** 2025-09-28  
**Mode:** Two-agent parallel execution (Cursor + Gemini)  
**Theme:** Production workflow, anti‑hallucination, scale without cross‑blocking

### Objectives
- **Zero hallucinations** with richer ICS fields and preference integration.  
- **Daily workflow**: single `winners.ics`, `weekly_review.md`, rolling updates.  
- **Scale inputs**: add 10–15 high‑yield sources and basic automation/health.

### Parallel Workstreams and Ownership

#### Workstream A — Research Engine Hardening
- **Cursor (owner, writes code):**
  - Enhance `src/research/llm_agent.py`: always enable search; inject full ICS + scoring fields; integrate preferences; strict `_parse_response` validation.  
  - Add `src/util/preferences.py` if needed to load `src/preferences.yaml` safely.  
  - Emit `data/out/run_summary.json` with counts/errors.
- **Gemini (owner, drafts spec & fixtures):**
  - Author `docs/prompt_spec.md` containing the exact event field schema (ICS, scoring, preference alignment, must‑see).  
  - Provide 2–3 sample JSON research responses matching the schema in `docs/examples/research_samples/*.json` for validation.
- **Interfaces (no blocking):** Cursor ships working prompt/validation with defaults; when Gemini’s `prompt_spec.md` lands, Cursor aligns without breaking changes.

#### Workstream B — Review Markdown + Rolling Updates
- **Cursor (owner, writes code):**
  - Create `src/emit/weekly_review.py` to generate `data/out/weekly_review.md` with daily breakdown, goal overview, and quick actions.  
  - Add CLI flags in `src/run_all.py`: `--rolling-update`, `--full-refresh`; implement portfolio archiving and minimal change detection.
- **Gemini (owner, content & UX polish):**
  - Draft copy blocks/checklists for the review markdown (approval language, edit prompts) in `docs/weekly_review_copy.md`.  
  - Suggest goal overview layout and approval workflow refinements.
- **Interfaces:** Cursor treats Gemini copy as optional; uses sane defaults until copy is merged.

#### Workstream C — Source Expansion & Throughput
- **Gemini (owner, research & config):**
  - Propose 15 new Ann Arbor sources with URLs, categories, and notes; open PR editing `src/sources.yaml`.  
  - For dynamic sites, add per‑source hints in YAML (e.g., selectors, keywords, timing).
- **Cursor (owner, tooling):**
  - Implement `src/emit/source_performance_report.py` to generate `data/out/source_performance_report.md` ranking sources by discovery success.  
  - Add YAML validation to guard malformed entries (fail fast with actionable errors).
- **Interfaces:** Gemini can add sources immediately; Cursor’s reporter consumes whatever exists without schema surprises.

#### Workstream D — Tests & Validation
- **Cursor (owner):**
  - Unit tests: preference loading, hallucination keyword filter, required field completeness.  
  - Smoke script to scan `data/research/*.json` for year/keyword violations.  
  - Ensure `pytest -q` stays green.
- **Gemini (assist):**
  - Provide adversarial research samples that try to slip “inferred/plausible/example” language.

#### Workstream E — Automation & Ops
- **Gemini (owner):**
  - Author `scripts/daily_research.sh` (non‑interactive): run pipeline, archive outputs by date, print summary.  
  - Document usage in `docs/automation.md`.
- **Cursor (owner):**
  - Ensure `src/run_all.py` prints concise run summary and writes `run_summary.json` for the script to consume.

### Deliverables by Agent
- **Cursor:**
  - `src/research/llm_agent.py` (enhanced prompt + validation, search enabled)  
  - `src/util/preferences.py` (or equivalent integration)  
  - `src/emit/weekly_review.py`  
  - CLI flags and portfolio archiving in `src/run_all.py`  
  - `src/emit/source_performance_report.py`  
  - `data/out/run_summary.json`  
  - Tests in `tests/` for validation and preferences
- **Gemini:**
  - `docs/prompt_spec.md`, `docs/weekly_review_copy.md`  
  - `docs/examples/research_samples/*.json`  
  - Updated `src/sources.yaml` (15 new sources with hints)  
  - `scripts/daily_research.sh` and `docs/automation.md`

### Coordination Rules (No Cross‑Blocking)
- File ownership to avoid merge conflicts:  
  - Cursor primarily changes `src/research/*`, `src/emit/*`, `src/run_all.py`, `tests/*`.  
  - Gemini primarily changes `docs/*`, `src/sources.yaml`, `scripts/*`, and adds sample JSON under `docs/examples/`.
- Backward‑compatible specs: Cursor ships working defaults; Gemini specs refine behavior without breaking existing runs.
- Daily PR cadence with small diffs; each PR must include a passing smoke check.

### Acceptance Criteria
- No hallucination keywords; all events in 2025; required ICS fields present.  
- `data/out/winners.ics` imports cleanly with rich details.  
- `data/out/weekly_review.md` shows 7‑day plan, goal overview, and action prompts.  
- Rolling update preserves approvals and appends day 8 suggestions.  
- ≥10 new sources merged; `source_performance_report.md` generated.

### Run/Verify
```bash
# Full refresh
python src/run_all.py --full-refresh --horizon-days 7

# Rolling update
python src/run_all.py --rolling-update --horizon-days 7

# Hallucination scan
grep -r "inferred\|plausible\|realistic suggestion" data/research/*.json || echo "OK"
grep -r "2024-\|2023-\|2026-" data/research/*.json && echo "BAD" || echo "OK"
```

### Risks & Mitigations
- Prompt length/cost → monitor and trim non‑essential prose.  
- Source schema drift → YAML validation + fail‑fast errors.  
- Change detection false positives → conservative flags; manual confirmation.

### Definition of Done
- All acceptance criteria met; three consecutive clean runs; artifacts pushed.  
- Cursor and Gemini PRs merged with zero red tests and smoke checks passing.


