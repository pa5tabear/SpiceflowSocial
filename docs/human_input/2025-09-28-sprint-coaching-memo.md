# Spiceflow Social — Sprint Coaching Memo

**Prepared by:** Codex (Product Manager & Sprint Coach)

**Audience:** Programming Lead, Spiceflow Social

**Date:** 2025-09-28

---

## 1. Context and Executive Signals

Spiceflow Social now runs a zero-OAuth scrape → score → choose → export loop that proves the concept. The pipeline still lacks availability inputs, preference ingestion, and trustworthy scoring, so this memo targets the highest-risk gaps for the next iteration while keeping an obsessively MVP mindset—one small brick at a time.

### Fresh signals from Spiceflow Nesting (2025-09-28 pull)
- Async scrape orchestration with per-host throttles landed upstream (`SpiceflowNesting/src/run_all.py:1`), paired with conditional requests that raise `NotModifiedError` so we can reuse cached payloads when sources are unchanged (`SpiceflowNesting/src/util/http_cache.py:1`).
- The Nesting pipeline now yields swap-aware proposals, enforces anti-churn budgets, and persists an accepted-plan ledger (`SpiceflowNesting/src/plan/proposals.py:1`).
- Morning digests and richer run reports—including per-source timings and cache hits—ship as default artifacts (`SpiceflowNesting/src/emit/digest.py:1`, `SpiceflowNesting/src/emit/reports.py:1`).
- Dedupe entries track `first_seen`, `last_seen`, and per-source hashes, allowing safe rotation of the registry without losing provenance (`SpiceflowNesting/src/util/dedupe.py:1`).

These updates illustrate the productized direction we expect Social to emulate during the next planning cycle.

### Headline takeaways
- Codebase is lean and modular; keep it that way while layering tests and guardrails.
- Portfolio selection just sorts by score (`src/plan/choose.py`), so we overbook afternoons and clone museum shows; availability and diversity logic are urgent.
- Preference/goal ingestion is still hypothetical; ship the local file parser soon so story and software stay aligned.
- Cache + registry foundations exist, but we need monitoring and regression coverage before scaling source counts.
- The next sprints must add real context inputs (availability, budgets, weather placeholders) and codify testable contracts for scoring/selection.

## 2. Strengths to Preserve and Amplify

1. **Modular pipeline staging.** `src/run_all.py` cleanly chains scrape → dedupe → score → choose → emit via focused modules; keep that separation intact.
2. **Lightweight caching discipline.** `util/http_cache.py` already respects ETag/Last-Modified headers, giving us a hook for observability without rewrites.
3. **Documentation depth.** Existing planning docs (e.g., sprint plans and agent responsibilities) keep stakeholders aligned; maintain the cadence.
4. **Config-first philosophy.** `src/sources.yaml` and `src/scoring_config.json` let humans tune the system; reuse that pattern for upcoming constraints.
5. **Sister-repo accelerators.** Nesting’s new concurrency, proposal, and digest work offer blueprints we can port with minimal discovery.

## 3. Critical Gaps Blocking the Product Vision

### 3.1 Availability awareness is missing entirely
Without calendar data, the plan still recommends mid-day campus events and double-books evenings. Drop in a static availability fixture now, then wire it to Google Calendar as soon as auth plumbing exists.

### 3.2 Scoring is shallow and fragile
`src/plan/score.py` scans whole text blobs, so stray URL substrings boost scores while structured tags go unused. Config knobs like `budget_cap_per_week` and `pref_windows` never execute. Light up those rules and surface per-component score breakdowns so tuning becomes evidence-based.

### 3.3 Portfolio assembly ignores diversity and calendar semantics
`choose_portfolio` just sorts by score, which clumps planetarium shows and books the same window twice. We still need per-evening caps, category balance, outreach fallbacks, and weekly intensity limits to match the product story.

### 3.4 Preference ingestion remains hypothetical
We still lack a parser for the upcoming preferences/criteria/goals file, so scoring cannot anchor to human-authored priorities. Define the file schema now and wire it into the scoring config to keep the system honest.

### 3.5 No automated tests or smoke diagnostics
There is no `tests/` package, so every scraper tweak risks regressions. `run_all.py` also lacks structured status output. Stand up a small unit suite plus a smoke run artifact so CI can catch breakages.

### 3.6 Observability, error handling, and resilience gaps
Scrapers currently fail quietly, writing empty JSONL files and moving on. JS sources throw `NotImplementedError`, yet the run keeps going. We need explicit status codes, retries, and per-source metrics, mirroring Nesting’s richer run report (`SpiceflowNesting/src/emit/reports.py:1`).

### 3.7 Data hygiene & lifecycle concerns
`util/dedupe.py` still writes to `src/registry.json`, so the ledger will balloon and tempt accidental commits while outputs overwrite in place. Move everything under `data/` and adopt Nesting’s `first_seen/last_seen` pruning metadata (`SpiceflowNesting/src/util/dedupe.py:1`).

### 3.8 No proposal lifecycle or anti-churn controls
Social still emits one-shot ICS exports with no memory of accepted plans or change budgets. Nesting tracks accepted events, enforces daily/weekly limits, and ships a morning digest (`SpiceflowNesting/src/plan/proposals.py:1`, `SpiceflowNesting/src/emit/digest.py:1`); Social needs equivalent plumbing to act like a coach.

## 4. MVP Brick Roadmap (Do These One at a Time)

1. Create `data/availability_stub.json` with a two-week sample of 6–10 PM free blocks.
2. Add a loader in `src/util/timez.py` (or a new `src/util/availability.py`) that returns availability slots from the stub.
3. Update `src/plan/choose.py` to skip events outside the stubbed free windows.
4. Write a unit test for `choose_portfolio` that proves one event per evening when availability is enforced.
5. Surface a `score_breakdown` dict in `src/plan/score.py` (goal matches, category weight, penalties) and attach it to each event.
6. Cover `score_event` with unit tests that assert keyword hits, penalties, and rounding.
7. Move `src/registry.json` into `data/registry/registry.json` and update `.gitignore` to ignore the new folder.
8. Teach `util/dedupe.dedupe_events` to prune entries older than 90 days and persist `first_seen/last_seen` metadata.
9. Backfill a regression test ensuring duplicates update `last_seen` without duplicating entries.
10. Add `tests/test_parse_sources.py` covering YAML and Markdown parsing in `src/run_all.py`.
11. Introduce `pytest` config and document the local test command in `README.md`.
12. Emit a JSON summary file (`data/out/run_summary.json`) from `src/run_all.py` capturing counts, cache hits, and errors.
13. Extend `emit/reports.write_run_report` to log cache-served sources using the new timing data.
14. Import Nesting’s async scrape harness into `src/run_all.py`, defaulting to concurrency=8 with per-host limits.
15. Wrap scrapers with simple retry + timeout logic (two retries, exponential backoff).
16. Create `data/out/availability_report.md` that lists evenings lacking candidate events.
17. Enforce `hard_rules['budget_cap_per_week']` inside `choose_portfolio` using cumulative cost fields.
18. Add a `--availability` flag to `run_all.py` to switch between stubbed and future live sources.
19. Draft `data/preferences_stub.yaml` capturing goal weights, quiet hours, and budget tolerances.
20. Implement `src/util/preferences.py` to load the stub into a normalized preferences object.
21. Add unit tests that validate the preferences parser and ensure missing fields raise helpful errors.
22. Feed parsed preferences into `score_event` (merging weights and constraints) so scoring reflects human inputs.
23. Document the editing workflow in a new `docs/preferences.md` and include field definitions.
24. Add `scripts/validate_preferences.py` to lint the preferences file before each run.
25. Capture open assumptions and risks in a new `docs/risks.md` file maintained alongside the backlog.
26. Only after bricks 1–25 succeed, schedule the Google OAuth handshake and replace the availability stub with live data.
27. Only after brick 26, expand portfolio logic to incorporate preference-derived cadence rules (e.g., rest nights).

These bricks build the minimal viable assistant in a straight line. Start the next brick only after finishing and verifying the current one.

## 5. Medium-Horizon Targets (After the First 27 Bricks)

Once the brick list above is complete, queue these follow-on objectives:

- **Wellbeing/Weather coupling:** Define data contracts for weather and intensity scoring now to avoid rewrites later.
- **Feedback ingestion loop:** Map how Evening Recommendations and Recommendation Feedback feed back into scoring adjustments.
- **Automation & cadence controls:** Outline the nightly scheduler plus idempotent scripts and secret handling.
- **Privacy & secrets posture:** Draft `docs/security/data_handling.md` and lock `.env` conventions before tokens land.

## 6. Process Coaching Guidance

1. **Guard narrative-code alignment.** Each time we update docs or templates, schedule a quick “implementation parity” review. The current drift (e.g., budget caps declared but not enforced) must be a one-time anomaly.
2. **Adopt Definition of Done upgrades.** For each feature touching the pipeline, require a basic test and a run artifact demonstrating behavior. This can be as simple as attaching the new run report and confirming no regressions in `data/out/`.
3. **Introduce sprint review artifacts.** End every sprint with a concise update: run report snapshot, top three learnings, and a list of open risks. This keeps stakeholders engaged and gives the programming team a feedback loop.
4. **Code review focus.** Emphasize tests, error handling, and config alignment in code reviews. Encourage reviewers to cross-check new parameters against docs so we avoid silent misconfigurations.
5. **Cross-repo alignment.** Schedule a short retro item to diff Social against Nesting’s latest commits so we either adopt or intentionally defer shared abstractions.

## 7. Decisions & Inputs Needed from the Programming Lead

To keep momentum, I need clarity on the following:

1. **Google Calendar integration strategy.** Are we committing to on-device tokens (manual OAuth flow) or targeting a service account / server-side flow? This determines how we approach the post-brick Google rollout.
2. **Preference file logistics.** Where will the goals/preferences file live (path, format, update cadence), and how should the CLI detect changes?
3. **Event source prioritization.** Do we expand beyond Ann Arbor feeds before finishing availability logic, or do we freeze the source list until diversity logic is in place? My recommendation is to freeze (focus on quality), but need your call.
4. **Testing infrastructure appetite.** Are we introducing CI (GitHub Actions) this quarter, or is local pre-commit sufficient for now? We should align before writing automation scripts.
5. **Data retention policy.** How long should we retain run artifacts and dedupe registries? Please provide a guideline so we can encode retention into the tooling.

## 8. Next Steps

- Await your decisions on the five inputs above; these gate the next bricks.
- Once aligned, I will translate the brick list into individual issues with crisp acceptance criteria.
- Let’s schedule a 30-minute working session with the dev pod to walk through bricks 1–5 and confirm owners.
- During that session, flag which Nesting modules (scrape orchestration, proposals, digest) we will port and in what order so estimates stay tight.

With these moves, we can transform the promising zero-API pipeline into a context-aware planner that honors the holistic vision articulated in `README.md` and the sprint plans under `spiceflow_social/`.

— Codex
