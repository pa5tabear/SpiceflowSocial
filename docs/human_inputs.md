# Human Inputs (Notion-Centric)

All strategic inputs live inside Notion and remain under human ownership. Use the MCP bootstrap flow (`docs/notion_bootstrap.md`) to create the databases before populating them.

| Notion Surface | Owner Actions | Purpose | Notes |
| --- | --- | --- | --- |
| Goals & Preferences | Define objectives, wellbeing guardrails, and weighting hints; review AI suggestion proposals weekly. | Anchors scoring logic and constraint system. | Populate fields for category, priority, weights, constraints, narratives, and `Last Reviewed`. |
| Relationship Directory | Maintain contacts, outreach cadence, last touchpoint, and qualitative notes. | Ensures recommendations align with intentional relationship building. | Update `Desired Cadence` and log `Last Contact` when you connect. |
| Event Calendar Sources | Curate newsletters, ICS feeds, and web calendars worth scraping. | Provides authoritative event intake list. | Review agent-proposed additions/removals in Pending Suggestions. |
| Pending Suggestions | Approve or reject AI-drafted adjustments to goals, relationships, and sources. | Keeps strategic changes human-in-the-loop. | Update `Status` (`Approved`, `Rejected`, `Deferred`) and leave comments as needed. |
| Evening Recommendations | Approve the proposed 6–10 PM plan for the upcoming horizon. | Feeds your decisions back into the feedback loop. | Mark `Status` and leave rationale for future learning. |
| Recommendation Feedback | Log the final decision and qualitative feedback for each recommendation. | Informs scoring heuristics and pattern detection. | Capture `Decision`, `Reason`, and optional tags. |
| Daily Journal | Continue journaling daily; optionally tag entries for emphasis. | Drives suggestion generation and wellbeing insights. | Include highlights/challenges to improve NLP accuracy. |
| Weekly Review Hub | Central board to triage suggestions, approve plans, and capture reflections. | Weekly control center for Spiceflow Social. | Customize linked database views to match your cadence. |
| Integration Credentials | Issue and protect tokens for Notion, Google, weather, travel, and notifications. | Enables the agent to automate workflows. | Store in secrets manager or `.env`; rotate periodically. |

## Human Rhythm
- **Daily:** Journal, add relationship touchpoint notes, log quick feedback on recommendations.
- **Weekly (default):** Review the Pending Suggestions database, approve/decline evening recommendations, update Weekly Review notes.
- **Monthly or Quarterly:** Reassess high-level goals, archive stale relationships or event sources, audit integration permissions, and rotate credentials.

You remain the final approver for strategic moves; the agent merely prepares suggestions and drafts content in Notion for your review.
