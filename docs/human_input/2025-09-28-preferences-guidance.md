## Preferences Guidance — 2025-09-28

Done — I’ve stripped Lansing from the decision system and made Ann Arbor the sole home base.

Here are the updated bits for your repo.

## Human-readable preferences (README excerpt)

* Build a month that maximizes **career learning/networking** (energy, climate, AI, data centers).
* Maintain **social connection** and **wellbeing** (outdoors/fitness/mental health).
* Keep **churn low**: once the plan is in place, change only for meaningful deltas or cancellations.
* Emphasize **Ann Arbor** proximity with reasonable travel time.
* Keep **budget reasonable** without blocking the occasional must-see event.

## `src/preferences.yaml`

```yaml
meta:
  tz: "America/Detroit"
  home_city: "Ann Arbor, MI"
  stable_plan_bias: true

time_windows:
  evenings:
    weekdays: ["17:30", "21:30"]
    saturday: ["10:00", "22:00"]
    sunday:   ["11:00", "20:00"]
  quiet_hours: ["22:30", "07:00"]
  no_change_window_hours: 24

caps:
  max_per_day: 2
  max_per_week: 6
  max_weekend_total: 4
  daily_change_budget: 2
  weekly_change_budget: 6

budgets:
  weekly_spend_cap_usd: 150
  allow_overage_events_per_week: 1

travel:
  origin: "Ann Arbor, MI"
  bins:
    - { label: "near",    minutes_max: 15, score_bonus: 0.05 }
    - { label: "local",   minutes_max: 30, score_bonus: 0.02 }
    - { label: "far",     minutes_max: 45, score_penalty: -0.06 }
    - { label: "too_far", minutes_max: 999, score_penalty: -0.12 }
  suppress_too_far: false

quotas:
  weekly:
    career_tech_min: 2
    social_arts_min: 2
    outdoors_wellbeing_min: 1
    deep_networking_min: 1
  monthly:
    arts_culture_min: 2
    outdoors_min: 2
    major_flagship_min: 1

weights:
  goals:
    career_learning: 0.25
    social_connection: 0.20
    wellbeing_fitness: 0.15
    outdoors_nature: 0.10
  novelty: 0.05
  speaker_org_relevance: 0.10
  travel_time_penalty: -0.10
  cost_penalty: -0.05
  conflict_overlap_penalty: -0.20
  sticky_keep_bonus: 0.15
  must_see_bonus: 0.20

preferences:
  start_time:
    ideal_weeknight_range: ["18:00","19:30"]
    late_start_penalty_after: "20:00"
    late_start_penalty: -0.04
  duration_defaults:
    lecture_minutes: 75
    fair_minutes: 180
    workshop_minutes: 120
  venue_tiers:
    tier1_bonus: 0.06
    tier2_bonus: 0.02
    tier3_penalty: -0.04

categories:
  map:
    Lecture: ["career_learning"]
    Tech: ["career_learning","social_connection"]
    Business: ["career_learning"]
    Climate: ["career_learning"]
    Arts: ["social_connection"]
    Music: ["social_connection"]
    Wellness: ["wellbeing_fitness"]
    Outdoors: ["outdoors_nature","wellbeing_fitness"]
    Community: ["social_connection"]
  must_see_keywords:
    - "keynote"
    - "Granholm"
    - "conference"
    - "summit"
    - "Climate Week"
    - "MSBC"
    - "Farrand"

anti_churn:
  min_swap_gain: 0.22
  cooldown_days_per_slot: 5
  freeze_hours_near_term: 24

exceptions:
  always_surface:
    - "Cancelled"
    - "Postponed"
    - "Venue change"
    - "Time change"
  urgent_override_keywords:
    - "registration closing"
    - "last tickets"
    - "limited capacity"
```

## `src/scoring_config.json`

No change needed; it already uses `"home_location": "Ann Arbor, MI"`.
