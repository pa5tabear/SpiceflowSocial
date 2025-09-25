# AI Programming Agent Responsibilities

## Data Ingestion & Normalization
- Import and parse calendar feeds from the curated bookmark export, normalizing event metadata into a unified schema.
- Sync Google Calendar free/busy data for the next 30 days within the 6–10 PM window and flag conflicts.
- Hydrate goal, preference, and relationship documents into typed domain models, validating required fields and defaults.
- Enrich events with derived attributes (intensity, category, travel estimates) using location data and third-party services.

## Scoring & Decision Logic
- Maintain weighting functions and constraint rules derived from human-authored goals and wellbeing limits.
- Score candidate activities against entertainment, intellectual, social, wellness, and professional objectives.
- Apply guardrails such as fatigue management, diversity quotas, and cadence requirements for outreach.
- Resolve ties or missing candidates by escalating to alternative recommendations (relationship outreach, at-home options).

## Context Awareness
- Integrate weather forecasts to suppress or boost outdoor activities based on threshold logic.
- Combine location feasibility, travel time, and surrounding commitments to ensure logistical viability.

## Output & Feedback Loop
- Generate daily or weekly recommendation briefings (Markdown, email, dashboard) with justifications and preparation notes.
- Capture user feedback on delivered plans and update scoring weights or constraint parameters accordingly.
- Log decision rationale, data sources, and confidence metrics for auditing and future tuning.

## Operations & Automation
- Schedule recurring runs (e.g., nightly) that refresh the 30-day planning horizon.
- Monitor ingestion errors, API quota usage, and authentication health, raising alerts when intervention is required.
- Guard sensitive data by honoring secret storage policies and ensuring personal documents remain outside version control.
