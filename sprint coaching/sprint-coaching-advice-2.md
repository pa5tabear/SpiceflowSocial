# Spiceflow Social — Sprint Coaching Memo

**Prepared by:** Codex (Product Manager & Sprint Coach)

**Audience:** Programming Lead, Spiceflow Social

**Date:** 2025-09-28

---

## 1. Context and Executive Signals

Spiceflow Social now runs a zero-OAuth scrape → score → choose → export loop that proves the concept. The next push is to ground the CLI workflow in the Apple Calendar layer (already syncing back to Google Calendar), ingest the existing preference blueprint, and tighten scoring so every suggestion is justified. We stay in pure local mode: no GitHub automation, no additional source feeds, just a disciplined Codex CLI calendar curator that emits clear artifacts.

### Fresh signals from Spiceflow Nesting (2025-09-28 pull)
- Async scrape orchestration with per-host throttles and conditional cache reuse (`SpiceflowNesting/src/run_all.py:1`, `SpiceflowNesting/src/util/http_cache.py:1`).
- Proposal lifecycle, anti-churn budgets, and accepted-plan ledger primitives (`SpiceflowNesting/src/plan/proposals.py:1`).
- Morning digest and enhanced run reports with per-source timings and cache hits (`SpiceflowNesting/src/emit/digest.py:1`, `SpiceflowNesting/src/emit/reports.py:1`).
- Dedupe registry enriched with `first_seen/last_seen` and per-source hashes (`SpiceflowNesting/src/util/dedupe.py:1`).

These patterns are the north star for Social’s near-term hardening.

### Headline takeaways
- Codebase is lean and modular; keep it that way while layering tests and guardrails.
- Portfolio selection just sorts by score (`src/plan/choose.py`), so we overbook afternoons and clone museum shows; availability and diversity logic are urgent.
- Preference/goal ingestion is still hypothetical; ship the `src/preferences.yaml` parser so story and software stay aligned.
- Cache + registry foundations exist, but we need monitoring and regression coverage before scaling source counts.
- The next sprints must add real context inputs (Apple Calendar availability, budgets, weather placeholders) and codify testable contracts for scoring/selection.

## 2. Strengths to Preserve and Amplify

1. **Modular pipeline staging.** `src/run_all.py` cleanly chains scrape → dedupe → score → choose → emit via focused modules; keep that separation intact.
2. **Lightweight caching discipline.** `util/http_cache.py` already respects ETag/Last-Modified headers, giving us a hook for observability without rewrites.
3. **Documentation depth.** Existing planning docs (e.g., sprint plans and agent responsibilities) keep stakeholders aligned; maintain the cadence while updating them whenever workflow realities change.
4. **Config-first philosophy.** `src/sources.yaml` and `src/scoring_config.json` let humans tune the system; reuse that pattern for upcoming constraints.
5. **Sister-repo accelerators.** Nesting’s new concurrency, proposal, and digest work offer blueprints we can port with minimal discovery.

## 3. Critical Gaps Blocking the Product Vision

### 3.1 Availability awareness is missing entirely
Without direct Apple Calendar access, the plan still recommends mid-day campus events and double-books evenings. Drop in a static availability fixture now, then wire the pipeline to Apple Calendar (already syncing from Google) so we read the real 6–10 PM windows.

### 3.2 Scoring is shallow and fragile
`src/plan/score.py` scans whole text blobs, so stray URL substrings boost scores while structured tags go unused. Config knobs like `budget_cap_per_week` and `pref_windows` never execute. Light up those rules and surface per-component score breakdowns so tuning becomes evidence-based.

### 3.3 Portfolio assembly ignores diversity and calendar semantics
`choose_portfolio` just sorts by score, which clumps planetarium shows and books the same window twice. We still need per-evening caps, category balance, outreach fallbacks, and weekly intensity limits to match the product story.

### 3.4 Preference ingestion remains hypothetical
`src/preferences.yaml` already sketches goals, weights, and guardrails, but nothing loads it. Parse that file and flow the values into scoring/selection so the pipeline reflects human intent.

### 3.5 No automated tests or smoke diagnostics
There is no `tests/` package, so every scraper tweak risks regressions. `src/run_all.py` also lacks structured status output. Stand up a small unit suite plus a smoke run artifact so local execution can catch breakages.

### 3.6 Observability, error handling, and resilience gaps
Scrapers currently fail quietly, writing empty JSONL files and moving on. JS sources throw `NotImplementedError`, yet the run keeps going. We need explicit status codes, retries, and per-source metrics, mirroring Nesting’s richer run report (`SpiceflowNesting/src/emit/reports.py:1`).

### 3.7 Data hygiene & lifecycle concerns
`util/dedupe.py` still writes to `src/registry.json`, so the ledger will balloon and tempt accidental commits while outputs overwrite in place. Move everything under `data/` and adopt Nesting’s `first_seen/last_seen` pruning metadata (`SpiceflowNesting/src/util/dedupe.py:1`).

### 3.8 No proposal lifecycle or anti-churn controls
Social still emits one-shot ICS exports with no memory of accepted plans or change budgets. Nesting tracks accepted events, enforces daily/weekly limits, and ships a morning digest (`SpiceflowNesting/src/plan/proposals.py:1`, `SpiceflowNesting/src/emit/digest.py:1`); Social needs equivalent plumbing to act like a coach.

## 4. MVP Brick Roadmap (Do These One at a Time)

1. Create `data/availability_stub.json` with a two-week sample of 6–10 PM free blocks.
2. Add `src/util/availability.py` to load the stub and expose evening slots.
3. Update `src/plan/choose.py` to skip events outside the loaded windows.
4. Write a unit test proving `choose_portfolio` returns ≤1 event per evening when availability is enforced.
5. Attach a `score_breakdown` dict in `src/plan/score.py` (goal matches, category weights, penalties) and include it in event payloads.
6. Cover `score_event` with unit tests that assert keyword hits, penalties, and rounding.
7. Relocate the dedupe registry to `data/registry/registry.json` and update `.gitignore` accordingly.
8. Extend `util/dedupe.dedupe_events` to prune entries older than 90 days and store `first_seen/last_seen` metadata.
9. Add a regression test ensuring duplicates update `last_seen` without duplicating entries.
10. Create `tests/test_parse_sources.py` covering YAML and Markdown parsing flows in `src/run_all.py`.
11. Introduce a minimal `pytest.ini` and document the local test command in `README.md`.
12. Emit `data/out/run_summary.json` from `src/run_all.py` capturing counts, cache hits, and errors.
13. Expand `emit/reports.write_run_report` to log cache-served sources using timing data.
14. Port Nesting’s async scrape harness into `src/run_all.py`, defaulting to concurrency=8 with per-host limits.
15. Wrap scrapers with simple retry + timeout logic (two retries, exponential backoff) so transient failures surface clearly.
16. Generate `data/out/availability_report.md` listing evenings with no qualified events.
17. Enforce `hard_rules['budget_cap_per_week']` in `choose_portfolio` using cumulative cost fields.
18. Add a `--availability` flag to `run_all.py` to switch between stub-based and Apple-derived availability.
19. Review `src/preferences.yaml` and confirm required fields plus ownership for ongoing edits.
20. Implement `src/util/preferences.py` to load that file into a normalized preferences object.
21. Add unit tests validating the preferences loader and ensuring missing fields raise actionable errors.
22. Feed parsed preferences into `score_event` and selection rules so scoring reflects human inputs.
23. Document the editing workflow in `docs/preferences.md` with field definitions and examples.
24. Add `scripts/validate_preferences.py` to lint the preferences file before each run.
25. Capture open assumptions and risks in a new `docs/risks.md` file maintained alongside the backlog.
26. Build an Apple Calendar bridge (e.g., read ICS exports from the local CalDAV cache) to replace the stub with live availability.
27. Once the bridge works, expand portfolio logic to honor preference-derived cadence rules (rest nights, quota checks) while writing an ICS ready for Apple Calendar import.

These bricks build the minimal viable assistant in a straight line. Start the next brick only after finishing and verifying the current one.

## 5. Medium-Horizon Targets (After the First 27 Bricks)

Once the brick list above is complete, queue these follow-on objectives:

- **Wellbeing/Weather coupling:** Define data contracts for weather and intensity scoring now to avoid rewrites later.
- **Feedback ingestion loop:** Map how acceptance/decline feedback feeds back into scoring adjustments and anti-churn budgets.
- **Automation & cadence controls:** Outline the nightly launcher script plus idempotent data writes, still local-first.
- **Privacy & secrets posture:** Document how Apple Calendar credentials and preference files are stored/rotated even in local mode.

## 6. Process Coaching Guidance

1. **Guard narrative-code alignment.** Each time the workflow plan shifts, schedule a parity check between docs, config files, and implemented behavior.
2. **Definition of Done.** Every new brick ships with a unit test (or smoke script) plus screenshots or file listings proving the artifact exists.
3. **Sprint review snapshot.** Capture run summary JSON, availability report, and key learnings at the end of each iteration; store them in `docs/run_logs/`.
4. **Code review focus.** Anchor reviews on tests, error handling, and config alignment; ask reviewers to trace new knobs to actual code before approving.
5. **Cross-repo sync.** Reserve 10 minutes every planning cycle to diff Social against Nesting so we adopt changes intentionally.

## 7. Decision Snapshot (Confirmed 2025-09-28)

1. **Apple Calendar bridge strategy.** Availability comes from Apple Calendar (which already syncs with Google). No direct Google OAuth needed for the MVP.
2. **Preference file logistics.** Use the existing `src/preferences.yaml`; the CLI must detect edits and reload gracefully.
3. **Event source prioritization.** Freeze the current Ann Arbor-heavy source list until diversity logic is in place.
4. **Testing infrastructure appetite.** Stay fully local—no GitHub Actions or remote CI until the workflow is proven in the CLI.
5. **Data retention policy.** Keep artifacts and registries indefinitely for now; revisit if disk pressure appears.

## 8. Next Steps

- Translate bricks 1–6 into individual issues/tasks and assign owners.
- Schedule a 30-minute working session to walk through bricks 1–5, confirm acceptance criteria, and demo the Apple Calendar bridge concept.
- Capture a short design note outlining how to read Apple Calendar ICS exports without elevated privileges.
- Begin drafting `docs/preferences.md` while the preferences loader is under construction.

With these moves, we can evolve the zero-API scaffold into a focused Apple Calendar curator that honors your written priorities, keeps artifacts auditable, and stays in sync with the workflow vision.

— Codex
