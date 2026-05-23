# Autonomous Execution Flow

This document describes how Codex orchestrates the 4-phase web security testing workflow with autonomous decision-making and minimal user intervention.

---

## Workflow Entry Points

### Entry Point 1: Full Automated Assessment

```
User Input: "Audit https://target.com for vulnerabilities"
            ↓
Codex checks scope, confirms authorization
            ↓
Runs ALL phases: 1 → 2 → 3 → 4
            ↓
Generates full report
```

### Entry Point 2: Focused Phase Execution

```
User Input: "Run Phase 2 passive scanning on endpoint inventory from Phase 1"
            ↓
Codex loads previous Phase 1 output
            ↓
Starts at Phase 2 with known endpoints
            ↓
Continues through remaining phases
```

### Entry Point 3: Single Phase

```
User Input: "Validate this SQL injection finding"
            ↓
Codex runs Phase 3 validation only
            ↓
Returns classification and evidence
```

---

## Phase 1: Autonomous Execution

### Codex Flow

```
START PHASE 1
  ├─ Read scope.md (if present)
  ├─ Read .github/instructions/memory.md (if present)
  │
  ├─ STAGE: Subdomain Discovery
  │  ├─ Query passive DNS APIs
  │  ├─ Test each for HTTP(S) availability
  │  └─ Store: hosts_inventory.json
  │
  ├─ STAGE: Application Mapping
  │  ├─ Crawl HTML structure (Playwright)
  │  ├─ Extract all links and forms
  │  ├─ Download all JavaScript files
  │  ├─ Extract API endpoints from JS
  │  └─ Store: endpoints_inventory.json
  │
  ├─ STAGE: JavaScript Analysis
  │  ├─ Analyze for DOM XSS patterns
  │  ├─ Extract hidden endpoints (admin, debug)
  │  ├─ Detect SSRF sink patterns
  │  └─ Store: js_analysis.json
  │
  ├─ STAGE: Input Discovery
  │  ├─ Fuzz common parameter names
  │  ├─ Extract form input fields
  │  ├─ Build parameter matrix
  │  └─ Store: parameters_matrix.json
  │
  ├─ STAGE: Quick Checks
  │  ├─ Test unauthenticated access
  │  ├─ Check CORS configuration
  │  ├─ Scan for common files (.env, swagger.json)
  │  └─ Store: quick_checks.json
  │
  ├─ GATE 1: Coverage Check
  │  ├─ Detected endpoints: {{ endpoint_count }}
  │  └─ Decision:
  │     ├─ If >10 endpoints: "PASS - Continue to Phase 2"
  │     ├─ If 5-10 endpoints: "PASS (partial) - Continue with caution"
  │     └─ If <5 endpoints: "FAIL - Expand crawling"
  │
  └─ END PHASE 1
```

### Decision Logic

```python
def phase_1_complete():
    endpoints = len(load("endpoints_inventory.json"))
    parameters = len(load("parameters_matrix.json"))
    js_files = len(load("js_analysis.json"))
    
    confidence = (
        (endpoints > 10) * 0.5 +
        (parameters > 5) * 0.25 +
        (js_files > 0) * 0.25
    )
    
    if confidence > 0.7:
        return "CONTINUE_PHASE_2"
    elif confidence > 0.4:
        return "ASK_USER: Low coverage, continue anyway?"
    else:
        return "EXPAND_PHASE_1: More endpoints needed"
```

### User Interaction Points

```
OPTIONAL: User reviews endpoint map
          ├─ Approve and continue
          ├─ Add manual endpoints
          └─ Mark endpoints as out-of-scope

OPTIONAL: User provides credentials
          └─ Codex tests authenticated endpoints
```

---

## Phase 2: Autonomous Execution

### Codex Flow

```
START PHASE 2
  ├─ Load endpoints from Phase 1
  │
  ├─ STAGE: Passive Pattern Matching
  │  ├─ Scan all responses for:
  │  │  ├─ API keys / secrets (regex patterns)
  │  │  ├─ Internal IPs (10.x, 172.x, 192.x)
  │  │  ├─ Stack traces (Python, Node, .NET)
  │  │  ├─ Database errors (MySQL, Postgres, etc)
  │  │  ├─ Version information (headers, banners)
  │  │  └─ Debug flags (debug=true, DEBUG mode)
  │  │
  │  └─ Store: passive_findings.json
  │
  ├─ STAGE: SQL Injection Scanning
  │  ├─ For each endpoint with parameters:
  │  │  ├─ Send: id=1
  │  │  ├─ Send: id=1 AND 1=1
  │  │  ├─ Send: id=1 AND 1=2
  │  │  ├─ Compare response sizes and content
  │  │  ├─ Flag if boolean-based pattern detected
  │  │  └─ Rate confidence (low/medium/high)
  │  │
  │  └─ Store: sqli_candidates.json
  │
  ├─ STAGE: XSS Scanning (Reflected)
  │  ├─ For each parameter:
  │  │  ├─ Send: xss_test_<img src=x>
  │  │  ├─ Check if unencoded in response
  │  │  ├─ Flag if reflection detected
  │  │  └─ Rate confidence
  │  │
  │  └─ Store: xss_candidates.json
  │
  ├─ STAGE: Authorization Scanning
  │  ├─ For each resource endpoint:
  │  │  ├─ Send with Auth A
  │  │  ├─ Send with Auth B
  │  │  ├─ Send with no auth
  │  │  ├─ Flag if inconsistent access control
  │  │  └─ Rate confidence
  │  │
  │  └─ Store: authz_candidates.json
  │
  ├─ STAGE: SSRF Scanning
  │  ├─ For endpoints with URL parameters:
  │  │  ├─ Send: http://localhost:8080/admin
  │  │  ├─ Send: http://169.254.169.254/metadata
  │  │  ├─ Check for internal responses
  │  │  └─ Rate confidence
  │  │
  │  └─ Store: ssrf_candidates.json
  │
  ├─ STAGE: Business Logic Scanning
  │  ├─ For state-changing endpoints:
  │  │  ├─ Test: negative quantities
  │  │  ├─ Test: price manipulation
  │  │  ├─ Test: duplicate coupon usage
  │  │  └─ Rate confidence
  │  │
  │  └─ Store: logic_candidates.json
  │
  ├─ STAGE: Aggregate & Prioritize
  │  ├─ Merge all candidate files
  │  ├─ Sort by confidence
  │  ├─ Filter by severity potential
  │  └─ Store: findings_candidates.json (top 10)
  │
  ├─ GATE 2: Candidate Check
  │  ├─ Viable candidates found: {{ count }}
  │  └─ Decision:
  │     ├─ If >2 high-confidence: "CONTINUE_PHASE_3"
  │     ├─ If 1-2 medium-confidence: "ASK_USER: Low confidence, continue?"
  │     └─ If 0: "NO_CANDIDATES: Expand scanning parameters"
  │
  └─ END PHASE 2
```

### Confidence Scoring

```python
def score_candidate(endpoint, test_results):
    confidence = 0
    
    # SQL Injection confidence
    if test_results.get('response_delta') > 0.5:
        confidence += 0.3
    if test_results.get('error_detected'):
        confidence += 0.2
    if test_results.get('timing_difference') > 0.5:
        confidence += 0.2
    
    # XSS confidence
    if test_results.get('unencoded_reflection'):
        confidence += 0.4
    if test_results.get('context') == 'javascript':
        confidence += 0.1
    
    # Authorization confidence
    if test_results.get('cross_user_access'):
        confidence += 0.5
    if test_results.get('no_auth_required'):
        confidence += 0.3
    
    return min(confidence, 1.0)
```

---

## Phase 3: Autonomous Execution

### Codex Flow

```
START PHASE 3
  ├─ Load top candidates from Phase 2
  │
  ├─ FOR EACH candidate (sorted by confidence):
  │  │
  │  ├─ CANDIDATE: SQL Injection
  │  │  ├─ VALIDATE STEP 1: Confirm reachability
  │  │  │  ├─ Send normal request → status 200?
  │  │  │  └─ Decision: CONTINUE if yes, SKIP if no
  │  │  │
  │  │  ├─ VALIDATE STEP 2: Boolean-based confirmation
  │  │  │  ├─ Send: id=1 AND 1=1
  │  │  │  ├─ Send: id=1 AND 1=2
  │  │  │  ├─ Compare responses
  │  │  │  ├─ If delta: REPRODUCED_FINDING
  │  │  │  └─ Store: finding_sql_001.json
  │  │  │
  │  │  ├─ VALIDATE STEP 3: Impact measurement
  │  │  │  ├─ Try UNION-based extraction (safe payload)
  │  │  │  ├─ Document data types exposed
  │  │  │  └─ Measure risk: CRITICAL
  │  │  │
  │  │  └─ CLASSIFICATION: REPRODUCED_FINDING (HIGH confidence)
  │  │
  │  ├─ CANDIDATE: Authorization Bypass
  │  │  ├─ VALIDATE STEP 1: Establish baseline
  │  │  │  ├─ User A access own resource → 200
  │  │  │  └─ Document fields returned
  │  │  │
  │  │  ├─ VALIDATE STEP 2: Cross-user test
  │  │  │  ├─ User A access User B resource
  │  │  │  ├─ Compare responses
  │  │  │  ├─ If user B data leaked: REPRODUCED_FINDING
  │  │  │  └─ Store: finding_authz_001.json
  │  │  │
  │  │  └─ CLASSIFICATION: REPRODUCED_FINDING (HIGH confidence)
  │  │
  │  ├─ CANDIDATE: Reflected XSS
  │  │  ├─ VALIDATE STEP 1: Confirm reflection
  │  │  │  ├─ Send: xss_marker_<img src=x>
  │  │  │  ├─ Check if unencoded in response
  │  │  │  └─ Decision: CONTINUE if yes, SUPPRESS if no
  │  │  │
  │  │  ├─ VALIDATE STEP 2: Execution via browser
  │  │  │  ├─ Load page in Playwright
  │  │  │  ├─ Check console for JS errors/execution
  │  │  │  ├─ If executed: REPRODUCED_FINDING
  │  │  │  └─ Store: finding_xss_001.json
  │  │  │
  │  │  └─ CLASSIFICATION: REPRODUCED_FINDING (MEDIUM confidence)
  │  │
  │  └─ [Continue for other candidates...]
  │
  ├─ STAGE: Consolidate Results
  │  ├─ Count reproduced findings: {{ count }}
  │  ├─ Count suppressed findings: {{ count }}
  │  ├─ Merge into: validated_findings.json
  │  └─ Generate: validation_report.json
  │
  ├─ GATE 3: Validation Check
  │  ├─ Confirmed findings: {{ count }}
  │  └─ Decision:
  │     ├─ If >1 reproduced: "CONTINUE_PHASE_4"
  │     ├─ If 1 reproduced: "CONTINUE_PHASE_4"
  │     └─ If 0: "NO_CONFIRMED_FINDINGS: Assessment complete with no issues"
  │
  └─ END PHASE 3
```

### Validation Decision Tree

```
For each candidate:
  │
  ├─ Can we reach the endpoint? 
  │  ├─ NO → SKIP
  │  └─ YES → Continue
  │
  ├─ Can we trigger the vulnerable behavior?
  │  ├─ NO → SUPPRESS (false positive)
  │  └─ YES → Continue
  │
  ├─ Is the behavior exploitable?
  │  ├─ NO → SUPPRESS (mitigated by framework)
  │  └─ YES → Continue
  │
  ├─ Can we measure impact?
  │  ├─ NO → UNVERIFIED_SUSPICION
  │  └─ YES → REPRODUCED_FINDING
  │
  └─ CLASSIFY: reproduced_finding / suppressed / unverified_suspicion
```

---

## Phase 4: Autonomous Execution

### Codex Flow

```
START PHASE 4
  ├─ Load validated findings from Phase 3
  │
  ├─ STAGE: Format Findings
  │  ├─ For each finding:
  │  │  ├─ Generate title
  │  │  ├─ Extract POC
  │  │  ├─ Document root cause
  │  │  ├─ Calculate severity (CVSS)
  │  │  ├─ Write remediation steps
  │  │  └─ Add references
  │  │
  │  └─ Store: findings_formatted.json
  │
  ├─ STAGE: Generate Reports
  │  ├─ Executive Summary (1 page)
  │  │  ├─ Severity breakdown
  │  │  ├─ Top 3 findings
  │  │  ├─ Remediation priority
  │  │  └─ Output: EXECUTIVE_SUMMARY.md
  │  │
  │  ├─ Detailed Report
  │  │  ├─ Full POC for each finding
  │  │  ├─ Root cause analysis
  │  │  ├─ Code examples (vulnerable + secure)
  │  │  └─ Output: DETAILED_REPORT.md
  │  │
  │  └─ Remediation Roadmap
  │     ├─ Priority-ordered fixes
  │     ├─ Timeline estimates
  │     └─ Output: REMEDIATION_ROADMAP.md
  │
  ├─ STAGE: Export Formats
  │  ├─ Markdown (for humans)
  │  ├─ JSON (for tools)
  │  ├─ CSV (for tracking)
  │  └─ Output: findings.json, findings.csv
  │
  ├─ STAGE: Distribution
  │  ├─ Store in: security-reports/
  │  ├─ Mark timestamp
  │  └─ Generate index.md
  │
  └─ END PHASE 4
      OUTPUT: Full assessment report ready for stakeholder delivery
```

---

## End-to-End Timeline Example

```
USER INPUT: "Assess target.com"
│
├─ 14:00 → START
│
├─ 14:05 → PHASE 1: Recon/Fuzz/Crawl
│  │       ├─ Found 42 endpoints
│  │       ├─ Extracted 156 parameters
│  │       ├─ Analyzed 12 JS files
│  │       └─ GATE 1: PASS ✓
│  │
│  └─ 14:20 → [Update user] "Phase 1 complete, starting Phase 2..."
│
├─ 14:20 → PHASE 2: Passive/Active Scanning
│  │       ├─ Pattern matches: 8 candidates
│  │       │  - SQL Injection: 2 (high confidence)
│  │       │  - Authorization: 1 (high confidence)
│  │       │  - XSS: 2 (medium confidence)
│  │       │  - SSRF: 1 (low confidence)
│  │       │  - Other: 2 (low confidence)
│  │       └─ GATE 2: PASS ✓
│  │
│  └─ 14:45 → [Update user] "Phase 2 complete, starting Phase 3..."
│
├─ 14:45 → PHASE 3: Validating Issues
│  │       ├─ Testing 8 candidates
│  │       │  - SQL Injection #1: REPRODUCED ✓
│  │       │  - SQL Injection #2: REPRODUCED ✓
│  │       │  - Authorization: REPRODUCED ✓
│  │       │  - XSS #1: REPRODUCED ✓
│  │       │  - XSS #2: SUPPRESSED (HTML-encoded)
│  │       │  - SSRF: SUPPRESSED (no service on port)
│  │       │  - Others: INCONCLUSIVE
│  │       │
│  │       └─ Final: 4 reproduced findings
│  │       └─ GATE 3: PASS ✓
│  │
│  └─ 15:10 → [Update user] "Phase 3 complete, generating reports..."
│
├─ 15:10 → PHASE 4: Reporting
│  │       ├─ Generating executive summary
│  │       ├─ Generating detailed reports
│  │       ├─ Generating remediation roadmap
│  │       └─ Exporting to JSON/CSV
│  │
│  └─ 15:15 → COMPLETE ✓
│
└─ 15:15 → USER OUTPUT:
           ├─ EXECUTIVE_SUMMARY.md
           ├─ DETAILED_REPORT.md
           ├─ REMEDIATION_ROADMAP.md
           ├─ findings.json
           └─ findings.csv

TOTAL TIME: 15 minutes (fully autonomous)
FINDINGS: 4 confirmed vulnerabilities (2 critical, 1 high, 1 medium)
```

---

## Decision Override Points

At each gate, user can override Codex decisions:

```
GATE 1 (Phase 1 → Phase 2)
├─ If Codex says "Not enough endpoints"
└─ User says "Continue anyway" → Proceed to Phase 2

GATE 2 (Phase 2 → Phase 3)
├─ If Codex says "Only 1 low-confidence candidate"
└─ User says "Validate it anyway" → Proceed to Phase 3 with that candidate

GATE 3 (Phase 3 → Phase 4)
├─ If Codex says "No findings confirmed"
└─ User says "Generate report anyway" → Creates "No Issues Found" report
```

---

## Autonomous Mode Settings

Users can customize Codex behavior:

```yaml
autonomy_settings:
  confidence_threshold: 0.7  # Only test candidates above this
  timeout_per_request: 5     # Seconds per HTTP request
  max_parallel_requests: 10  # Concurrent testing
  rate_limit_delay: 0.1      # Seconds between requests
  stop_on_first_finding: false  # Continue testing or stop?
  
  phase_skipping:
    skip_phase_1: false      # If user provides endpoints
    skip_phase_2: false      # If user provides candidates
    skip_phase_3: false      # If user only wants report
    skip_phase_4: false      # If user only wants metrics

  output_formats:
    markdown: true
    json: true
    csv: true
    html: false

  decision_gates:
    ask_on_gate_1: true      # Ask before proceeding to Phase 2?
    ask_on_gate_2: false     # Auto-proceed if candidates found
    ask_on_gate_3: true      # Ask before proceeding to Phase 4?
```

---

## Error Handling & Backoff

If Codex encounters issues:

```
SCENARIO 1: Rate Limiting Detected (429)
├─ Action: Back off, increase request delays
├─ Retry: After 60 seconds
└─ Report: "Rate limiting detected, slowing down..."

SCENARIO 2: Authentication Expired
├─ Action: Stop testing authenticated endpoints
├─ Report: "Session expired, continuing with unauthenticated testing"
└─ Decision: Continue or abort?

SCENARIO 3: Endpoint Crashes (500)
├─ Action: Skip that endpoint, move to next
├─ Report: "Target endpoint unavailable (500), skipping..."
└─ Decision: Mark as DoS vector?

SCENARIO 4: Out-of-Scope Trigger (e.g., admin login page)
├─ Action: Stop immediately
├─ Report: "Out-of-scope endpoint detected, aborting..."
└─ Decision: User confirms safe to continue?
```

---

## Success Criteria

Assessment is deemed successful when:

```
Phase 1:
  ✓ Endpoint inventory complete (>10 endpoints or user approval)
  ✓ Parameter matrix built (>5 parameters or user approval)

Phase 2:
  ✓ Pattern scanning complete (all endpoints tested)
  ✓ Candidates prioritized (top 10 flagged)

Phase 3:
  ✓ Validation complete for each candidate
  ✓ Classification assigned (reproduced/suppressed/inconclusive)

Phase 4:
  ✓ All reports generated in requested formats
  ✓ Findings ready for stakeholder delivery
```

---

## Quick Commands

```bash
# Start full assessment
codex assess https://target.com

# Resume from Phase 2 (using Phase 1 output)
codex phase-2 --endpoints endpoints_inventory.json

# Validate specific finding
codex validate-finding --type sql-injection --endpoint "/api/users?id="

# Generate report only
codex report --findings validated_findings.json --format markdown,json

# Dry run (show commands without executing)
codex assess https://target.com --dry-run
```

---

End of autonomous execution flow documentation.
