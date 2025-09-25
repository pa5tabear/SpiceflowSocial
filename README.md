# Spiceflow Social

*A personal evening planning assistant for crafting meaningful 6–10 PM experiences across the next 30 days.*

## At a Glance
- Curates events, goals, relationships, weather, and calendar availability into balanced nightly plans.
- Scores every free evening block against personal objectives, wellbeing guardrails, and contextual constraints.
- Produces just-in-time recommendations with the rationale, prep notes, and alternates.

## Vision & Objectives
- **Holistic evening planning:** Fill each 6–10 PM slot with the highest-impact activity.
- **Goal alignment:** Move personal and professional objectives forward every week.
- **Preference awareness:** Respect entertainment, intellectual, social, and wellness preferences.
- **Balanced wellbeing:** Prevent overloading intense workouts or mentally taxing events.
- **Context sensitivity:** Account for schedule conflicts, location logistics, and weather.

## Key Inputs
| Category | Source | Purpose |
| --- | --- | --- |
| Event calendars | Chrome bookmark folder (~30 public calendars) | Load raw activity options (ICS/HTML feeds). |
| Goals & preferences | Structured doc in `docs/` | Define weights, constraints, and desired outcomes. |
| Relationship list | CSV/YAML (git-ignored) | Surface intentional outreach when events are weak fits. |
| Google Calendar | OAuth API (read-only) | Detect free vs. busy evening blocks. |
| Weather | Hourly/daily API | Filter or favor outdoor activities based on forecast. |
| Location profile | Home base & travel constraints | Validate travel feasibility relative to commitments. |

## Core Capabilities
- **Calendar ingestion:** Parse exported bookmarks, normalize ICS/HTML event feeds, and harmonize titles, times, and locations.
- **Goal & preference engine:** Translate written goals into weights and constraints (e.g., cap strength workouts per week).
- **Relationship suggestions:** Track outreach cadence and propose contact when no event clears thresholds.
- **Availability detection:** Fetch 30-day Google Calendar events to locate open 6–10 PM blocks.
- **Weather-aware filtering:** Block or highlight outdoor options based on forecast conditions.
- **Constraint-aware recommendations:** Score options, enforce wellbeing rules, and balance goal categories.
- **Report generation:** Deliver daily or weekly briefings via Markdown, email, or dashboard.

## Decision Flow
1. Enumerate the next 30 days of 6–10 PM availability from Google Calendar.
2. Collect candidate events that match date, timing, travel, and weather constraints.
3. Score each candidate using goals, preferences, social priorities, fitness targets, and professional aims.
4. Apply guardrails (variety, fatigue limits, cadence requirements) to filter the list.
5. When no event qualifies, promote relationship outreach or at-home activities.
6. Publish top recommendations with reasoning, prep notes, and backup options.

## Data Model (Draft)
- **Goal:** Description, category (fitness, professional, social, etc.), priority weight.
- **Preference:** Structured rules describing desired entertainment vs. intellectual balance, divergent vs. convergent modes, and recovery spacing.
- **Event:** Normalized fields plus derived attributes (intensity, travel time, weather sensitivity).
- **Recommendation:** Final suggestion, justification, confidence score, backup list.

## Integration Notes
- Export Chrome bookmarks to JSON, then parse to refresh event calendars.
- Standardize on ICS feeds when possible; fall back to scraping adapters for HTML calendars.
- Use Google OAuth with securely stored tokens (keyring or encrypted secrets).
- Select a reliable weather API and cache responses to control quota usage.
- Convert addresses to coordinates via geocoding and compute travel times (Google Maps or OpenRouteService).
- Consider a rule engine or lightweight constraint solver for schedule balancing.

## Implementation Roadmap
| Phase | Focus | Key Deliverables |
| --- | --- | --- |
| **Foundation** | Repo scaffolding & data contracts | Poetry/virtualenv setup, lint/test config, base schemas. |
| **Ingestion** | Calendars & availability | Bookmark parser, event normalization, Google Calendar free/busy timeline. |
| **Preferences** | Goals & weights | Machine-readable goals document, constraint calculators, scoring weights. |
| **Recommendation MVP** | Initial suggestions | Combine events + preferences, simple weather checks, distance gating. |
| **Wellbeing Enhancements** | Guardrails & alternates | Fatigue rules, richer weather logic, relationship outreach fallback. |
| **Outputs & Feedback** | Reports & learning | Markdown/email reports, feedback capture, weight tuning hooks. |
| **Automation** | Reliability | Nightly scheduler, logging, error alerts, audit trail. |

## Planned Repository Structure
```
spiceflow-social/
├── README.md
├── docs/
│   ├── goals_preferences.md
│   ├── data_model.md
│   └── api_integrations.md
├── data/              # git-ignored personal inputs
│   ├── bookmarks.json
│   ├── contacts.yaml
│   └── goals.yaml
├── src/
│   ├── ingestion/
│   ├── scheduling/
│   ├── scoring/
│   └── outputs/
└── tests/
```

## Security & Privacy
- Keep personal documents out of version control; rely on `.gitignore` and encrypted storage.
- Secure OAuth tokens (keyring, encrypted secrets files) and restrict API scopes to read-only where possible.
- Use anonymized logging for recommendation rationales when sharing metrics.
- Isolate sensitive configs if collaborating (e.g., encrypted config repo).

## Immediate Next Steps
- Finalize the structured goals and preferences document format (YAML/JSON).
- Aggregate the event calendar URLs and confirm ICS vs. HTML feed handling.
- Set up a Google Cloud project for Calendar API credentials and the OAuth consent screen.
- Choose a weather API provider and obtain credentials.
- Begin implementing ingestion pipelines and baseline scoring heuristics.

This roadmap provides the scaffolding for building a personal evening planning assistant that balances entertainment, growth, connection, and wellbeing.
