# Spiceflow Social

*A Notion-connected evening planning assistant that curates meaningful 6–10 PM experiences across the next 30 days.*

## At a Glance
- Powered by Notion's **official** MCP server (`@notionhq/notion-mcp-server`) to sync goals, relationships, event sources, journals, and feedback directly from your workspace.
- Scores every free evening block against personal objectives, wellbeing guardrails, and contextual constraints (weather, travel, schedule).
- Publishes weekly recommendation packets and suggestion drafts back into Notion for human approval.

## Repository Quickstart
1. **Bootstrap Notion:** Follow `docs/notion_bootstrap.md` to create databases in a blank Notion workspace using the official MCP server.
2. **Run MCP server:**
   ```bash
   export NOTION_TOKEN="ntn_..."
   npx @notionhq/notion-mcp-server
   ```
   (See `integrations/notion-official/README.md` for Docker and client config examples.)
3. **Populate data:** Enter goals, relationships, event sources, and start journaling in Notion.
4. **Configure secrets:** Create `.env` with Notion, Google, weather, and travel credentials for the ingestion services.
5. **Build services:** Scaffold the sync, scoring, and recommendation pipelines to read/write through MCP.

## Notion Source of Truth
| Surface | Purpose | Agent Interaction |
| --- | --- | --- |
| Goals & Preferences | Objectives, weights, wellbeing constraints. | Read for scoring; draft updates into Pending Suggestions. |
| Relationship Directory | Outreach cadence, tiers, notes. | Read for social balance; propose cadence tweaks. |
| Event Calendar Sources | Curated feeds to scrape. | Read for ingestion; suggest additions/removals. |
| Pending Suggestions | Queue of AI-drafted updates. | Write with rationale and confidence; await approval. |
| Evening Recommendations | Weekly 30-day plan. | Write proposals; observe status changes. |
| Recommendation Feedback | Decisions and rationale. | Read to tune scoring heuristics. |
| Daily Journal | Free-form reflections. | Read/analyze for emerging themes; optionally write summaries. |
| Weekly Review Hub | Human control center. | Write weekly packets and linked views. |

Detailed architecture and workflows live in `docs/notion_integration.md`, while database templates are under `docs/notion_templates/`.

## Core Capabilities
- **Official MCP sync:** Use the Notion-hosted OpenAPI tool surface to provision databases, sync content, and submit suggestions.
- **Journal & feedback analysis:** NLP pipelines over daily entries and feedback outcomes to surface suggestions.
- **Calendar & event ingestion:** Scrape curated sources, normalize data, and align with Google Calendar availability.
- **Contextual enrichment:** Compute travel friction, detect weather risks, and classify intensity to enforce wellbeing guardrails.
- **Constraint-aware recommendations:** Score options, enforce variety, and balance goal categories across the horizon.
- **Review workflow:** Publish weekly recommendation packets and pending suggestions to Notion; ingest approval decisions and close the loop.

## Decision Flow
1. Sync Notion databases and Google Calendar availability; fetch weather/travel context.
2. Compile candidate events that match date/time, travel, and weather constraints.
3. Score candidates against goals, relationships, wellbeing, and professional aims.
4. Apply guardrails (fatigue limits, cadence targets, diversity requirements).
5. When no event qualifies, promote relationship outreach or at-home alternatives.
6. Post weekly recommendations and suggestion drafts to Notion.
7. Record approvals/rejections and update learning signals.

## Documentation Map
- `docs/notion_bootstrap.md` – Build the Notion workspace with the official MCP server.
- `docs/notion_integration.md` – Architecture, cadences, and human-in-loop workflow.
- `docs/human_inputs.md` – Your responsibilities inside Notion.
- `docs/agent_tasks.md` – Automation responsibilities.
- `docs/notion_templates/` – JSON payloads for database creation.
- `integrations/notion-official/README.md` – MCP server runtime options and client configs.

## Implementation Roadmap
| Phase | Focus | Deliverables |
| --- | --- | --- |
| **Foundation** | Repo scaffolding, Notion schema mapping, secrets management. | Project setup, official MCP integration instructions, `.env` template, typed models. |
| **Notion Sync & Journals** | Data ingestion & NLP tooling. | Incremental sync service, journal analyzers, suggestion generator. |
| **Event & Availability Ingestion** | Calendars, Google availability, weather/travel enrichment. | Scraper orchestrator, free/busy timeline builder, context annotators. |
| **Recommendation MVP** | Initial 30-day planner. | Scoring engine integrating Notion data, weather filtering, distance gating. |
| **Review Workflow** | Weekly hub & approvals. | Notion report publishers, approval processing, feedback logging. |
| **Wellbeing Enhancements** | Guardrails & alternates. | Fatigue rules, richer weather logic, outreach fallback strategies. |
| **Automation & Monitoring** | Reliability & observability. | Scheduled jobs, alerts, audit logs, cadence controls surfaced in Notion. |

## Repository Structure
```
spiceflow-social/
├── README.md
├── docs/
│   ├── agent_tasks.md
│   ├── human_inputs.md
│   ├── notion_bootstrap.md
│   ├── notion_integration.md
│   └── notion_templates/
│       ├── daily_journal.json
│       ├── event_sources.json
│       ├── feedback_log.json
│       ├── goals_preferences.json
│       ├── recommendations.json
│       ├── relationships.json
│       ├── suggestions.json
│       └── weekly_review.json
├── integrations/
│   └── notion-official/
│       └── README.md
├── data/              # git-ignored personal caches (if required later)
├── src/
│   ├── ingestion/
│   ├── notion_sync/
│   ├── scheduling/
│   ├── scoring/
│   └── outputs/
└── tests/
```

## Security & Privacy
- Use scoped integration tokens stored outside version control (env vars, secret manager).
- Keep personal data (journals, contacts, credentials) in Notion or encrypted stores; never commit to git.
- Log every automated write and highlight it in weekly reviews for transparency.
- Rotate credentials periodically and audit permissions in Notion's integration panel.

## Immediate Next Steps
- Stand up the Notion workspace using the official MCP server and seed initial data.
- Configure secrets (`.env` or secret manager) for Notion, Google, weather, travel, and notifications.
- Scaffold the Notion sync service, journal analysis pipeline, and event ingestion orchestrator.
- Build the weekly recommendation publisher that writes summaries and suggestions into Notion.

This Notion-centered architecture lets the assistant automate ingestion, analysis, and planning while keeping humans firmly in control of strategic decisions and approvals.
