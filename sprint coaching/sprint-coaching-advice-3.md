# Sprint Coaching Advice #3 — Gemini Research Hardening

**Prepared by:** Codex (Product Manager & Sprint Coach)  
**Date:** 2025-09-28

## 1. Situation Overview
- Gemini API calls succeed (see `data/research/*` with `{ "provider": "gemini" }`), but most `events` arrays are empty because Gemini receives only the source metadata—not the actual web content.
- The current prompt assumes the model can browse; in reality it cannot unless we enable `googleSearchRetrieval` or supply the page content ourselves.
- As long as we send “URL + basic info” without context, Gemini will either hallucinate or emit placeholders, which explains the dummy shortlist entries.

## 2. Root Causes
1. **No content in prompt** — `_build_prompt` passes only the URL, category, tags, horizon. Gemini has nothing concrete to summarize.
2. **Browsing not enabled** — our payload omits the `tools` stanza required for Gemini’s search. Without it the model is blind to the web.
3. **No post-processing fallback** — when Gemini returns empty events, we still treat the output as authoritative, leading to empty daily plans.

## 3. Strategy: Make Gemini Useful
1. **Fetch context before calling Gemini**  
   - Reuse our scrapers to retrieve each source’s HTML/ICS/JSON.  
   - Clean and truncate the content (e.g., first 5 KB) and embed it in the prompt under a `Content excerpt` block.
2. **(Optional) Enable Gemini retrieval**  
   - If your Google project has access, add `"tools": [{"googleSearchRetrieval": {}}]` and a matching `toolConfig`.  
   - This lets Gemini perform web lookups on its own. Requires API quota and may incur billing.
3. **Improve prompt & parsing**  
   - Remind the model to pull titles, ISO start/end times, and add rationale.  
   - Continue enforcing JSON structure; add guards for hallucinated fields.
4. **Fallback when events are missing**  
   - If Gemini still returns zero events after we supply context, log it and fall back to scraped data or flag the source for manual review.

## 4. Implementation Plan

### Brick A — Context Fetcher
- Add `research/context_fetcher.py` that loads each source’s HTML (reuse `util/http_cache.fetch`), strips scripts/styles, and truncates to e.g. 5 KB.
- Extend `_build_prompt` to include the snippet:
  ```text
  Content excerpt:
  """
  ... cleaned snippet ...
  """
  ```
- Add redaction rules (no personal data).

### Brick B — Payload Enhancements
- Allow `LLMResearchClient` to pass optional `tools` if env var `SPICEFLOW_GEMINI_ENABLE_SEARCH=1` is set.  
- Increase `max_output_tokens` (configurable) so longer event lists fit.  
- Log any HTTP errors with the full response for debugging.

### Brick C — Structured Validation
- Expand `_parse_response` to ensure each event has required fields (title, start, end). Drop invalid entries with warnings.  
- Require at least one of `url`, `location`; otherwise fallback to scraper output.

### Brick D — Fallback Logic
- Modify `gather_llm_research` so an empty `events` list triggers:
  - A warning in `research_summary.md` (`status: no-events`).
  - Optional re-run with the HTML snippet fallback or manual review queue.

### Brick E — Tests & Tooling
- Unit-test prompt builder to confirm snippet inclusion.  
- Add tests for `_parse_response` handling of valid/invalid JSON.  
- Run `scripts/test_gemini.py` after enabling content fetch to confirm real candidates appear.

## 5. Artifact Integration
- Update `data/out/research_summary.md` to surface `provider`, snippet status, and warnings for zero events.  
- Consider adding `data/out/research_log.md` listing which sources yielded real events vs. placeholders.
- Propagate enriched events into `data/out/shortlist.md` and daily plans so new insights actually affect scheduling.

## 6. Coordination Notes
- Ensure `icalendar` and any new dependencies are installed (`pip install -r requirements.txt`).  
- When testing Gemini, run from a network-enabled environment; the sandbox lacks outbound access.  
- Keep secrets in `data/secrets/secrets.md` and avoid committing them.  
- Update the sprint brick roadmap to include these Gemini-hardening tasks (Bricks ~28–33).

## 7. Next Actions
1. Add `context_fetcher.py` and integrate snippet injection into `_build_prompt`.
2. Decide whether to enable Gemini’s `googleSearchRetrieval`; obtain access if needed.  
3. Implement validation + fallback logic and add tests.  
4. Re-run `python src/run_all.py --use-llm-research --llm-overwrite` with the new context to confirm real events appear.  
5. Review `shortlist.md` and daily markdowns to ensure Gemini insights influence scheduling.  

Once these steps are complete, Gemini should shift from placeholder summaries to actionable event discovery feeding the calendar curator.
