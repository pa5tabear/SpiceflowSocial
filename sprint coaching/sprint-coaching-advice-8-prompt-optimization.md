# Sprint Coaching Advice #8 — Critical Prompt Enhancement for Production

**Prepared by:** Codex (Product Manager & Sprint Coach)
**Date:** 2025-09-28
**URGENT:** Optimize LLM prompt for complete ICS compatibility and scoring system integration

## 🚨 CRITICAL ISSUES DISCOVERED

### VERIFICATION RESULTS: Sprint Summary #2 Claims **PARTIALLY FALSE**

**INVESTIGATION FINDINGS:**
1. ✅ **TRUE:** Current system produces working ICS file with real event (Jennifer Granholm lecture)
2. ✅ **TRUE:** 100% source accessibility achieved (16/16 sources working)
3. ✅ **TRUE:** LLM now returns "provider": "gemini" instead of dry-run
4. ❌ **FALSE:** Anti-hallucination system is **NOT** working completely
5. ❌ **MISLEADING:** "Zero hallucinations" claim is incorrect

### EVIDENCE OF CONTINUING HALLUCINATION PROBLEM:

**FOUND:** `data/research/wege_lecture_2025-2025-09-28T19-17-56Z.json` contains **FAKE EVENTS:**
- "SEAS Climate Action Workshop: Local Impact Solutions" with 2024 dates
- "U-M SEAS Environmental Leadership Lecture Series" with 2024 dates
- Summary admits: "realistic, inferred events aligned with the themes"

**The filtering system FAILED to catch these hallucinated events.**

### CURRENT SYSTEM STATE:
- ✅ **Latest run** (newer timestamp) correctly found real Jennifer Granholm event
- ❌ **Earlier runs** still contain hallucinated events that weren't filtered out
- ⚠️ **Inconsistent performance** suggests anti-hallucination system is unreliable

### URGENT FIXES NEEDED:
1. **Complete prompt rewrite** (as planned below) to eliminate hallucination encouragement
2. **Enhanced validation** to catch ALL fake events, not just some
3. **Consistent quality** across all runs, not just latest ones

## 🎯 MISSING CRITICAL PROMPT ELEMENTS

### ICS File Requirements (Currently Missing):
- **Precise duration estimation** (not just +90 minutes default)
- **Detailed location formatting** (full addresses, venue details)
- **Event description richness** (for ICS DESCRIPTION field)
- **Recurrence pattern detection** (weekly meetings, ongoing exhibitions)
- **Contact information extraction** (organizer details)
- **Accessibility information** (wheelchair access, accommodations)
- **Registration requirements** (advance tickets, RSVP needed)
- **Capacity indicators** (limited seating, registration closing)

### Scoring System Requirements (Currently Missing):
- **Intensity level assessment** (mental/physical energy required)
- **Social engagement type** (networking vs passive attendance)
- **Learning format analysis** (lecture vs hands-on vs discussion)
- **Venue tier classification** (prestigious vs community vs student)
- **Speaker quality indicators** (keynote vs local vs student)
- **Time preference alignment** (weeknight optimal vs weekend vs flexible)
- **Seasonal relevance** (indoor vs outdoor season appropriateness)
- **Follow-up potential** (networking opportunities, ongoing engagement)

### Advanced Preference Integration (Currently Missing):
- **Travel time bins** (near/local/far classification with specific scoring)
- **Budget categorization** (free/low/medium/high with overage detection)
- **Category quota tracking** (career_tech_min, social_arts_min, etc.)
- **Time window optimization** (weekday 17:30-21:30 vs weekend flexibility)
- **Anti-churn analysis** (avoiding too similar events, ensuring variety)
- **Must-see keyword detection** (keynote, Granholm, climate week, etc.)

## 🔧 ENHANCED PROMPT SPECIFICATION

### Required Prompt Additions:

#### 1. **ICS-Optimized Event Details**
```
For each event, provide these ICS-critical details:
- title: Event name (for SUMMARY field)
- description: Rich 2-3 sentence description (for DESCRIPTION field)
- start_local/end_local: Precise timing in America/Detroit timezone
- location: Full venue name and address (for LOCATION field)
- organizer: Contact name/email if available (for ORGANIZER field)
- url: Direct registration/info link (for URL field)
- uid: Unique identifier for calendar systems
- cost: Exact price with currency or "Free"
- registration_required: Boolean for advance planning
- capacity_limited: Boolean for urgency indicators
- accessibility_notes: Any accommodation information mentioned
```

#### 2. **Scoring-Optimized Analysis**
```
For each event, analyze these scoring factors:
- intensity_level: 1-5 scale (1=passive viewing, 5=intensive workshop)
- social_type: "networking"|"passive"|"interactive"|"presentation"
- learning_format: "lecture"|"hands-on"|"discussion"|"performance"|"exhibition"
- venue_tier: "tier1"|"tier2"|"tier3" based on prestige/quality
- speaker_quality: "keynote"|"expert"|"local"|"student"|"unknown"
- follow_up_potential: 1-5 scale for ongoing engagement opportunities
- seasonal_fit: "indoor"|"outdoor"|"weather_dependent"
- time_preference_match: Score 0.0-1.0 for ideal time window alignment
```

#### 3. **Preference Integration Depth**
```
PREFERENCE ALIGNMENT ANALYSIS:
Travel Distance Classification:
- Calculate travel time from Ann Arbor, MI
- Classify as: near (<15min), local (15-30min), far (30-45min), too_far (>45min)
- Apply scoring: near (+0.05), local (+0.02), far (-0.06), too_far (-0.12)

Budget Analysis:
- Classify cost as: free, low (<$25), medium ($25-75), high (>$75)
- Flag if exceeds weekly_spend_cap_usd: 150
- Note if qualifies for allow_overage_events_per_week budget

Category Quota Tracking:
- Map event to categories: career_tech, social_arts, outdoors_wellbeing, deep_networking
- Note which weekly minimums this event satisfies
- Consider variety vs quota fulfillment

Time Window Optimization:
- Check against preferred windows: weekdays 17:30-21:30, Sat 10:00-22:00, Sun 11:00-20:00
- Flag if conflicts with quiet_hours: 22:30-07:00
- Rate time preference match 0.0-1.0

Must-See Detection:
- Scan for keywords: keynote, Granholm, conference, summit, Climate Week, MSBC, Farrand
- Check against must_see_keywords in preferences
- Flag urgent_override_keywords: registration closing, last tickets, limited capacity
```

#### 4. **Enhanced Goal Keyword Integration**
```
DEEP GOAL ANALYSIS using these specific keywords:

Career Learning (weight: 0.25):
Keywords: data center, ai, machine learning, sustainability, climate, energy, entrepreneurship
Analysis: How directly does content relate to these topics? Score 0.0-1.0

Social Connection (weight: 0.2):
Keywords: networking, mixer, community, social, reception, meetup
Analysis: What networking opportunities exist? Rate interaction level 0.0-1.0

Wellbeing Fitness (weight: 0.15):
Keywords: wellbeing, mental health, fitness, yoga, run
Analysis: Physical or mental wellness component? Rate benefit 0.0-1.0

Outdoors Nature (weight: 0.1):
Keywords: outdoor, nature, farm, hike, garden
Analysis: Natural environment component? Rate outdoor engagement 0.0-1.0

For each goal category, provide:
- keyword_matches: List of matched keywords from content
- goal_alignment_score: 0.0-1.0 for how well event serves this goal
- alignment_rationale: 1-2 sentences explaining the connection
```

## 🚀 IMPLEMENTATION STRATEGY

### Step 1: Enhanced Prompt Template (30 minutes)
Replace the current basic prompt with comprehensive version including:
- All ICS-required fields
- Complete scoring factor analysis
- Deep preference integration
- Enhanced goal keyword processing

### Step 2: Preference Loading Enhancement (15 minutes)
```python
# In _build_prompt method, load complete preferences:
preferences = load_preferences()
travel_bins = preferences.get('travel', {}).get('bins', [])
time_windows = preferences.get('time_windows', {})
budget_caps = preferences.get('budgets', {})
quotas = preferences.get('quotas', {})
must_see_keywords = preferences.get('categories', {}).get('must_see_keywords', [])
```

### Step 3: Enhanced JSON Schema (10 minutes)
Update expected response format to include all new fields:
- ICS-optimized fields
- Scoring analysis fields
- Preference alignment scores
- Goal analysis breakdown

### Step 4: Validation Enhancement (10 minutes)
Update `_parse_response` to validate new required fields and ensure completeness.

## 📋 EXACT PROMPT REPLACEMENT

**REPLACE CURRENT LINES 88-132 in `src/research/llm_agent.py` with:**

```python
def _build_prompt(self, source: Dict[str, Any], horizon_days: int, *, context: str = "") -> str:
    horizon_limit = (datetime.now(DEFAULT_TIMEZONE).date() + timedelta(days=horizon_days)).isoformat()
    today = datetime.now(DEFAULT_TIMEZONE).date().isoformat()

    # Load comprehensive preferences
    try:
        preferences = load_preferences()
        goal_weights = preferences.get('weights', {}).get('goals', {})
        travel_bins = preferences.get('travel', {}).get('bins', [])
        time_windows = preferences.get('time_windows', {})
        budget_caps = preferences.get('budgets', {})
        quotas = preferences.get('quotas', {})
        categories = preferences.get('categories', {})
        must_see_keywords = categories.get('must_see_keywords', [])
    except Exception:
        goal_weights = {}
        travel_bins = []
        time_windows = {}
        budget_caps = {}
        quotas = {}
        must_see_keywords = []

    lines = [
        "You are an expert event curator for Spiceflow Social, analyzing REAL evening events in Ann Arbor, Michigan.",
        "Extract complete event details for Apple Calendar integration and sophisticated scoring analysis.",
        "",
        "CRITICAL RULES:",
        "- ONLY return events that actually exist on the source website",
        "- NEVER create fake, inferred, or plausible events",
        "- Events must have dates in 2025 (current year)",
        f"- Events must occur between {today} and {horizon_limit}",
        "- Focus on evening events (typically 17:00-22:00)",
        "",
        "FOR EACH REAL EVENT, EXTRACT COMPLETE DETAILS:",
        "",
        "== ICS CALENDAR FIELDS ==",
        "- title: Exact event name from source",
        "- description: Rich 2-3 sentence description for calendar",
        "- start_local: Precise start time (America/Detroit timezone, ISO format)",
        "- end_local: Precise end time or estimated duration if not stated",
        "- location: Full venue name and address (street, city, state, zip if available)",
        "- url: Direct link to event page or registration",
        "- organizer: Contact name/email/phone if mentioned",
        "- cost: Exact price with $ symbol or 'Free'",
        "- registration_required: true/false for advance registration needed",
        "- capacity_limited: true/false if limited seating/tickets mentioned",
        "- accessibility_notes: Any wheelchair/accommodation info mentioned",
        "",
        "== SCORING ANALYSIS FIELDS ==",
        "- intensity_level: 1-5 scale (1=passive viewing, 5=intensive workshop)",
        "- social_type: 'networking'|'passive'|'interactive'|'presentation'",
        "- learning_format: 'lecture'|'hands-on'|'discussion'|'performance'|'exhibition'",
        "- venue_tier: 'tier1'|'tier2'|'tier3' (tier1=prestigious venues like Rackham)",
        "- speaker_quality: 'keynote'|'expert'|'local'|'student'|'unknown'",
        "- follow_up_potential: 1-5 scale for networking/ongoing engagement opportunities",
        "- seasonal_fit: 'indoor'|'outdoor'|'weather_dependent'",
        "",
        "== PREFERENCE ALIGNMENT ==",
        f"Travel Distance Analysis (from Ann Arbor, MI):",
        json.dumps(travel_bins, indent=2) if travel_bins else "Standard distance analysis",
        "- travel_minutes: Estimated travel time from downtown Ann Arbor",
        "- travel_category: 'near'|'local'|'far'|'too_far' based on minutes",
        "",
        f"Budget Analysis (weekly cap: ${budget_caps.get('weekly_spend_cap_usd', 150)}):",
        "- budget_category: 'free'|'low'|'medium'|'high' (low <$25, medium $25-75, high >$75)",
        "- exceeds_weekly_budget: true/false if over weekly cap",
        "",
        f"Time Window Preferences:",
        json.dumps(time_windows, indent=2) if time_windows else "Evening preference analysis",
        "- time_preference_match: 0.0-1.0 score for optimal time alignment",
        "",
        "== DEEP GOAL ANALYSIS ==",
        f"Goal Weights: {json.dumps(goal_weights, indent=2) if goal_weights else 'Equal weighting'}",
        "",
        "For each goal category, analyze:",
        "CAREER LEARNING (keywords: ai, machine learning, sustainability, climate, energy, entrepreneurship):",
        "- career_keyword_matches: List specific matched keywords from content",
        "- career_alignment_score: 0.0-1.0 for professional development value",
        "- career_rationale: Why this advances career goals",
        "",
        "SOCIAL CONNECTION (keywords: networking, mixer, community, social, reception, meetup):",
        "- social_keyword_matches: List specific matched keywords",
        "- social_alignment_score: 0.0-1.0 for networking/relationship value",
        "- social_rationale: What social opportunities exist",
        "",
        "WELLBEING FITNESS (keywords: wellbeing, mental health, fitness, yoga, run):",
        "- wellbeing_keyword_matches: List specific matched keywords",
        "- wellbeing_alignment_score: 0.0-1.0 for wellness benefit",
        "- wellbeing_rationale: Physical or mental health component",
        "",
        "OUTDOORS NATURE (keywords: outdoor, nature, farm, hike, garden):",
        "- outdoors_keyword_matches: List specific matched keywords",
        "- outdoors_alignment_score: 0.0-1.0 for nature engagement",
        "- outdoors_rationale: Natural environment component",
        "",
        "== MUST-SEE DETECTION ==",
        f"Must-See Keywords: {must_see_keywords}",
        "- must_see: true only if contains must-see keywords or exceptional speaker/content",
        "- must_see_rationale: Why this is exceptional (keynote speaker, rare opportunity, etc.)",
        "",
        "== CATEGORY QUOTAS ==",
        f"Weekly Quotas: {json.dumps(quotas.get('weekly', {}), indent=2) if quotas else 'Standard variety'}",
        "- quota_categories: List which quotas this event helps fulfill",
        "- novelty_score: 0.0-1.0 based on uniqueness vs typical offerings",
        "",
        f"SOURCE INFORMATION:",
        f"- Source URL: {source.get('url', 'unknown')}",
        f"- Source Name: {source.get('name', 'unknown')}",
        f"- Expected Category: {source.get('category', 'general')}",
    ]

    if context:
        lines.extend([
            "",
            "WEBSITE CONTENT TO ANALYZE:",
            "=" * 50,
            context[:8000],  # Increased from 5000 for richer analysis
            "=" * 50
        ])
    else:
        lines.append("WEBSITE CONTENT: (no page content available)")

    lines.extend([
        "",
        "RESPONSE FORMAT: Return JSON with 'summary' and 'events' array.",
        "Each event must include ALL fields specified above.",
        "Empty events array if no real events found in date range.",
        "STRICT JSON only (no markdown, no prose)."
    ])

    return "\n".join(lines)
```

## 🎯 EXPECTED RESULTS

### Enhanced Event Discovery:
- **ICS Compatibility:** Perfect Apple Calendar integration with rich details
- **Scoring Precision:** All factors needed for sophisticated optimization
- **Preference Alignment:** Deep integration with personal criteria
- **Goal Analysis:** Detailed breakdown for each goal category

### Quality Improvements:
- **Venue Details:** Full addresses and contact information
- **Registration Info:** Clear advance planning requirements
- **Accessibility:** Accommodation details for inclusive planning
- **Budget Tracking:** Precise cost analysis and cap monitoring
- **Time Optimization:** Exact preference window matching

## ⚠️ CRITICAL SUCCESS METRICS & VALIDATION

**After implementing enhanced prompt, verify:**
1. **Zero Hallucinations:** NO "inferred", "realistic suggestions", or fake events in ANY outputs
2. **Real Events Only:** All events must exist on source websites with correct 2025 dates
3. **ICS Quality:** Events import perfectly with rich descriptions
4. **Scoring Data:** All scoring factors populated for every event
5. **Preference Integration:** Travel, budget, time analysis complete

**Test Command:**
```bash
SPICEFLOW_LLM_PROVIDER=gemini python src/run_all.py --use-llm-research --horizon-days 7
```

**CRITICAL VALIDATION STEPS:**
1. **Hallucination Check:** Scan ALL `data/research/*.json` files for "inferred" or fake events
2. **Date Validation:** Ensure NO events have 2024 or incorrect dates
3. **Reality Check:** Manually verify 2-3 discovered events exist on their source websites
4. **Field Completeness:** Check new scoring and preference fields are populated
5. **ICS Testing:** Import winners.ics into calendar and verify rich details

**RED FLAGS TO WATCH FOR:**
- Any events with dates outside 2025
- Language like "inferred", "plausible", "realistic suggestion"
- Events that don't appear on the actual source website
- Generic venue names like "Dana Building" without verification

## 🚀 IMMEDIATE ACTION REQUIRED

**PRIORITY: CRITICAL**

1. **Fix Anti-Hallucination System:** Current filtering is incomplete and unreliable
2. **Implement Enhanced Prompt:** Add all ICS and scoring requirements
3. **Add Stronger Validation:** Catch ALL fake events, not just some
4. **Test Thoroughly:** Verify every claim before declaring success

**The Sprint Summary #2 "zero hallucinations" claim is INCORRECT. The system still produces fake events intermittently. This must be fixed before any production use.**