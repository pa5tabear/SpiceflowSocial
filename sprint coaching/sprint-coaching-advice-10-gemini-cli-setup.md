# Sprint Coaching Advice #10 — Gemini CLI Integration Setup

**Prepared by:** Codex (Product Manager & Sprint Coach)
**Date:** 2025-09-28
**Task:** Set up Google Gemini CLI for enhanced LLM research capabilities

## 🎯 OBJECTIVE

Set up the official Google Gemini CLI to potentially enhance or replace the current custom Gemini API integration in the LLM research pipeline.

**GitHub Repository:** https://github.com/google-gemini/gemini-cli

## 📋 SETUP INSTRUCTIONS

### Step 1: Install Gemini CLI (10 minutes)

**Method 1: Direct Installation**
```bash
# Install via npm (requires Node.js)
npm install -g @google/generative-ai-cli

# Or install via pip if Python distribution available
pip install google-generativeai-cli
```

**Method 2: Clone and Build**
```bash
# Clone the repository
git clone https://github.com/google-gemini/gemini-cli.git
cd gemini-cli

# Install dependencies and build
npm install
npm run build
npm link  # Make globally available
```

### Step 2: Configure Authentication (5 minutes)

**Set up API key (same as current system):**
```bash
# Option 1: Environment variable
export GEMINI_API_KEY="your_api_key_here"

# Option 2: CLI configuration
gemini auth login
# Follow prompts to configure API key

# Option 3: Config file
gemini config set api-key "your_api_key_here"
```

**Verify setup:**
```bash
gemini --version
gemini models list  # Should show available models
```

### Step 3: Test Basic Functionality (10 minutes)

**Simple test:**
```bash
# Test basic chat
echo "What is 2+2?" | gemini chat

# Test with specific model
echo "Analyze this text for events" | gemini chat --model gemini-2.5-pro

# Test file input
echo "Find events in this content" > test.txt
gemini chat --file test.txt --model gemini-2.5-pro
```

### Step 4: Integration Assessment (15 minutes)

**Compare with current implementation:**

**Current System (`src/research/llm_agent.py`):**
```python
# Direct HTTP API calls
response = client.post(url, params={"key": self._api_key}, json=payload)
```

**Potential CLI Integration:**
```python
import subprocess
result = subprocess.run([
    'gemini', 'chat',
    '--model', 'gemini-2.5-pro',
    '--input', prompt_text
], capture_output=True, text=True)
```

## 🔍 EVALUATION CRITERIA

### Advantages of Gemini CLI:
- ✅ **Official Google tool** - Better maintenance and updates
- ✅ **Built-in features** - May include search, file handling, etc.
- ✅ **Standardized interface** - Consistent with Google's tooling
- ✅ **Advanced options** - Potentially more configuration options

### Current System Advantages:
- ✅ **Direct control** - Custom error handling and retry logic
- ✅ **Integration depth** - Embedded in Python pipeline
- ✅ **Working reliably** - Current system is functional
- ✅ **Custom validation** - Anti-hallucination filters in place

## 🎯 INTEGRATION STRATEGY

### Phase 1: Parallel Testing (This Week)

**Create test script to compare outputs:**

```python
# File: src/research/gemini_cli_test.py
import subprocess
from research.llm_agent import LLMResearchClient

def test_gemini_cli_vs_current(test_source, test_context):
    """Compare CLI vs current API for same source"""

    # Current system
    current_client = LLMResearchClient(provider="gemini")
    current_result = current_client.summarize_source(test_source, horizon_days=7, context=test_context)

    # CLI system
    prompt = build_prompt_for_cli(test_source, test_context)
    cli_result = subprocess.run([
        'gemini', 'chat',
        '--model', 'gemini-2.5-pro',
        '--input', prompt
    ], capture_output=True, text=True)

    return {
        'current': current_result,
        'cli': parse_cli_response(cli_result.stdout),
        'comparison': compare_results(current_result, cli_result)
    }
```

### Phase 2: Feature Assessment (Next Week)

**Test CLI-specific features:**
- File upload capabilities
- Search integration options
- Model configuration flexibility
- Error handling and retry mechanisms

### Phase 3: Decision Point (Week After)

**Evaluation criteria:**
1. **Quality:** Does CLI produce better event discovery?
2. **Reliability:** Is error handling as robust as current system?
3. **Integration:** How easily does it integrate with existing pipeline?
4. **Maintenance:** Does it reduce or increase system complexity?

## 🚀 IMPLEMENTATION OPTIONS

### Option A: Replace Current System
**If CLI proves superior:**
- Replace `src/research/llm_agent.py` with CLI-based implementation
- Migrate all prompt engineering to CLI format
- Update error handling and validation for CLI outputs

### Option B: Hybrid Approach
**If both have advantages:**
- Use CLI for initial content analysis
- Use current API for structured JSON responses
- Combine strengths of both approaches

### Option C: Keep Current System
**If CLI doesn't add value:**
- Document CLI evaluation results
- Continue with current proven implementation
- Monitor CLI development for future opportunities

## 📋 TESTING PROTOCOL

### Test Cases:
1. **Source Analysis:** Compare event discovery quality on same sources
2. **Error Handling:** Test with problematic content (empty pages, errors)
3. **Performance:** Measure response times and API usage
4. **Integration:** Test with current pipeline components
5. **Reliability:** Run extended tests for consistency

### Success Metrics:
- **Event Quality:** CLI finds same or better real events
- **Reliability:** <5% failure rate on known working sources
- **Performance:** Response time ≤ current system
- **Integration:** Works with existing validation and scoring
- **Maintenance:** Reduces system complexity

## ⚠️ RISK ASSESSMENT

### LOW RISKS:
- **Setup complexity** - Standard CLI installation
- **API compatibility** - Same underlying Gemini models
- **Feature parity** - CLI should match current capabilities

### MEDIUM RISKS:
- **Integration complexity** - May require significant pipeline changes
- **Error handling** - CLI error modes may differ from direct API
- **Performance** - Subprocess overhead vs direct HTTP calls

### MITIGATION:
- **Parallel testing** - Keep current system while evaluating CLI
- **Gradual migration** - Test one component at a time
- **Rollback plan** - Easy revert to current system if needed

## 🎯 IMMEDIATE NEXT ACTIONS

### For Programming Team (Next 2 Days):
1. **Install and configure** Gemini CLI following setup instructions
2. **Create comparison test** between CLI and current system
3. **Run basic functionality tests** to verify installation
4. **Document setup process** and any installation issues

### For Evaluation (Next Week):
1. **Compare output quality** on 5-10 test sources
2. **Test error scenarios** and edge cases
3. **Measure performance** and resource usage
4. **Assess integration complexity** with current pipeline

### For Decision Making (Following Week):
1. **Review test results** and comparison data
2. **Make integration decision** based on evaluation criteria
3. **Plan migration strategy** if CLI proves beneficial
4. **Document decision rationale** for future reference

## 💡 STRATEGIC CONSIDERATIONS

### Why This Makes Sense Now:
- **Current system working** - No urgency, can evaluate properly
- **Official tooling** - Google's CLI may have advantages we're missing
- **Future-proofing** - Official tools often get new features first
- **Best practices** - Using official tools often reduces maintenance

### Integration with Current Priorities:
- **Doesn't block** current sprint work on prompt optimization
- **Complements** goal of improving LLM research quality
- **Supports** reliability improvements by potentially offering better tooling
- **Aligns** with using best available tools for each component

---

**BOTTOM LINE:** Set up and evaluate Gemini CLI as a potential improvement to current LLM research capabilities, but don't disrupt working system until CLI proves clearly superior through systematic testing.