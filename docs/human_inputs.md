# Human Inputs

| Input | Owner | Purpose | Format / Notes |
| --- | --- | --- | --- |
| Goals and preferences | Human | Encode long-term objectives, desired activity mix, wellbeing guardrails, and weighting rules. | Structured Markdown source (`docs/goals_preferences.md`) plus machine-readable export (`data/goals.yaml`). |
| Relationship list | Human | Track priority contacts and desired outreach cadence for social recommendations. | CSV or YAML stored in `data/contacts.yaml` (git-ignored). |
| Event calendar sources | Human | Curate the public calendars that seed activity options. | Chrome bookmark folder export (`data/bookmarks.json`), refreshed when calendars change. |
| Location profile | Human | Describe home base, typical travel radius, transit modes, and high-friction locations. | YAML or JSON document referenced by ingestion layer. |
| Google Workspace account | Human | Grant read-only Google Calendar access for evenings and maintain accurate personal schedule. | OAuth client credentials (client ID/secret), consent screen configuration, and ongoing calendar hygiene. |
| Weather API credentials | Human | Authorize forecast requests for planning horizons. | API key or token for chosen provider (e.g., OpenWeather, NWS) stored securely via env vars or secrets manager. |
| Travel time provider access | Human | Enable distance and travel-time estimates between events and home base. | API key for Google Maps, OpenRouteService, or equivalent (optional but recommended). |
| Personal feedback | Human | Review generated plans, supply accept/reject feedback, and adjust preferences over time. | Lightweight feedback log or in-app survey captured after recommendations. |
| Security configuration | Human | Decide on secret storage, access controls, and collaborator permissions. | `.env` template, secret management policy, encrypted storage setup. |

These inputs stay under human control to keep the assistant aligned with evolving goals, relationships, and privacy requirements.
