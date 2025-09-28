# Sprint Plan One — Technical Roadmap

This document expands the Sprint Plan Number One outline into technical milestones, acceptance criteria, and dependencies for each of the ten sprints.

## Sprint 1 — Repository Foundation & Tooling
- **Objective:** Establish engineering scaffolding that mirrors the master plan's envisioned repository structure.
- **Key Tasks:**
  - Scaffold `spiceflow-social/` with `src/`, `tests/`, and `docs/` packages plus placeholder modules for ingestion, scheduling, scoring, and outputs.
  - Configure Poetry (or pip-tools) with baseline dependencies (`requests`, `pydantic`, `pytest`, etc.) and define Python version.
  - Add formatting and linting hooks (`black`, `ruff`, `mypy`) via `pre-commit` and create a CI workflow stub running lint + tests.
  - Draft `CONTRIBUTING.md`, `SECURITY.md`, and `.env.example` capturing handling of personal data and secrets.
  - Generate GitHub issue templates capturing the ten sprint themes.
- **Acceptance:** Clean test run (`pytest -q`) succeeds on empty scaffolding; CI workflow executes formatting and lint steps without failure.

## Sprint 2 — Personal Data Intake Preparation
- **Objective:** Formalize structured inputs for goals, preferences, and contacts while protecting sensitive information.
- **Key Tasks:**
  - Define YAML schemas using `pydantic` models for `Goal`, `PreferenceRule`, and `ContactCadence`.
  - Create `docs/samples/` containing sanitized example files; ensure `.gitignore` excludes actual `data/` directory holding personal data.
  - Implement validation CLI (`python -m spiceflow_social.cli.validate_inputs`) that checks schema conformance.
  - Document encryption/storage options (e.g., `gpg`, macOS keychain) for real files in `docs/security/data_handling.md`.
  - Integrate validation command into CI to guard against malformed configurations.
- **Acceptance:** Validation CLI runs successfully against sample data and fails gracefully with descriptive errors when schema violations occur.

## Sprint 3 — Event Source Aggregation
- **Objective:** Convert bookmark exports into normalized calendar event feeds.
- **Key Tasks:**
  - Analyze Chrome bookmark JSON and implement parser retrieving URLs, titles, and folder metadata.
  - Build ICS ingestion module leveraging `icalendar` or `ics` library to standardize event fields.
  - Implement HTML scraping adapter using `BeautifulSoup` for calendars lacking ICS feeds, with throttling/respectful access.
  - Create deduplication logic based on event UID/time/location and attach semantic tags.
  - Populate automated tests with fixture bookmark exports and ICS/HTML samples.
- **Acceptance:** Running `pytest tests/ingestion` executes parsers and produces normalized event objects persisted in temporary storage.

## Sprint 4 — Availability Detection Pipeline
- **Objective:** Provide reliable availability data for evening windows.
- **Key Tasks:**
  - Configure OAuth consent screen and store credentials via `google-auth` libraries.
  - Implement scheduler module calling Google Calendar free/busy endpoint and caching responses.
  - Model availability objects capturing start/end, overlapping commitments, and geographic anchor points.
  - Persist availability snapshots in lightweight database (SQLite or JSON) for reuse across recommendation runs.
  - Add alerting hooks logging quota usage and refresh token expirations.
- **Acceptance:** Integration test hits Google Calendar sandbox (or mocked service) and produces 30-day 6–10 PM availability records.

## Sprint 5 — Goals & Preference Structuring
- **Objective:** Translate personal intent into machine-consumable scoring inputs.
- **Key Tasks:**
  - Implement parser mapping goals/preferences YAML into weighted metrics and constraint definitions.
  - Encode entertainment vs. intellectual, divergent vs. convergent, social, fitness, and professional vectors with normalized scales.
  - Create cadence evaluator for relationship outreach frequency and workout recovery spacing.
  - Validate documents against conflicting constraints (e.g., overlapping blackout dates) and surface warnings.
  - Expose configuration toggles via `config/settings.py` to adjust weighting per category.
- **Acceptance:** Unit tests confirm parser generates deterministic weights and constraint sets from sample documents; invalid documents raise actionable errors.

## Sprint 6 — Scoring & Constraint Engine
- **Objective:** Score every candidate option while enforcing personal constraints.
- **Key Tasks:**
  - Implement scoring engine using composable evaluators (e.g., `ScoreComponent` interface) for each goal dimension.
  - Integrate constraint checks (strength session spacing, weather gating, travel feasibility placeholders).
  - Provide explanation payload capturing contributions per score component and triggered constraints.
  - Optimize performance with vectorized computations or caching to handle 30-day horizon.
  - Expand unit tests to include conflicting preferences, limited availability, and missing data scenarios.
- **Acceptance:** Running `pytest tests/scoring` generates ranked scores with attached explanations, and constraint violations short-circuit appropriately.

## Sprint 7 — Recommendation Assembly
- **Objective:** Merge inputs into nightly actionable suggestions.
- **Key Tasks:**
  - Develop recommendation orchestrator that selects top event/outreach per free evening while honoring diversity rules.
  - Implement fallback generator for at-home or self-directed options when external events fail thresholds.
  - Track recommendation history to avoid repeating similar experiences and to surface follow-up tasks.
  - Emit structured payloads (JSON + Markdown) ready for reporting layer.
  - Add integration tests simulating 30-day planning run end-to-end with mocked inputs.
- **Acceptance:** End-to-end dry run outputs recommendations for sample data with rationale fields populated and diversity constraints respected.

## Sprint 8 — Weather & Wellbeing Intelligence
- **Objective:** Enrich recommendations with environmental and wellbeing awareness.
- **Key Tasks:**
  - Connect to chosen weather API (OpenWeather/NWS) and implement caching strategy using Redis or on-disk caches.
  - Translate weather forecasts into categorical suitability signals (e.g., `OUTDOOR_OK`, `STORM`, `HEAT_ALERT`).
  - Model fatigue scoring adjustments based on consecutive intensity levels and travel durations.
  - Integrate geocoding/travel-time estimation for event locations to ensure feasibility with adjacent commitments.
  - Add resilience handling (retry/backoff) and surface alerts when data freshness thresholds are violated.
- **Acceptance:** Weather-aware recommendations skip unsuitable outdoor events in tests that simulate inclement conditions, and wellbeing rules adjust scoring accordingly.

## Sprint 9 — Experience Delivery & Feedback Loop
- **Objective:** Deliver recommendations and capture insights for continuous improvement.
- **Key Tasks:**
  - Build Markdown/email report generator summarizing evening suggestions and rationales.
  - Add optional integration with email or messaging API for proactive delivery.
  - Create feedback ingestion mechanism (CLI or form) to capture satisfaction and adjustments per recommendation.
  - Store recommendation outcomes and feedback in analytics-friendly format.
  - Produce user-facing documentation covering review cadence and feedback process.
- **Acceptance:** Manual run produces shareable report; feedback tool records inputs and influences subsequent scoring weights during test scenarios.

## Sprint 10 — Automation, Monitoring & Privacy Hardening
- **Objective:** Operationalize the system with safeguards and observability.
- **Key Tasks:**
  - Schedule recurring jobs via GitHub Actions, cron, or external scheduler to refresh plans nightly.
  - Instrument logging/metrics (structured logs, Prometheus exporters) for ingestion, scoring, and delivery phases.
  - Implement secret management workflow (e.g., `doppler`, `aws secrets manager`, or encrypted `.secrets` files).
  - Conduct privacy review checklist ensuring no personal data enters git history; add automated checks where possible.
  - Hold sprint retrospective and populate backlog for next iteration cycle based on learnings.
- **Acceptance:** Automated job completes sample run without manual intervention; monitoring dashboards/alerts capture run status and privacy guardrails are documented.

