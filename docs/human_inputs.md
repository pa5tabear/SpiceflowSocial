# Human Inputs (Notion-Centric)

All strategic inputs live inside Notion workspaces so they remain under human ownership. The agent reads from these surfaces and submits suggested updates for approval.

| Notion Surface | Owner Actions | Purpose | Format / Notes |
| --- | --- | --- | --- |
| Goals & Preferences database | Define and periodically refine objectives, wellbeing guardrails, and weighting hints. Approve or reject suggested revisions surfaced in the Weekly Review Hub. | Anchor the scoring logic and constraint system for recommendations. | One entry per goal/preference with fields for category, priority, constraints, narrative context, last reviewed date. |
| Relationship Directory database | Maintain contact list, set outreach cadence, log significant interactions, review agent-suggested adjustments. | Ensure social recommendations align with intentional relationship building. | Includes person name, tier, desired cadence, last contact, notes. |
| Event Calendar Sources database | Curate the list of newsletters, ICS feeds, and web calendars worth scraping. Approve additions suggested by journal insights or feedback trends. | Provide authoritative activity sources for the scraper orchestrator. | Fields for source name, URL, tags, geography, verification status, freshness cadence. |
| Feedback Log database | Record approvals/rejections of weekly recommendations and capture qualitative feedback. | Close the loop so the agent can learn from decisions and tune scoring heuristics. | Reference to recommendation ID, outcome, reason codes, free-form notes. |
| Daily Journal database | Continue journaling as normal; flag entries you want emphasized. Review periodic summaries for accuracy. | Enables NLP analysis of evolving interests, moods, and emerging goals. | Free-form content with optional sentiment tags, highlights, challenges. |
| Weekly Review Hub page/database | Review pending suggestions (goals, relationships, calendar sources), approve recommended events for the next 30 days, leave comments. | Central command center for human-in-the-loop decisions. | Template includes linked views of suggestions, recommendation queue, and recap metrics. |
| Integration Credentials | Create and manage Notion integration tokens, Google API secrets, weather/travel API keys. | Secure connectivity for the agent to read/write data. | Store in secrets manager or environment variables; never enter directly into Notion properties. |

## Human Rhythm
- **Daily:** Journal entries, quick reactions to recommendations (approve/reject), optional inline comments.
- **Weekly (default, configurable):** Review the Weekly Review Hub, approve event selections, triage proposed updates to goals/relationships/calendar sources.
- **Monthly or Quarterly:** Step back to adjust high-level priorities, archive outdated goals, and audit integration permissions.

You remain the final approver for strategic changes; the agent simply drafts suggestions based on the signals it ingests from Notion and other data sources.
