# Sprint Coaching Advice #4 — Post-Update Review

**Prepared by:** Codex (Product Manager & Sprint Coach)  
**Date:** 2025-09-28

## 1. What Changed
- Added `src/research/context_fetcher.py` to gather page content; Gemini now receives real snippets (pending prompt integration).
- Introduced `src/emit/daily_markdown.py` and `tests/test_daily_markdown.py` to generate daily planning notes (see `data/out/daily/`).
- Updated `src/run_all.py`, `src/research/llm_agent.py`, `src/research/pipeline.py`, and `tests/test_preferences.py` to wire in preferences and daily reports.
- `scripts/test_gemini.py` verifies key loading but still fails to reach the API inside sandbox (network blocked).
- Sprint coaching folder now includes advisories #2, #3, #4 plus the Obsidian integration plan.

## 2. Current Gaps
1. **Gemini still returns empty events** — context fetcher exists but prompt updating/fallback handling isn’t finished. `data/research/*.json` mostly contain summaries with no `events`.
2. **Availability ingest** — daily markdowns show “No primary event selected” because availability and selection logic still need real events.
3. **Secrets & dependencies** — `data/secrets/` is untracked; make sure `.gitignore` covers it. Ensure `icalendar` and other libs are installed so runs don’t fail (see earlier ModuleNotFoundError).
4. **CI / Testing** — new tests exist but we still rely on manual `pytest`; consider adding a local make target or pre-commit hook.

## 3. Recommended Next Moves
- **Integrate context into prompt**: modify `_build_prompt` to include the snippet from `context_fetcher`. Re-test Gemini locally with network access.
- **Fallback logic**: if Gemini returns zero events, log a warning and fall back to scraper or mark source for manual review.
- **Daily markdown improvements**: once events populate, ensure `daily_markdown.py` selects top options and references availability (`summarise_evenings`).
- **Vault sync**: run planned `export_preferences_to_md` and `export_sources_to_md` scripts once they exist so Obsidian stays aligned (future brick).
- **Automate smoke tests**: bundle `scripts/test_gemini.py` and `pytest` into a `make smoke` command for quick verification.

## 4. Immediate Action Checklist
1. Update `_build_prompt` and Gemini payload to use fetched content (and optionally enable retrieval tools).
2. Re-run `python src/run_all.py --use-llm-research --llm-overwrite --horizon-days 14` from a network-enabled machine; inspect `data/research/*` and `data/out/shortlist.md` for real events.
3. Adjust `daily_markdown.py` to surface actual recommendations once events exist.
4. Ensure `data/secrets/` is ignored and secrets remain local.
5. Run `pytest` to confirm tests pass after prompt changes.

Staying focused on these steps will move Gemini from “placeholder summaries” to actionable event discovery feeding the calendar curator and the daily markdown workflow.
