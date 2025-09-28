# Sprint #4 Plan — Comprehensive Production Optimization & Workflow Enhancement

**Date:** 2025-09-28
**Lead Programmer:** Claude Code (Codex)
**Sprint Coach Directives:**
- Sprint Coaching Advice #7 - Production Optimization & Scale
- Sprint Coaching Advice #8 - Critical Prompt Enhancement
- Sprint Coaching Advice #9 - ICS Workflow Optimization
**Duration:** 3-5 Days (Production Readiness Focus)
**Priority:** 🚀 **PRODUCTION** - Scale system from prototype to daily-use platform

## 📊 Current System Analysis

### ✅ **WHAT'S ALREADY WORKING:**
- **Single ICS file:** `data/out/winners.ics` contains only selected events (exactly what you want)
- **7-day window:** System uses `--horizon-days 7` for planning
- **Apple Calendar ready:** ICS format fully compatible
- **Portfolio selection:** Events are already curated, not just dumped

### 🔧 **OPTIMIZATION OPPORTUNITIES:**
- **Enhanced review workflow** for easy approval/disapproval
- **Daily rolling updates** instead of full regeneration
- **Change detection** for event modifications and cancellations
- **Goal tracking** with weekly quota monitoring

---

## Sprint Objectives - Multi-Track Approach

### 🚨 **CRITICAL TRACK A: Complete Anti-Hallucination Fix**
**URGENCY:** Critical issue from Coaching Advice #8
**TARGET:** Achieve TRUE zero hallucinations across all runs

#### Sub-objectives:
1. **Enhanced Prompt Replacement** - Bulletproof anti-hallucination version
2. **Complete ICS Integration** - All fields for perfect Apple Calendar
3. **Advanced Scoring System** - Full goal analysis and preference integration
4. **Ironclad Validation** - Catch ALL fake events reliably

### 🎯 **PRODUCTION TRACK B: Scale & Optimize**
**FOUNDATION:** Sprint Coaching Advice #7 - Production Optimization
**TARGET:** Transform from 4 events/week to 40+ events/week

#### Sub-objectives:
1. **Source Expansion** - Add 15+ new quality Ann Arbor sources
2. **Production Automation** - Daily automation with monitoring
3. **Performance Optimization** - API efficiency and cost management
4. **Quality Assurance** - Automated validation and health checks

### 🔄 **WORKFLOW TRACK C: Daily Usage Optimization**
**USER EXPERIENCE:** Sprint Coaching Advice #9 - ICS Workflow
**TARGET:** Seamless daily review and approval workflow

#### Sub-objectives:
1. **Enhanced Review Markdown** - Comprehensive approval system
2. **Rolling Update Logic** - Smart daily maintenance
3. **Change Detection** - Event modification tracking
4. **CLI Enhancement** - Streamlined commands

### 📊 **INTEGRATION TRACK D: System Cohesion**
**TARGET:** Ensure all tracks work together seamlessly

#### Sub-objectives:
1. **Unified Pipeline** - All enhancements integrated smoothly
2. **Performance Validation** - No regression from optimizations
3. **User Testing** - End-to-end workflow verification
4. **Documentation** - Complete usage and maintenance guides

---

## Technical Implementation Plan - Multi-Track Execution

### 🚨 **TRACK A: CRITICAL ANTI-HALLUCINATION FIX (Day 1-2)**

#### A1: Complete Prompt Enhancement (120 minutes)
**PRIORITY:** CRITICAL - Address Sprint Coaching Advice #8

**A1.1: Enhanced Prompt Replacement (60 minutes)**
**FILE:** `src/research/llm_agent.py` lines 88-132
**IMPLEMENTATION:** Replace with comprehensive prompt from Coaching Advice #8

**KEY ADDITIONS:**
- **ICS Calendar Fields:** title, description, location, organizer, registration_required, accessibility_notes
- **Scoring Analysis:** intensity_level, social_type, venue_tier, speaker_quality, follow_up_potential
- **Preference Integration:** travel_category, budget_category, time_preference_match
- **Goal Analysis:** Deep keyword matching for all 4 goal categories
- **Must-See Detection:** Keyword scanning and exceptional event identification

**A1.2: Enhanced Preference Loading (30 minutes)**
```python
# Load complete preferences structure
preferences = load_preferences()
travel_bins = preferences.get('travel', {}).get('bins', [])
time_windows = preferences.get('time_windows', {})
budget_caps = preferences.get('budgets', {})
quotas = preferences.get('quotas', {})
must_see_keywords = preferences.get('categories', {}).get('must_see_keywords', [])
```

**A1.3: Ironclad Validation System (30 minutes)**
**ENHANCE:** `_parse_response` method with comprehensive fake event detection

```python
# Enhanced hallucination detection
hallucination_keywords = [
    "inferred", "plausible", "suggested", "example", "realistic suggestion",
    "likely", "probable", "estimated event", "typical", "might", "could be",
    "potentially", "presumably", "hypothetical"
]
# Multi-field validation across title, description, notes, rationale
# Date validation for 2025 only
# Required field completeness checks
```

#### A2: Complete Testing & Validation (60 minutes)
**A2.1: Comprehensive Testing Protocol (30 minutes)**
```bash
# Test commands
SPICEFLOW_LLM_PROVIDER=gemini python src/run_all.py --use-llm-research --horizon-days 7
grep -r "inferred\|plausible\|realistic suggestion" data/research/*.json
grep -r "2024-\|2023-\|2026-" data/research/*.json
```

**A2.2: Manual Verification (30 minutes)**
- Verify 5 discovered events exist on source websites
- Import winners.ics and test Apple Calendar integration
- Validate all new scoring fields populated correctly

### 🎯 **TRACK B: PRODUCTION SCALE & OPTIMIZATION (Day 2-4)**

#### B1: Source Expansion (180 minutes)
**TARGET:** 15+ new quality Ann Arbor event sources

**B1.1: Source Research & Discovery (90 minutes)**
**NEW SOURCES TO ADD:**
- Ann Arbor District Library events
- Downtown Ann Arbor venues (UMMA, Ark, etc.)
- Community centers and recreation facilities
- Local theaters and performance venues
- Farmer's markets and outdoor events
- Networking and professional groups
- Fitness and wellness studios
- Cultural organizations and museums

**B1.2: Source Configuration (60 minutes)**
**UPDATE:** `src/sources.yaml` with new sources
**ADD:** Source-specific prompt hints and categorization
**INCLUDE:** Scraping frequency optimization for dynamic sources

**B1.3: Source Quality Analysis (30 minutes)**
**CREATE:** `src/emit/source_performance_report.py`
**GENERATE:** `data/out/source_performance_report.md`
**TRACK:** Event discovery success rate per source
**IDENTIFY:** Best performing source types and patterns

#### B2: Production Automation (120 minutes)
**TARGET:** Daily automation with monitoring and error handling

**B2.1: Daily Automation Script (60 minutes)**
**CREATE:** `scripts/daily_research.sh`
```bash
#!/bin/bash
# Nightly automation script
# Error handling and status reporting
# Timestamp-based research archives
# Email/notification on completion or failure
```

**B2.2: Performance Monitoring (30 minutes)**
**IMPLEMENT:** API usage and cost tracking
**MONITOR:** Source accessibility trends
**ALERT:** Significant drops in event discovery
**GENERATE:** Weekly performance summaries

**B2.3: Quality Assurance Automation (30 minutes)**
**AUTOMATE:** Event date validation (2025 only)
**CHECK:** Batch hallucination indicator scanning
**VERIFY:** ICS file validity before publishing
**FLAG:** Unusual patterns for human review

#### B3: System Optimization (90 minutes)
**B3.1: API Optimization (45 minutes)**
- Test batching multiple sources per API call
- Optimize token usage while maintaining quality
- Add retry logic for transient API failures
- Experiment with temperature settings

**B3.2: Performance Enhancement (45 minutes)**
- Add concurrent processing for source analysis
- Implement incremental updates for unchanged sources
- Create pipeline performance profiling
- Add memory usage optimization

### 🔄 **TRACK C: DAILY WORKFLOW OPTIMIZATION (Day 3-4)**

#### C1: Enhanced Review Workflow (90 minutes)

#### Task 1.1: Create Weekly Review Generator (60 minutes)
**FILE:** `src/emit/weekly_review.py`

**IMPLEMENTATION:**
```python
def write_weekly_review(selected_events, portfolio_data, availability, output_path):
    """Generate comprehensive weekly review markdown with approval workflow"""

    # Group events by day
    events_by_day = defaultdict(list)
    for event in selected_events:
        day = event["start_local"].split("T")[0]
        events_by_day[day].append(event)

    # Calculate goal fulfillment
    goal_progress = analyze_goal_fulfillment(selected_events, portfolio_data)

    # Generate daily breakdown with approval template
    daily_sections = []
    for offset in range(7):
        day = (datetime.now(DEFAULT_TIMEZONE).date() + timedelta(days=offset))
        day_key = day.isoformat()

        events = events_by_day.get(day_key, [])
        availability_info = availability.get(day_key, {})

        section = generate_day_section(day, events, availability_info)
        daily_sections.append(section)

    # Create comprehensive review
    lines = [
        f"# Weekly Event Review - {start_date} - {end_date}",
        f"**Status:** {len(selected_events)} events selected for next 7 days",
        f"**Last Updated:** {datetime.now(DEFAULT_TIMEZONE).strftime('%Y-%m-%d %H:%M %Z')}",
        f"**ICS File:** `data/out/winners.ics` (ready to import)",
        "",
        "## 📅 Daily Breakdown",
        "",
        *daily_sections,
        "",
        "## 🎯 Weekly Overview",
        *generate_goal_overview(goal_progress),
        "",
        "## 📝 Quick Edit Commands",
        generate_edit_commands(),
        "",
        "## 🔄 Tomorrow's Update Preview",
        generate_update_preview()
    ]

    output_path.write_text("\\n".join(lines))
```

#### Task 1.2: Day Section Generator (20 minutes)
**FUNCTION:** `generate_day_section(day, events, availability_info)`

**OUTPUT FORMAT:**
```markdown
### Monday, Sept 30
**✅ APPROVED** Powering Tomorrow: Clean Energy Future
- **When:** 5:30 PM - 7:00 PM
- **Where:** Rackham Auditorium, 915 E Washington St
- **Why Selected:** High-profile keynote (Jennifer Granholm), sustainability goal alignment
- **Score:** 1.88 (career: 0.9, social: 0.3, location: 0.0)
- **Actions:** [ ] Keep [ ] Modify [ ] Cancel

### Tuesday, Oct 1
**🔍 NEEDS REVIEW** No events currently selected
- **Suggestions:** Check for late-added events, consider backup options
- **Actions:** [ ] Find alternatives [ ] Keep open [ ] Add specific search
```

#### Task 1.3: Goal Progress Tracking (10 minutes)
**FUNCTION:** `analyze_goal_fulfillment(events, portfolio_data)`

**OUTPUT:**
- Career Learning: X/2+ events
- Social Connection: X/2+ events
- Outdoors/Wellbeing: X/1+ events
- Budget tracking against weekly cap
- Travel time distribution

### 🔄 **PHASE 2: Rolling Update Logic (120 minutes)**

#### Task 2.1: Previous Portfolio Loading (30 minutes)
**FILE:** `src/portfolio/rolling_updates.py`

**IMPLEMENTATION:**
```python
def load_previous_portfolio(portfolio_dir):
    """Load yesterday's portfolio for comparison"""
    yesterday = datetime.now(DEFAULT_TIMEZONE).date() - timedelta(days=1)
    portfolio_file = portfolio_dir / f"portfolio-{yesterday.isoformat()}.json"

    if portfolio_file.exists():
        return json.loads(portfolio_file.read_text())
    return None

def detect_changes(previous_events, new_events):
    """Detect cancellations, modifications, and new opportunities"""
    changes = {
        "cancelled": [],
        "modified": [],
        "new_better": [],
        "goal_adjustments": []
    }

    # Compare events by UID and detect changes
    # Analyze scoring improvements
    # Suggest goal rebalancing

    return changes
```

#### Task 2.2: Change Detection Algorithm (45 minutes)
**FUNCTIONALITY:**
- **Event Cancellations:** Detect when previously selected events no longer exist
- **Score Improvements:** Find better alternatives that appeared
- **Goal Rebalancing:** Suggest swaps to meet weekly quotas
- **Conflict Resolution:** Handle schedule conflicts

#### Task 2.3: Rolling Update Generator (45 minutes)
**FUNCTION:** `generate_rolling_update(previous_portfolio, new_events, changes)`

**FEATURES:**
- Preserve approved events from days 2-7
- Add new suggestions for day 8
- Flag changes requiring attention
- Maintain goal balance across week

### 📱 **PHASE 3: CLI Enhancement (60 minutes)**

#### Task 3.1: Add Rolling Update Mode (30 minutes)
**FILE:** `src/run_all.py`

**ADD CLI OPTIONS:**
```python
parser.add_argument("--rolling-update", action="store_true",
                   help="Daily rolling update mode (maintain existing selections)")
parser.add_argument("--full-refresh", action="store_true",
                   help="Full 7-day refresh mode (regenerate all selections)")

def main():
    args = parse_arguments()

    if args.rolling_update:
        # Load previous portfolio
        # Detect changes
        # Generate minimal updates
        # Preserve user approvals
    elif args.full_refresh or not previous_portfolio_exists():
        # Full regeneration
        # Fresh 7-day window
        # Complete goal analysis
```

#### Task 3.2: Change Summary Output (20 minutes)
**FUNCTIONALITY:**
- Print summary of daily changes
- Highlight events requiring attention
- Show goal progress status
- Provide import instructions

#### Task 3.3: Portfolio Archiving (10 minutes)
**FEATURE:**
- Save daily portfolios with timestamps
- Enable change tracking over time
- Support rollback if needed

### 🧪 **PHASE 4: Integration & Testing (45 minutes)**

#### Task 4.1: Pipeline Integration (20 minutes)
**INTEGRATE INTO `src/run_all.py`:**
```python
# After portfolio selection:
write_weekly_review(
    portfolio["selected"],
    portfolio,
    availability_summary,
    Path("data/out/weekly_review.md")
)

# Archive portfolio for change tracking
archive_portfolio(portfolio, Path("data/portfolios"))
```

#### Task 4.2: Quality Validation (15 minutes)
**VERIFY:**
- `winners.ics` contains only selected events
- `weekly_review.md` format works for LLM editing
- Rolling updates preserve user choices
- Goal tracking matches preferences

#### Task 4.3: Documentation Update (10 minutes)
**UPDATE README with new workflow:**
- Daily usage pattern
- Weekly planning cycle
- Edit command examples
- Troubleshooting guide

---

## Enhanced Workflow Design

### 📅 **DAILY USAGE PATTERN:**
```bash
# Morning routine (5 minutes)
python src/run_all.py --rolling-update --horizon-days 7

# Review changes
open data/out/weekly_review.md

# Edit if needed (using LLM)
# "Cancel [event] on [day]" or "Find [type] event for [day]"

# Import updated calendar
# Import data/out/winners.ics to Apple Calendar
```

### 📊 **WEEKLY PLANNING CYCLE:**
```bash
# Sunday reset
python src/run_all.py --full-refresh --horizon-days 7

# Comprehensive review
open data/out/weekly_review.md

# Bulk approve/modify
# Use LLM for efficient editing

# Set for the week
# Daily rolling updates will maintain plan
```

### 🎯 **APPROVAL WORKFLOW:**
**In `weekly_review.md`:**
- **✅ APPROVED** - Keep as selected
- **🔍 NEEDS REVIEW** - Requires decision
- **❌ CANCELLED** - Remove from calendar
- **🔄 MODIFIED** - Change time/details

---

## 🤝 PARALLEL DEVELOPMENT PLAN: GEMINI & CURSOR

**Objective:** Accelerate sprint completion by dividing tasks between Gemini and Cursor, allowing for parallel work on distinct tracks.

### 💬 **Message to Cursor**

*Hello Cursor,*

*To speed up development for Sprint #4, I've outlined a plan for us to work in parallel. I will focus on the core LLM, prompt engineering, and research tasks, which are my specialty. I've assigned the application logic, workflow implementation, and automation tasks to you.*

*Please review the division of labor below. My work on Track A and B (Source Expansion) will provide the high-quality, validated event data your workflow in Track C will consume. Before you begin Track C, please implement the foundational "Availability Stub" task, as the weekly review you'll generate needs to be aware of the user's free time.*

*Let's sync up if you have any questions. Our tracks are designed to be independent to minimize merge conflicts.*

*Best, Gemini*

---

### **Gemini's Sprint Plan (LLM & Research Focus)**

**Primary Owner:** Gemini

1.  **Track A: Complete Anti-Hallucination Fix**
    *   **A1: Complete Prompt Enhancement:** I will replace the existing prompt in `src/research/llm_agent.py` with the comprehensive version from Coaching Advice #8. This includes adding all fields for ICS, scoring, and preference integration.
    *   **A1.3: Ironclad Validation System:** I will enhance the `_parse_response` method to implement stricter validation, including keyword filtering, date validation, and required field checks to ensure no hallucinated events pass through.
    *   **A2: Comprehensive Testing & Validation:** I will run the pipeline, manually verify event authenticity, and ensure all new data fields are populated correctly.

2.  **Track B (Partial): Source Expansion**
    *   **B1: Source Research & Discovery:** I will research and identify 15+ new high-quality event sources in the Ann Arbor area.
    *   **B1.2: Source Configuration:** I will update `src/sources.yaml` with the new sources, including any specific prompt hints or categorization needed.

### **Cursor's Sprint Plan (Application & Workflow Focus)**

**Primary Owner:** Cursor

1.  **Track 0: Foundational Availability**
    *   **Task:** Implement the `data/availability_stub.json` as described in the main coaching memo.
    *   **Task:** Create `src/util/availability.py` to load the stub and expose free/busy windows. This is a prerequisite for Track C.

2.  **Track C: Daily Workflow Optimization**
    *   **C1: Enhanced Review Workflow:** You will create the `src/emit/weekly_review.py` file to generate the comprehensive `weekly_review.md` with the approval workflow, daily breakdown, and goal overview.
    *   **C2: Rolling Update Logic:** You will implement the logic for rolling updates in `src/portfolio/rolling_updates.py`, including loading the previous portfolio and detecting changes.
    *   **C3: CLI Enhancement:** You will add the `--rolling-update` and `--full-refresh` CLI options to `src/run_all.py` to manage the two distinct workflows.

3.  **Track B (Partial): Production Automation & Optimization**
    *   **B2.1: Daily Automation Script:** You will create the `scripts/daily_research.sh` script for automating the daily pipeline runs, including error handling.
    *   **B3.2: Performance Enhancement:** You will investigate and implement concurrent processing for source analysis to improve pipeline performance.

---

## Success Metrics & Validation - Multi-Track Targets

### 🚨 **TRACK A: ANTI-HALLUCINATION SUCCESS CRITERIA**

#### Zero Hallucination Validation:
- **✅ NO events with dates outside 2025**
- **✅ NO hallucination keywords** ("inferred", "plausible", etc.)
- **✅ ALL events verified** to exist on source websites (manual check of 5 events)
- **✅ CONSISTENT quality** across multiple pipeline runs

#### Enhanced Prompt Quality:
- **✅ Complete ICS fields** populated for every event
- **✅ Advanced scoring data** (intensity, social_type, venue_tier, etc.)
- **✅ Deep goal analysis** with keyword matching for all 4 categories
- **✅ Preference integration** (travel, budget, time alignment)

### 🎯 **TRACK B: PRODUCTION SCALE SUCCESS CRITERIA**

#### Event Discovery Expansion:
- **Target: 40+ events per week** (vs current ~4)
- **Target: 30+ active sources** (vs current 16)
- **Maintain: 90%+ source success rate**
- **Quality: High-scoring events across all goal categories**

#### Automation Reliability:
- **Daily runs complete successfully** 95%+ of time
- **Automated validation** catches all quality issues
- **Performance monitoring** tracks API costs and runtime
- **Error recovery** handles common failure modes

### 🔄 **TRACK C: WORKFLOW SUCCESS CRITERIA**

#### Daily Usage Efficiency:
- **<5 minutes daily review** time
- **Single file import** (`winners.ics`)
- **Easy LLM editing** via markdown
- **Minimal disruption** to approved events

#### Rolling Update Quality:
- **Preserve user approvals** across daily updates
- **Accurate change detection** for event modifications
- **Smart goal rebalancing** when events cancelled
- **Preview system** for tomorrow's changes

### 📊 **INTEGRATION SUCCESS CRITERIA**

#### System Cohesion:
- **All tracks work together** without conflicts
- **No performance regression** from enhancements
- **Unified CLI** supports all workflows
- **Complete documentation** for maintenance

#### Production Readiness:
- **End-to-end testing** validates complete workflow
- **User acceptance** confirmed through real usage
- **Monitoring coverage** for all critical components
- **Backup and recovery** procedures documented

### 📊 **TESTING PROTOCOL:**

#### Day 1 Testing:
```bash
# Generate initial 7-day plan
python src/run_all.py --full-refresh --horizon-days 7

# Verify outputs
ls data/out/winners.ics data/out/weekly_review.md

# Test ICS import
# Import winners.ics into test calendar
```

#### Day 2 Testing:
```bash
# Test rolling update
python src/run_all.py --rolling-update --horizon-days 7

# Verify preservation
# Check that Day 1 events remain unless changed

# Test change detection
# Manually modify a source and verify detection
```

#### Edit Workflow Testing:
```bash
# Test LLM editing
# Use weekly_review.md with approval/cancellation commands
# Verify changes reflected in next run
```

---

## Risk Assessment & Mitigation

### 🔴 **HIGH RISK: User Approval Loss**
- **Risk:** Rolling updates accidentally remove user-approved events
- **Mitigation:** Preserve approval status in portfolio archive
- **Contingency:** Manual restoration from previous day's portfolio

### 🟡 **MEDIUM RISK: Change Detection Accuracy**
- **Risk:** False positives in event change detection
- **Mitigation:** Conservative change flagging with manual review
- **Contingency:** Disable rolling updates if too many false alarms

### 🟢 **LOW RISK: CLI Complexity**
- **Risk:** Too many command options confuse usage
- **Mitigation:** Clear documentation and sensible defaults
- **Contingency:** Simplify to single command with smart detection

---

## Definition of Done

### Sprint Complete When:
1. ✅ **Enhanced review markdown** generates comprehensive daily breakdown
2. ✅ **Rolling update system** preserves approved events while adding new days
3. ✅ **Change detection** identifies event modifications and better alternatives
4. ✅ **CLI options** support both daily and weekly workflows
5. ✅ **Goal tracking** shows progress against weekly quotas
6. ✅ **ICS compatibility** maintains perfect Apple Calendar integration

### Quality Gates:
- [ ] Import `winners.ics` into Apple Calendar successfully
- [ ] Edit `weekly_review.md` with LLM and see changes reflected
- [ ] Run rolling update 3 consecutive days without losing approvals
- [ ] Verify goal tracking matches actual event selection
- [ ] Test change detection with sample event modifications

---

## 🚀 Immediate Next Actions

### **TODAY (2-3 hours):**
1. **Create `weekly_review.py`** with comprehensive markdown generation
2. **Test current ICS workflow** - import `winners.ics` into calendar
3. **Add basic rolling update logic** to `run_all.py`

### **TOMORROW (2-3 hours):**
1. **Implement change detection** algorithm
2. **Add CLI options** for rolling vs full refresh
3. **Test daily workflow** with real events

### **DAY 3 (1-2 hours):**
1. **Integration testing** across multiple days
2. **Documentation update** with new workflow
3. **User feedback** incorporation

---

**BOTTOM LINE:** Sprint #4 optimizes the already-working ICS generation for seamless daily usage. The current system produces the right file (`winners.ics`) - we're adding intelligent review, approval, and rolling update workflows to minimize daily maintenance while maximizing goal achievement.

**Focus:** User experience and workflow efficiency, not core functionality changes.