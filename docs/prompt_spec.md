# Prompt Schema Specification for Spiceflow Social Event Curation

**Version:** 1.0  
**Date:** 2025-09-28  
**Owner:** Gemini

## 1. Overview

This document specifies the exact JSON schema that the LLM research agent must produce for each event it discovers. Adherence to this schema is critical for ensuring data consistency for the downstream ICS generation, scoring, and preference-matching systems.

The top-level response from the LLM should be a JSON object containing two keys:
- `summary` (string): A brief, one-paragraph summary of the research findings for the source.
- `events` (array): An array of event objects, where each object strictly follows the schema defined below.

## 2. Event Object Schema

Each object in the `events` array must contain the following fields. All fields are required unless otherwise noted.

---

### 2.1. ICS Calendar Fields

These fields are essential for generating a rich, fully-compatible `.ics` file for Apple Calendar and other calendar applications.

| Field Name              | Type    | Description                                                                                                 | Example                                                 |
| ----------------------- | ------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `title`                 | string  | The exact, official name of the event.                                                                      | "Powering Tomorrow: A Conversation on the Clean Energy Future" |
| `description`           | string  | A rich 2-3 sentence summary of the event's content and purpose. Ideal for the calendar event notes.         | "Join former Energy Secretary Jennifer Granholm for a keynote on the future of clean energy..." |
| `start_local`           | string  | The precise start time in ISO 8601 format for the `America/Detroit` timezone.                               | "2025-09-30T17:30:00-04:00"                             |
| `end_local`             | string  | The precise end time in ISO 8601 format. If not stated, estimate based on content (e.g., start + 90 minutes). | "2025-09-30T19:00:00-04:00"                             |
| `location`              | string  | The full, physical address of the event venue, including name, street, city, and state.                     | "Rackham Auditorium, 915 E Washington St, Ann Arbor, MI"  |
| `url`                   | string  | The direct, canonical URL to the event's information or registration page.                                  | "https://events.umich.edu/event/12345"                  |
| `organizer`             | string  | (Optional) The name and/or email of the event organizer, if available.                                      | "School for Environment and Sustainability (SEAS)"        |
| `cost`                  | string  | The exact cost of the event. Must be "Free" or a dollar amount (e.g., "$15.00").                            | "Free"                                                  |
| `registration_required` | boolean | `true` if attendees must register, RSVP, or buy tickets in advance. `false` otherwise.                      | `true`                                                  |
| `capacity_limited`      | boolean | `true` if the source mentions limited seating, "selling out," or other capacity constraints.                | `true`                                                  |
| `accessibility_notes`   | string  | (Optional) Any information regarding accessibility (e.g., wheelchair access, ASL interpretation).           | "Wheelchair accessible via the north entrance."           |

---

### 2.2. Scoring & Analysis Fields

These fields provide the quantitative and qualitative data needed for the portfolio selection and scoring engine.

| Field Name              | Type    | Description                                                                                             | Example                               |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `intensity_level`       | integer | A 1-5 scale of mental/physical energy required (1=passive viewing, 5=intensive all-day workshop).       | `2`                                   |
| `social_type`           | string  | Enum: "networking", "passive", "interactive", "presentation".                                           | "presentation"                        |
| `learning_format`       | string  | Enum: "lecture", "hands-on", "discussion", "performance", "exhibition".                                 | "lecture"                             |
| `venue_tier`            | string  | Enum: "tier1" (prestigious, e.g., Hill Aud.), "tier2" (standard, e.g., dept. building), "tier3" (casual). | "tier1"                               |
| `speaker_quality`       | string  | Enum: "keynote", "expert", "local", "student", "unknown".                                               | "keynote"                             |
| `follow_up_potential`   | integer | A 1-5 scale of opportunity for future engagement or networking (1=none, 5=high).                        | `3`                                   |
| `seasonal_fit`          | string  | Enum: "indoor", "outdoor", "weather_dependent".                                                         | "indoor"                              |

---

### 2.3. Preference Alignment Fields

These fields directly map the event to the user's stated preferences from `preferences.yaml`.

| Field Name              | Type    | Description                                                                                             | Example                               |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `travel_minutes`        | integer | Estimated travel time in minutes from a central point in Ann Arbor (e.g., downtown).                    | `10`                                  |
| `travel_category`       | string  | Enum based on `travel.bins`: "near", "local", "far", "too_far".                                         | "near"                                |
| `budget_category`       | string  | Enum based on cost: "free", "low" (<$25), "medium" ($25-75), "high" (>$75).                             | "free"                                |
| `time_preference_match` | float   | A 0.0-1.0 score indicating how well the event fits into the user's preferred time windows.              | `0.9`                                 |
| `must_see`              | boolean | `true` only if the event contains a `must_see_keyword` or is otherwise exceptional (e.g., major speaker). | `true`                                |
| `must_see_rationale`    | string  | (Optional) A brief explanation for why `must_see` is true.                                              | "Features keynote by Jennifer Granholm" |
| `quota_categories`      | array   | A list of strings identifying which weekly quotas this event helps fulfill (e.g., "career_tech", "social_arts"). | `["career_tech", "deep_networking"]` |
| `novelty_score`         | float   | A 0.0-1.0 score based on how unique this event is compared to typical offerings.                        | `0.8`                                 |

---

### 2.4. Deep Goal Analysis Fields

For each of the user's goal categories, a detailed analysis is required.

| Field Name                 | Type    | Description                                                                                             | Example                               |
| -------------------------- | ------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `career_keyword_matches`   | array   | List of specific keywords from the content that match the "Career Learning" goal.                       | `["sustainability", "energy"]`        |
| `career_alignment_score`   | float   | A 0.0-1.0 score of how well the event serves this goal.                                                 | `0.95`                                |
| `career_rationale`         | string  | A 1-2 sentence explanation of the alignment score.                                                      | "Directly addresses core career interests in energy policy." |
| `social_keyword_matches`   | array   | List of specific keywords from the content that match the "Social Connection" goal.                     | `["reception"]`                       |
| `social_alignment_score`   | float   | A 0.0-1.0 score of how well the event serves this goal.                                                 | `0.4`                                 |
| `social_rationale`         | string  | A 1-2 sentence explanation of the alignment score.                                                      | "A pre-event reception offers some networking opportunities." |
| `wellbeing_keyword_matches`| array   | List of specific keywords from the content that match the "Wellbeing/Fitness" goal.                     | `[]`                                  |
| `wellbeing_alignment_score`| float   | A 0.0-1.0 score of how well the event serves this goal.                                                 | `0.0`                                 |
| `wellbeing_rationale`      | string  | A 1-2 sentence explanation of the alignment score.                                                      | "This event has no direct wellbeing or fitness component." |
| `outdoors_keyword_matches` | array   | List of specific keywords from the content that match the "Outdoors/Nature" goal.                       | `[]`                                  |
| `outdoors_alignment_score` | float   | A 0.0-1.0 score of how well the event serves this goal.                                                 | `0.0`                                 |
| `outdoors_rationale`       | string  | A 1-2 sentence explanation of the alignment score.                                                      | "This is an indoor lecture."          |

