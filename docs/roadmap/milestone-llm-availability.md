# Near-Term Artifact Milestone

**Objective:** Produce a reviewer-friendly bundle that combines LLM research summaries with a shortlist of events mapped to evening availability windows by 2025-10-05.

## Deliverables

1. `data/research/<slug>-<timestamp>.json` — LLM-generated insights for each source, including structured event candidates.
2. `data/out/availability.md` — Markdown snapshot summarising free/busy slots (initially from a static fixture; later via Google Calendar sync).
3. `data/out/shortlist.md` — Ranked list of proposed events with rationale, linking back to research summaries and highlighting quota coverage.

## Acceptance Criteria

- Pipeline flag `--use-llm-research` fetches or records LLM results without falling back to legacy scrapers.
- Preference quotas/caps surface in the run report (`run_report.md`) so we can eyeball balance gaps quickly.
- Unit tests cover preference loading, scoring with must-see bonuses, and caps inside the portfolio selector (see `tests/`).
- Dry-run mode works without API keys; when credentials are provided the system should make a single provider call per source.

## Next Steps

- Implement availability fixture ingest and emit `availability.md`.
- Extend the shortlist emitter to merge research context with scored events.
- Schedule a working session to review the first artifact bundle and decide on production calendar automation.
