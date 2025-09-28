# Sprint Coaching Advice #6 — CRITICAL LLM Research Fixes

**Prepared by:** Codex (Product Manager & Sprint Coach)
**Date:** 2025-09-28
**URGENT:** Fix broken LLM research system producing fake events

## 🚨 CRITICAL ISSUES DISCOVERED

The LLM research system is **fundamentally broken** and producing hallucinated events instead of real research. Current outputs show:
- **Fake events** with wrong dates (2024-06-06 when today is 2025-09-28)
- **No web access** - Gemini isn't actually browsing websites
- **Dry-run placeholders** instead of real API calls
- **Empty content fetching** from most sources

## 🎯 MANDATORY FIXES (DO THESE FIRST)

### Fix #1: Enable Live API Mode
**Problem:** System running in dry-run mode, not calling Gemini API

**IMMEDIATE ACTION:**
```bash
# Run this exact command to test live API:
SPICEFLOW_LLM_PROVIDER=gemini SPICEFLOW_GEMINI_ENABLE_SEARCH=1 python src/run_all.py --use-llm-research --horizon-days 7
```

**Verification:**
- Check `data/research/*.json` files show `"provider": "gemini"` instead of `"status": "dry-run"`
- Confirm API calls in logs, not placeholder text

### Fix #2: Enable Gemini Web Search
**Problem:** Gemini has no web access despite having search capabilities

**CODE FIX REQUIRED:**
```python
# In src/research/llm_agent.py, line 164-165, ALWAYS enable search tools:
payload["tools"] = [{"googleSearchRetrieval": {}}]
# Remove the conditional check that keeps it disabled
```

**Environment Variable:**
```bash
export SPICEFLOW_GEMINI_ENABLE_SEARCH=1
```

### Fix #3: Fix Context Fetching Failures
**Problem:** Most sources show "(no page content available)"

**DEBUG STEPS:**
1. Test context fetcher directly:
   ```python
   from src.research.context_fetcher import fetch_context_for_source
   test_source = {"url": "https://events.umich.edu/event/138552"}
   result = fetch_context_for_source(test_source)
   print(f"Length: {len(result)}, Content: {result[:200]}")
   ```

2. Check for 403/blocking issues in `util/http_cache.py`
3. Add User-Agent headers if needed
4. Verify network connectivity

### Fix #4: Completely Rewrite Prompt
**Problem:** Current prompt encourages hallucination

**NEW PROMPT TEMPLATE:**
```
You are a research assistant for Spiceflow Social, finding REAL evening events in Ann Arbor, Michigan.

CRITICAL RULES:
- ONLY return events that actually exist on the source website
- NEVER create fake or inferred events
- If no real events found, return empty events array
- Use web search to find additional event details if needed

Search the provided source for ACTUAL upcoming events between {today} and {horizon_limit}.

For each REAL event found, extract:
- title: Exact event name from source
- start_local: Actual start time in ISO format (America/Detroit timezone)
- end_local: Actual end time or start + 90 minutes
- location: Real venue address
- url: Direct link to event page
- cost: Actual price or "Free" if stated
- category: {source_category}
- tags: Relevant keywords from content
- fit_rationale: Why this aligns with goals: {goal_weights}
- novelty_score: 0.0-1.0 based on uniqueness
- travel_minutes: Estimated from Ann Arbor
- must_see: true only if exceptional/keynote speaker
- notes: Key details from source

GOAL ALIGNMENT PRIORITIES:
{include actual preferences.yaml weights here}

Source to research: {url}
Content: {webpage_content}

Return JSON with summary and events array. Empty events array if no real events found.
```

### Fix #5: Include Real Preferences
**Problem:** Prompt ignores actual goal weights and preferences

**IMPLEMENTATION:**
```python
# In _build_prompt method, add:
preferences = load_preferences()  # from util/preferences.py
goal_weights = preferences.get('weights', {}).get('goals', {})
prompt_parts.append(f"Goal priorities: {json.dumps(goal_weights)}")
```

## 🔧 TECHNICAL IMPLEMENTATION STEPS

### Step 1: Verify API Credentials (5 minutes)
```bash
# Check if API key exists:
grep "gemini_api_key" data/secrets/secrets.md

# Test basic API connectivity:
curl -H "Authorization: Bearer YOUR_KEY" \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
```

### Step 2: Enable Web Search (10 minutes)
```python
# Edit src/research/llm_agent.py line 164:
# OLD:
if os.getenv("SPICEFLOW_GEMINI_ENABLE_SEARCH", "0") == "1":
    payload["tools"] = [{"googleSearchRetrieval": {}}]

# NEW:
payload["tools"] = [{"googleSearchRetrieval": {}}]
```

### Step 3: Fix Context Fetching (15 minutes)
```python
# Add to util/http_cache.py:
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}
# Include headers in all requests
```

### Step 4: Replace Prompt (20 minutes)
```python
# Rewrite _build_prompt method to:
1. Load actual preferences from preferences.yaml
2. Include goal weights in prompt
3. Remove hallucination encouragement
4. Add strict "real events only" instructions
5. Include web search directive
```

### Step 5: Add Validation (10 minutes)
```python
# In _parse_response, add checks:
if "inferred" in event.get("notes", "").lower():
    continue  # Skip fake events
if event.get("start_local", "").startswith("2024"):
    continue  # Skip wrong year events
```

## 📋 VERIFICATION CHECKLIST

**After fixes, verify:**
- [ ] `SPICEFLOW_LLM_PROVIDER=gemini` runs without dry-run messages
- [ ] `data/research/*.json` shows `"provider": "gemini"`
- [ ] API calls visible in logs with actual responses
- [ ] Context fetcher returns >1000 chars for most sources
- [ ] Events have current year dates (2025-10-xx)
- [ ] No "inferred" or "plausible" events in outputs
- [ ] Goal weights from preferences.yaml appear in prompts

## 🎯 SUCCESS CRITERIA

**DELIVERABLE: Working LLM Research Markdown**
- Run: `SPICEFLOW_LLM_PROVIDER=gemini SPICEFLOW_GEMINI_ENABLE_SEARCH=1 python src/run_all.py --use-llm-research --horizon-days 7`
- Verify: `data/out/research_summary.md` shows real events with actual dates
- Confirm: Events match what's actually on source websites
- Validate: No hallucinated events in any outputs

## ⚠️ ANTI-PATTERNS TO AVOID

**DO NOT:**
- Skip API credential verification
- Leave dry-run mode enabled
- Allow hallucinated events in outputs
- Ignore context fetching failures
- Use environment variables that default to disabled

**DO:**
- Test each fix incrementally
- Verify real web content fetching
- Validate event authenticity against source websites
- Include actual preferences in prompts
- Enable all Gemini capabilities (search, high token count)

## 🚀 IMMEDIATE NEXT ACTIONS

1. **[5 min]** Verify Gemini API key configured and accessible
2. **[10 min]** Enable web search tools permanently in code
3. **[15 min]** Debug and fix context fetching for UM sources
4. **[20 min]** Rewrite prompt to eliminate hallucination
5. **[10 min]** Add preferences integration
6. **[10 min]** Test full pipeline and verify real events

**Total time to fix: ~70 minutes of focused development work**

Once these fixes are complete, the LLM research system will produce high-quality, real event discovery instead of hallucinated placeholders. This is the foundation needed for the training data you want.