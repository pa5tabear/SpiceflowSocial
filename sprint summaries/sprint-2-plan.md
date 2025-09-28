# Sprint #2 Plan — High-Quality LLM Research Pipeline Activation

**Date:** 2025-09-28
**Lead Programmer:** Claude Code (Codex)
**Sprint Coach Directive:** Sprint Coaching Advice #5
**Duration:** 1 Week (Focused Single Deliverable)

## SINGULAR FOCUS MANDATE

**ONE DELIVERABLE ONLY:** Create a perfect `data/out/weekly_llm_research.md` file that demonstrates high-quality LLM event discovery with actual web browsing capability.

**CRITICAL SUCCESS GATE:** No other work begins until this deliverable is production-perfect.

---

## Sprint Objectives

### PRIMARY OBJECTIVE (100% Sprint Focus)
**DELIVERABLE:** `data/out/weekly_llm_research.md`
- **Success Criteria:** LLM demonstrates actual website content analysis
- **Technical Proof:** Gemini 2.5 Pro with full web access working
- **Quality Gate:** Events include details only available from live web browsing
- **Business Value:** Automated event discovery beyond scraper capabilities

### SUPPORTING DELIVERABLE
**ARTIFACT:** `data/out/winners.ics`
- **Success Criteria:** Working calendar file ready for import
- **Quality Gate:** Contains events discovered via LLM research
- **Business Value:** Immediate calendar integration for discovered events

---

## Technical Implementation Plan

### Phase 1: LLM Configuration Enhancement (Day 1)

#### Task 1.1: Upgrade to Gemini 2.5 Pro Model
- **Current State:** Using `models/gemini-2.5-flash` (basic model)
- **Target State:** Configure `models/gemini-2.5-pro` for high-quality research
- **Implementation:** Update `SPICEFLOW_GEMINI_MODEL` environment variable
- **Verification:** API calls show Pro model in request logs

#### Task 1.2: Enable High Token Output Configuration
- **Current State:** Default token limits may truncate responses
- **Target State:** Configure for detailed, comprehensive research responses
- **Implementation:** Review and adjust max_output_tokens in Gemini client
- **Verification:** LLM responses show full event analysis (not truncated)

#### Task 1.3: Verify Web Access Tools Integration
- **Current State:** Context fetcher exists but web browsing tools unclear
- **Target State:** LLM can access live website content during research
- **Implementation:** Enable Gemini web browsing/search capabilities
- **Verification:** LLM responses reference current website content

### Phase 2: Pipeline Execution & Validation (Days 2-3)

#### Task 2.1: Execute High-Quality Research Run
- **Command:** `SPICEFLOW_LLM_PROVIDER=gemini python src/run_all.py --use-llm-research --horizon-days 7`
- **Environment:** Network-enabled environment (not sandboxed)
- **Monitoring:** Log API calls and response quality
- **Output:** Generate `data/research/*.json` with rich content

#### Task 2.2: Generate Weekly Research Markdown
- **Implementation:** Create new `src/emit/weekly_research_markdown.py`
- **Content:** Aggregate LLM research into human-readable summary
- **Format:** Structured markdown with event analysis and discovery insights
- **Integration:** Add to main pipeline run

#### Task 2.3: Validate Calendar Output Quality
- **Verification:** `data/out/winners.ics` contains LLM-discovered events
- **Testing:** Import ICS file into test calendar environment
- **Quality Check:** Events include rich details from web research

### Phase 3: Quality Assurance & Documentation (Days 4-5)

#### Task 3.1: Content Quality Validation
- **Manual Review:** Examine research markdown for depth and accuracy
- **Technical Check:** Verify events contain details not in source metadata
- **Comparison:** Side-by-side with previous scraper-only results
- **Success Metric:** Clear evidence of web browsing and analysis

#### Task 3.2: Performance & Cost Monitoring
- **API Usage:** Track Gemini token consumption and costs
- **Performance:** Measure research pipeline execution time
- **Logging:** Comprehensive debugging output for troubleshooting
- **Documentation:** Update README with LLM research capabilities

---

## Technical Configuration Requirements

### Gemini API Configuration
```bash
# Environment Variables
export SPICEFLOW_LLM_PROVIDER=gemini
export SPICEFLOW_GEMINI_MODEL=models/gemini-2.5-pro
export GEMINI_API_KEY=[configured in data/secrets/secrets.md]

# Enable web browsing tools
# Configure max_output_tokens for comprehensive responses
# Ensure network access for live content fetching
```

### Pipeline Execution Commands
```bash
# Primary research run
python src/run_all.py --use-llm-research --llm-overwrite --horizon-days 7

# Verify API connectivity
python -c "from src.research.llm_agent import LLMResearchClient; client = LLMResearchClient(provider='gemini'); print('API Ready:', not client.dry_run)"

# Debug output locations
ls -la data/research/
ls -la data/out/
```

---

## Success Criteria & Validation

### PRIMARY SUCCESS METRICS

#### 1. **LLM Web Browsing Evidence**
- ✅ Research markdown contains website-specific details
- ✅ Event descriptions include content not in source metadata
- ✅ LLM responses reference current website layout/content
- ✅ API logs show successful web content retrieval

#### 2. **Research Quality Indicators**
- ✅ Events include venue details, registration requirements, prerequisites
- ✅ Analysis shows understanding of event context and goals alignment
- ✅ Discovery of events not found by scrapers
- ✅ Rich event descriptions with compelling rationale

#### 3. **Technical Integration Success**
- ✅ Gemini 2.5 Pro model confirmed in API calls
- ✅ High token limits allowing comprehensive responses
- ✅ Context fetcher properly feeding LLM prompts
- ✅ No truncated or incomplete research responses

#### 4. **Pipeline Output Quality**
- ✅ `weekly_llm_research.md` shows professional-grade analysis
- ✅ `winners.ics` contains actionable calendar events
- ✅ Events demonstrate clear goal alignment scoring
- ✅ Research insights inform future source prioritization

### FAILURE CRITERIA (STOP AND FIX)
- ❌ LLM returns empty events or generic placeholders
- ❌ Research responses appear to use only metadata (no web content)
- ❌ API calls fail or show basic model usage
- ❌ Network access issues prevent live content fetching

---

## Anti-Roadmap (DO NOT BUILD)

### Explicitly Deferred Until LLM Research Works:
- ❌ Source health dashboards
- ❌ Performance monitoring systems
- ❌ Additional event scrapers
- ❌ OAuth calendar integrations
- ❌ Obsidian export scripts
- ❌ Mobile workflow implementation
- ❌ Alert or notification systems

### Rationale:
**The LLM research markdown must be production-perfect before ANY other development work begins.** This ensures the core value proposition is proven before expanding surface area.

---

## Risk Mitigation

### HIGH RISK: API Configuration Issues
- **Risk:** Gemini API not properly configured for web access
- **Mitigation:** Test API connectivity and web browsing capabilities first
- **Contingency:** Debug API configuration before pipeline execution

### MEDIUM RISK: Network Access Restrictions
- **Risk:** Execution environment blocks web requests
- **Mitigation:** Verify network access in non-sandboxed environment
- **Contingency:** Test context fetcher independently

### LOW RISK: Token Costs
- **Risk:** High-quality research consumes significant API tokens
- **Mitigation:** Monitor usage and set reasonable limits
- **Contingency:** Implement batch processing for cost optimization

---

## Definition of Done

### Sprint Complete When:
1. ✅ `data/out/weekly_llm_research.md` demonstrates clear web browsing evidence
2. ✅ Research quality shows significant improvement over scraper-only results
3. ✅ `data/out/winners.ics` ready for production calendar import
4. ✅ Technical configuration documented and reproducible
5. ✅ API usage and costs measured and documented
6. ✅ No truncated or placeholder research responses

### Success Validation:
- **Human Review:** Product leadership approves research markdown quality
- **Technical Test:** ICS import works in production calendar
- **Process Test:** Pipeline run reproducible without manual intervention

---

## Sprint Retrospective Setup

### Key Questions for Review:
1. Does the LLM research show clear evidence of web browsing capability?
2. Are discovered events higher quality than scraper-only results?
3. Is the research markdown ready for daily production use?
4. What API costs and performance characteristics were observed?
5. What technical or product blockers emerged?

### Success Metrics to Track:
- Event discovery rate (LLM vs scraper)
- Research quality scores (depth, accuracy, relevance)
- API token usage and costs
- Pipeline execution time
- User satisfaction with research insights

---

**SPRINT COMMITMENT:** One perfect deliverable showcasing high-quality LLM event discovery with actual web research capabilities. No scope creep until this foundation is rock-solid.