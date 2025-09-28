# Sprint #3 Plan — Critical Prompt Enhancement & Production Optimization

**Date:** 2025-09-28
**Lead Programmer:** Claude Code (Codex)
**Sprint Coach Directive:** Sprint Coaching Advice #8 - Critical Prompt Enhancement
**Duration:** 2-3 Hours (Emergency Critical Fixes)
**Priority:** 🚨 **CRITICAL** - Production blocker discovered

## 🚨 CRITICAL ISSUES IDENTIFIED

### **Sprint Summary #2 Claims PARTIALLY FALSE**
**VERIFICATION REVEALS:** Current anti-hallucination system is **unreliable** and still producing fake events intermittently.

**EVIDENCE FOUND:**
- `data/research/wege_lecture_2025-2025-09-28T19-17-56Z.json` contains **FAKE EVENTS**
- Events with 2024 dates when searching 2025 range
- LLM admits to creating "realistic, inferred events aligned with themes"
- Current filtering system **FAILED** to catch these hallucinated events

**IMMEDIATE THREAT:** System is inconsistent - sometimes works, sometimes hallucinates. **NOT production-ready**.

---

## Sprint Objectives

### 🔥 **CRITICAL PRIORITY 1: Complete Anti-Hallucination Fix**
**TARGET:** Achieve **TRUE ZERO** hallucinations across ALL runs, not just some

#### Sub-objectives:
1. **Enhanced Prompt Rewrite** - Replace existing prompt with bulletproof anti-hallucination version
2. **Stronger Validation** - Catch ALL fake events, not just obvious ones
3. **Consistent Quality** - Ensure reliable performance across all pipeline runs
4. **Verification System** - Comprehensive testing to validate claims

### 🎯 **CRITICAL PRIORITY 2: Production-Grade Prompt Enhancement**
**TARGET:** Complete ICS compatibility and sophisticated scoring integration

#### Sub-objectives:
1. **ICS Calendar Fields** - All fields needed for perfect Apple Calendar integration
2. **Scoring Analysis** - Complete factor analysis for optimization algorithm
3. **Preference Integration** - Deep integration with travel, budget, time, quota preferences
4. **Goal Analysis** - Detailed breakdown for each goal category with keyword matching

### 📊 **SUPPORTING PRIORITY 3: Enhanced Output Quality**
**TARGET:** Professional-grade event discovery with rich metadata

#### Sub-objectives:
1. **Venue Details** - Full addresses, contact information, accessibility notes
2. **Registration Intelligence** - Advance planning requirements, capacity limits
3. **Budget Tracking** - Precise cost analysis with weekly cap monitoring
4. **Time Optimization** - Exact preference window matching and scoring

---

## Technical Implementation Plan

### 🚨 **PHASE 1: EMERGENCY ANTI-HALLUCINATION FIX (60 minutes)**

#### Task 1.1: Completely Replace Prompt (30 minutes)
**FILE:** `src/research/llm_agent.py` lines 88-132
**REPLACE WITH:** Enhanced prompt from Sprint Coaching Advice #8

**KEY CHANGES:**
- Remove ALL language that encourages inference
- Add explicit "NEVER create fake events" warnings
- Strengthen "REAL EVENTS ONLY" messaging
- Add validation instructions within prompt

#### Task 1.2: Enhanced Preference Loading (15 minutes)
**IMPLEMENTATION:**
```python
# Load complete preferences structure:
preferences = load_preferences()
travel_bins = preferences.get('travel', {}).get('bins', [])
time_windows = preferences.get('time_windows', {})
budget_caps = preferences.get('budgets', {})
quotas = preferences.get('quotas', {})
must_see_keywords = preferences.get('categories', {}).get('must_see_keywords', [])
```

#### Task 1.3: Stronger Validation Enhancement (15 minutes)
**FILE:** `src/research/llm_agent.py` `_parse_response` method

**ADD VALIDATION FOR:**
- All events with 2024 dates
- Any mention of "inferred", "realistic", "plausible", "suggested", "example"
- Events with generic venues not verified in content
- Events missing required fields (location, time, etc.)

### 🎯 **PHASE 2: PRODUCTION-GRADE PROMPT IMPLEMENTATION (90 minutes)**

#### Task 2.1: ICS Calendar Fields Integration (30 minutes)
**ADD TO PROMPT:**
- `title` - Exact event name for SUMMARY field
- `description` - Rich 2-3 sentence description for DESCRIPTION field
- `location` - Full venue name and address for LOCATION field
- `organizer` - Contact information for ORGANIZER field
- `registration_required` - Boolean for advance planning
- `capacity_limited` - Boolean for urgency indicators
- `accessibility_notes` - Accommodation information

#### Task 2.2: Scoring Analysis Fields (30 minutes)
**ADD TO PROMPT:**
- `intensity_level` - 1-5 scale (passive to intensive)
- `social_type` - networking|passive|interactive|presentation
- `learning_format` - lecture|hands-on|discussion|performance|exhibition
- `venue_tier` - tier1|tier2|tier3 (prestige classification)
- `speaker_quality` - keynote|expert|local|student|unknown
- `follow_up_potential` - 1-5 scale for ongoing engagement
- `seasonal_fit` - indoor|outdoor|weather_dependent

#### Task 2.3: Deep Preference Integration (30 minutes)
**ADD TO PROMPT:**
- **Travel Analysis:** Distance classification with scoring (near/local/far/too_far)
- **Budget Analysis:** Cost categorization with weekly cap checking
- **Time Window:** Preference match scoring against optimal windows
- **Category Quotas:** Weekly minimum tracking and variety analysis
- **Must-See Detection:** Keyword scanning for exceptional events

### 📊 **PHASE 3: GOAL ANALYSIS ENHANCEMENT (45 minutes)**

#### Task 3.1: Goal Keyword Integration (25 minutes)
**IMPLEMENT DETAILED ANALYSIS FOR:**

**CAREER LEARNING (weight: 0.25):**
- Keywords: ai, machine learning, sustainability, climate, energy, entrepreneurship
- Output: career_keyword_matches, career_alignment_score, career_rationale

**SOCIAL CONNECTION (weight: 0.2):**
- Keywords: networking, mixer, community, social, reception, meetup
- Output: social_keyword_matches, social_alignment_score, social_rationale

**WELLBEING FITNESS (weight: 0.15):**
- Keywords: wellbeing, mental health, fitness, yoga, run
- Output: wellbeing_keyword_matches, wellbeing_alignment_score, wellbeing_rationale

**OUTDOORS NATURE (weight: 0.1):**
- Keywords: outdoor, nature, farm, hike, garden
- Output: outdoors_keyword_matches, outdoors_alignment_score, outdoors_rationale

#### Task 3.2: Enhanced JSON Schema (10 minutes)
**UPDATE EXPECTED RESPONSE FORMAT:**
- All new ICS fields
- All scoring analysis fields
- All preference alignment scores
- Complete goal analysis breakdown

#### Task 3.3: Response Validation (10 minutes)
**UPDATE `_parse_response`:**
- Validate all new required fields present
- Ensure completeness of analysis
- Check field format compliance

### 🧪 **PHASE 4: COMPREHENSIVE TESTING & VALIDATION (30 minutes)**

#### Task 4.1: Anti-Hallucination Verification (15 minutes)
**CRITICAL VALIDATION STEPS:**
1. Run full pipeline: `SPICEFLOW_LLM_PROVIDER=gemini python src/run_all.py --use-llm-research --horizon-days 7`
2. Scan ALL `data/research/*.json` files for hallucination keywords
3. Verify ALL events have 2025 dates
4. Manually check 2-3 events exist on source websites
5. Confirm NO "inferred" or "plausible" language anywhere

#### Task 4.2: Enhanced Output Quality Verification (15 minutes)
**QUALITY CHECKS:**
1. All events have complete ICS fields
2. Scoring analysis fields populated
3. Preference alignment calculated
4. Goal analysis detailed and specific
5. ICS file imports perfectly into calendar

---

## Exact Code Implementation

### 🔧 **COMPLETE PROMPT REPLACEMENT**

**REPLACE LINES 88-132 in `src/research/llm_agent.py` WITH:**

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

    return "\\n".join(lines)
```

### 🛡️ **ENHANCED VALIDATION REPLACEMENT**

**ENHANCE `_parse_response` method:**

```python
# Add after line 169 in current _parse_response method:
# Enhanced hallucination detection
for event in events:
    # Skip events with wrong year
    start_date = event.get("start_local", "")
    if start_date.startswith("2024") or start_date.startswith("2023") or start_date.startswith("2026"):
        continue

    # Skip events that mention inference/plausible/fake indicators
    all_text = " ".join([
        str(event.get("notes", "")),
        str(event.get("description", "")),
        str(event.get("title", "")),
        str(event.get("career_rationale", "")),
        str(event.get("social_rationale", "")),
    ]).lower()

    hallucination_keywords = [
        "inferred", "plausible", "suggested", "example", "realistic suggestion",
        "likely", "probable", "estimated event", "typical", "might", "could be",
        "potentially", "presumably", "hypothetical"
    ]

    if any(keyword in all_text for keyword in hallucination_keywords):
        continue

    # Require essential fields
    if not event.get("title") or not event.get("start_local") or not event.get("location"):
        continue

    validated_events.append(event)
```

---

## Critical Success Criteria

### 🚨 **ABSOLUTE REQUIREMENTS (MUST PASS ALL)**

#### 1. **ZERO Hallucinations Verification**
- ✅ NO events with dates outside 2025
- ✅ NO language containing "inferred", "plausible", "realistic suggestion"
- ✅ ALL events must exist on source websites (manual verification of 3 events)
- ✅ NO generic venue names without source verification

#### 2. **ICS Integration Quality**
- ✅ Perfect Apple Calendar import with rich descriptions
- ✅ Complete location information (venue + address)
- ✅ Proper timezone handling (America/Detroit)
- ✅ Registration and accessibility information included

#### 3. **Scoring System Completeness**
- ✅ All scoring fields populated for every event
- ✅ Goal analysis detailed with specific keyword matches
- ✅ Preference alignment calculated (travel, budget, time)
- ✅ Must-see detection working for exceptional events

#### 4. **Production Reliability**
- ✅ Consistent quality across multiple pipeline runs
- ✅ No intermittent hallucination issues
- ✅ All error cases handled gracefully
- ✅ Comprehensive logging for debugging

### 🧪 **VALIDATION PROTOCOL**

#### Immediate Testing Commands:
```bash
# Full pipeline test
SPICEFLOW_LLM_PROVIDER=gemini python src/run_all.py --use-llm-research --horizon-days 7

# Hallucination scan
grep -r "inferred\|plausible\|realistic suggestion" data/research/*.json

# Date validation
grep -r "2024-\|2023-\|2026-" data/research/*.json

# Field completeness check
python -c "
import json, glob
for f in glob.glob('data/research/*.json'):
    with open(f) as file:
        data = json.load(file)
        for event in data.get('events', []):
            required = ['title', 'start_local', 'location', 'intensity_level', 'social_type']
            missing = [field for field in required if not event.get(field)]
            if missing: print(f'{f}: Missing {missing}')
"
```

#### Manual Verification Steps:
1. **Open** 3 random events from `data/research/*.json`
2. **Visit** their source websites
3. **Confirm** events actually exist with correct details
4. **Import** `data/out/winners.ics` into calendar
5. **Verify** rich descriptions and complete information

---

## Risk Assessment & Mitigation

### 🔴 **HIGH RISK: Hallucination Detection Failure**
- **Risk:** Enhanced prompt still allows some fake events through
- **Mitigation:** Multi-layer validation (prompt + code + manual verification)
- **Contingency:** Revert to scraper-only mode if LLM unreliable

### 🟡 **MEDIUM RISK: Performance Degradation**
- **Risk:** Enhanced prompt increases token usage and response time
- **Mitigation:** Monitor API costs and response times during testing
- **Contingency:** Optimize prompt length while maintaining quality

### 🟢 **LOW RISK: Preference Integration Complexity**
- **Risk:** Complex preference loading causes errors
- **Mitigation:** Comprehensive error handling with fallback defaults
- **Contingency:** Gradual rollout of preference features

---

## Definition of Done

### Sprint Complete When:
1. ✅ **ZERO hallucinations** verified across multiple pipeline runs
2. ✅ **Complete ICS integration** with all required fields
3. ✅ **Full scoring system** with goal analysis and preference alignment
4. ✅ **Production reliability** demonstrated through consistent quality
5. ✅ **Comprehensive testing** validates all claims
6. ✅ **Enhanced weekly research markdown** reflects new capabilities

### Success Validation Checklist:
- [ ] Run pipeline 3 times, scan all outputs for hallucination keywords
- [ ] Manually verify 5 discovered events exist on source websites
- [ ] Import winners.ics and confirm perfect calendar integration
- [ ] Verify all scoring fields populated with meaningful values
- [ ] Check preference alignment calculations working correctly
- [ ] Confirm goal analysis provides specific keyword matches

---

## 🚀 Sprint Execution Strategy

### **EMERGENCY SPRINT APPROACH:**
- **Focus:** Fix critical hallucination issue FIRST
- **Verification:** Test every change immediately
- **Quality Gate:** No advancement without validation
- **Documentation:** Update claims only after verification

### **ANTI-PATTERN PREVENTION:**
- **NO** declaring success without comprehensive testing
- **NO** assuming previous fixes are still working
- **NO** rushing implementation without validation
- **NO** generic claims without specific evidence

**This sprint transforms the system from "sometimes works" to "reliably excellent" - the difference between prototype and production.**

---

**BOTTOM LINE:** Sprint #2 claimed "zero hallucinations" but evidence shows this is false. Sprint #3 must achieve TRUE zero hallucinations through bulletproof prompt engineering and comprehensive validation. No shortcuts. No assumptions. Verify everything.