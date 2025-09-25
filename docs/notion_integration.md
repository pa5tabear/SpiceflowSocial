# Notion Integration Architecture

Spiceflow Social uses Notion as the system of record for strategic inputs and feedback while delegating automation and analysis to the agentic backend. This document outlines the core Notion databases, synchronization flows, and review cadences.

## Notion Data Surfaces
| Database / Page | Purpose | Key Fields | Sync Direction |
| --- | --- | --- | --- |
| Goals & Preferences | Capture long-term objectives, wellbeing guardrails, weighting factors, and qualitative context. | Goal name, category, priority, constraints, notes, last reviewed date. | Notion ➜ Spiceflow (read), Suggestions ➜ Notion (write via proposal sub-page). |
| Relationship Directory | Track relationship tiers, outreach cadence, last contact, and qualitative context. | Person, priority tier, desired cadence, last touchpoint, notes. | Notion ➜ Spiceflow (read), Suggestions ➜ Notion (write). |
| Event Calendar Sources | Maintain authoritative list of event feeds or web sources to scrape. | Source name, URL, tags, location radius, verification status. | Notion ➜ Spiceflow (read), Suggestions ➜ Notion (write). |
| Personal Feedback Log | Record approvals / rejections of recommendations and any manual notes. | Recommendation ID, outcome, feedback text, tags. | Notion ➜ Spiceflow (read). |
| Daily Journals | Free-form daily reflections used to detect evolving goals and relationship cues. | Date, mood metrics, highlights, challenges, free-write content. | Notion ➜ Spiceflow (read), Summaries ➜ Notion (write back optional). |
| Weekly Review Hub | Aggregates proposed revisions, selected events, and recap of the past week. | Week range, pending suggestions, approved updates, calendar commitments. | Spiceflow ➜ Notion (write), Human ➜ Notion (approve). |

## Integration Components
- **Notion Sync Service:** Periodically polls the relevant databases using the Notion API, normalizes records, and pushes them into the internal datastore used by the recommendation engine.
- **Journal Analyzer:** Processes new daily journal entries through NLP pipelines to detect emerging themes, shifts in motivation, relationship signals, and event interests. Outputs candidate updates tagged with confidence levels.
- **Suggestion Generator:** Aggregates signals from journal analysis, feedback logs, and engagement metrics to draft proposed revisions for goals, relationships, and calendar sources. Suggestions are written back into the Weekly Review Hub for human approval.
- **Web Scraper Orchestrator:** Reads the Notion Event Calendar Sources database, fetches fresh event data from listed feeds, and stores normalized events for scoring.
- **Recommendation Engine:** Combines normalized events, availability (from Google Calendar), goals/preferences, relationship status, and weather to rank evening options for the next 30 days.
- **Approval & Logging Layer:** Posts recommended events and rationale into the Weekly Review Hub, tracks approvals, and updates the feedback log.

## Cadences & Triggers
| Cadence | Activities |
| --- | --- |
| Daily | Sync new journal entries, refresh feedback log, update relationship last-contact dates, run quick event fetch for same-week adjustments. |
| Weekly (default, configurable) | Run full event scrape, recompute 30-day recommendation horizon, draft suggestion batch for goals/relationships/calendar sources, populate Weekly Review Hub page. |
| Monthly (optional) | Deep-dive analysis of goal progress, restructure weighting logic, escalate high-confidence suggestions for human review. |

Cadences should remain configurable via environment variables or Notion configuration properties to allow weekly vs. monthly review flexibility.

## Human-in-the-Loop Workflow
1. **Automated Intake:** Notion sync service pulls the latest data for goals, relationships, calendar sources, feedback, and journals.
2. **Analysis & Suggestion Drafting:** Journal analyzer and suggestion generator produce structured proposals (e.g., "Increase strength training cap" or "Add XYZ event newsletter").
3. **Review Surface:** Proposals are written to a "Pending Suggestions" linked database under the Weekly Review Hub with status fields (`Proposed`, `Accepted`, `Rejected`, `Deferred`).
4. **Human Approval:** You review suggestions on the weekly cadence, adjusting statuses and optionally editing details.
5. **Actioning:** Approved suggestions trigger updates in their source databases (e.g., modify an entry in Goals & Preferences) via automation tasks.
6. **Feedback Loop:** Outcomes and human decisions are logged for future tuning.

## Security & Access
- Use a dedicated Notion integration token with scoped database access.
- Store the token in secret management (environment variable or vault) and do not commit to version control.
- Maintain an audit log of read/write actions to trace automated changes and approvals.

## Next Steps for Implementation
1. Model the Notion databases and export their schemas for use in SDK integrations.
2. Scaffold the Notion sync service with typed clients and rate-limit handling.
3. Implement journaling NLP pipelines (keyword extraction, sentiment, clustering) to generate suggestion candidates.
4. Build the Weekly Review Hub templates (pending suggestions view, approved recommendations, weekly summary).
5. Wire the event scraping orchestrator to read from the Event Calendar Sources database and schedule weekly runs.
6. Design the suggestion approval automation that applies accepted changes back into the appropriate Notion databases.

This architecture keeps humans in control of strategic documents while letting the agent automate ingestion, analysis, and recommendation workflows on top of Notion-stored knowledge.
