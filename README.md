# Spiceflow Social

*A Notion-connected evening planning assistant that curates meaningful 6–10 PM experiences across the next 30 days.*

## At a Glance
- Syncs intentions and context straight from Notion databases (goals, relationships, event sources, journals, feedback).
- Scores every free evening block against personal objectives, wellbeing guardrails, and contextual constraints.
- Posts weekly recommendation briefings and suggestion drafts back into Notion for human approval.

## Vision & Objectives
- **Holistic evening planning:** Fill each 6–10 PM slot with the highest-impact activity.
- **Goal alignment:** Move personal and professional objectives forward every week.
- **Preference awareness:** Respect entertainment, intellectual, social, and wellness preferences.
- **Balanced wellbeing:** Prevent overloading intense workouts or mentally taxing events.
- **Context sensitivity:** Account for schedule conflicts, location logistics, weather, and travel friction.

## Notion Source of Truth
Spiceflow Social treats Notion as the master record for strategic inputs. Key surfaces include:

| Notion Surface | Purpose | Agent Interaction |
| --- | --- | --- |
| Goals & Preferences database | Captures objectives, weights, and wellbeing constraints. | Read for scoring; write suggestion drafts for review. |
| Relationship Directory | Stores outreach cadence, priority tiers, and relationship notes. | Read for social balancing; propose cadence tweaks. |
| Event Calendar Sources | Lists newsletters, ICS feeds, and web calendars to ingest. | Read for scraping; suggest additions/removals. |
| Feedback Log | Tracks approvals/rejections of recommendations. | Read to fine-tune scoring heuristics. |
| Daily Journal | Records reflections that hint at evolving goals and interests. | Analyze entries to create suggestion candidates. |
| Weekly Review Hub | Central review page for recommendations and pending updates. | Write weekly reports, pending suggestions, and approval queues. |

See `docs/human_inputs.md` for detailed ownership and cadence guidance.

## Core Capabilities
- **Notion synchronization:** Incrementally sync all relevant databases, track edits, and surface suggestions without overwriting human-owned data.
- **Journal & feedback analysis:** Run NLP pipelines over daily entries and feedback outcomes to detect evolving goals, relationship signals, and event interests.
- **Calendar ingestion:** Parse curated event sources, normalize ICS/HTML feeds, and harmonize titles, times, and locations.
- **Availability detection:** Pull 30-day Google Calendar free/busy data for 6–10 PM windows to isolate scheduling opportunities.
- **Contextual enrichment:** Attach travel-time estimates, weather sensitivity, and intensity levels to each event.
- **Constraint-aware recommendations:** Score options, enforce wellbeing rules, and balance goal categories across the horizon.
- **Review workflow:** Publish weekly recommendation packets and suggestion drafts to the Weekly Review Hub, then capture approvals back into the system.

## Decision Flow
1. Sync Notion databases and Google Calendar availability; pull weather forecasts and travel data.
2. Collect candidate events that satisfy date/time, travel, and weather constraints.
3. Score each candidate using goals, preferences, social priorities, fitness targets, and professional aims.
4. Apply guardrails (variety, fatigue limits, cadence requirements) to filter the list.
5. When no event qualifies, promote relationship outreach or at-home activities.
6. Post weekly recommendations with rationale and backup options to Notion for approval.
7. Log approvals/rejections and update learning signals.

## Suggestion Lifecycle
- Analyze new journal entries and feedback signals.
- Draft proposed updates for goals, relationship cadences, or event sources with confidence tags.
- Write proposals to the Weekly Review Hub (`Pending Suggestions`).
- Human reviews suggestions weekly (configurable cadence), marking them Approved/Rejected/Deferred.
- Automation applies approved changes back into the source databases and records outcomes for auditing.

## Integration Architecture
- **docs/notion_integration.md** describes the Notion data model, sync cadences, and human-in-the-loop approvals.
- **docs/agent_tasks.md** enumerates agent responsibilities across ingest, analysis, recommendations, and operations.
- **docs/human_inputs.md** outlines ongoing human contributions and review expectations.

## Implementation Roadmap
| Phase | Focus | Key Deliverables |
| --- | --- | --- |
| **Foundation** | Repo scaffolding & Notion schema mapping | Project setup, SDK clients, typed models for Notion databases. |
| **Notion Sync & Journals** | Data ingestion and NLP tooling | Incremental sync service, journal analyzers, suggestion generator. |
| **Event & Availability Ingestion** | Calendars, Google availability, weather/travel enrichment | Bookmark-based scraping orchestrator, free/busy timeline, context annotators. |
| **Recommendation MVP** | Initial 30-day planner | Scoring engine integrating Notion data, weather filtering, distance gating. |
| **Review Workflow** | Weekly hub and approvals | Notion report generators, approval processing, feedback logging. |
| **Wellbeing Enhancements** | Guardrails & alternates | Fatigue rules, richer weather logic, outreach fallback strategies. |
| **Automation & Monitoring** | Reliability & observability | Scheduled jobs, alerts, audit logs, configurable cadences. |

## Planned Repository Structure
```
spiceflow-social/
├── README.md
├── docs/
│   ├── agent_tasks.md
│   ├── human_inputs.md
│   └── notion_integration.md
├── data/              # git-ignored connectors/secrets (if any local caching is required)
├── src/
│   ├── ingestion/
│   ├── notion_sync/
│   ├── scheduling/
│   ├── scoring/
│   └── outputs/
└── tests/
```

## Security & Privacy
- Use minimally scoped Notion integration tokens stored outside version control (env vars, secret manager).
- Keep personal data (journals, contacts, credentials) inside Notion or encrypted stores; never commit to git.
- Log all automated writes to Notion and highlight them in weekly reviews for transparency.

## Immediate Next Steps
- Define the Notion database schemas and create template pages for Weekly Review Hub content.
- Generate integration tokens and configure secure storage for Notion, Google, weather, and travel APIs.
- Scaffold the Notion sync service and journal analysis pipeline.
- Implement the event scraping orchestrator driven by the Notion Event Calendar Sources list.
- Build the weekly recommendation publisher that writes summaries and suggestions back into Notion.

This Notion-centered architecture lets the assistant automate ingestion, analysis, and planning while keeping humans firmly in control of strategic decisions and approvals.
