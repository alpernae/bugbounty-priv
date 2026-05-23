# Web Security Testing Phases Overview

This workflow orchestrates automated web application security testing across four phases with decision gates and autonomous execution.

## Quick Start

1. **Scope & Rules** → Use `scope-and-authorization.md`
2. **Phase 1: Recon, Fuzz & Crawl** → `phase-1-recon-fuzz-crawl.md`
3. **Phase 2: Passive & Active Scanning** → `phase-2-passive-active-scanning.md`
4. **Phase 3: Validating Issues** → `phase-3-validating-issues.md`
5. **Phase 4: Reporting** → `phase-4-reporting.md`

## Phase Summary

### Phase 1: Recon, Fuzz & Crawl
- **Goal**: Map attack surface, discover endpoints, fuzz parameters, extract client-side code
- **Outputs**: Endpoint inventory, parameter matrix, hidden URLs, JS dependencies
- **Time**: Quick (minutes to hours depending on size)
- **Risk**: Passive to low-activity (reads, observations, benign fuzzing)

### Phase 2: Passive & Active Scanning
- **Goal**: Run SAST patterns, check for common misconfigurations, identify suspicious patterns
- **Outputs**: Hypotheses, pattern matches, suspicious behaviors, findings candidates
- **Time**: Medium (hours)
- **Risk**: Active but no mutation/destruction (requests, pattern probes)

### Phase 3: Validating Issues
- **Goal**: Confirm findings with controlled evidence, isolate root cause, measure impact
- **Outputs**: Reproduced findings, evidence chains, impact assessment
- **Time**: Varies (depends on finding complexity)
- **Risk**: May require mutation of test data; stop once impact is clear

### Phase 4: Reporting
- **Goal**: Consolidate findings, generate reports, provide remediation guidance
- **Outputs**: Executive report, per-issue details, remediation steps
- **Time**: Fast (automated generation)
- **Risk**: None (read-only consolidation)

## Decision Gates Between Phases

### Phase 1 → Phase 2
- ✓ Endpoint inventory is complete
- ✓ Critical endpoints identified
- ✓ Parameters extracted and mapped
- ✓ JS files analyzed for hidden logic

**Go/No-Go**: User reviews endpoint map or Codex confirms coverage threshold (e.g., 90%+ of estimated endpoints)

### Phase 2 → Phase 3
- ✓ At least 1-2 viable hypothesis candidates identified
- ✓ High-confidence pattern matches noted
- ✓ Suspicious behaviors documented

**Go/No-Go**: Filter hypotheses by severity/complexity; prioritize top 5-10 candidates

### Phase 3 → Phase 4
- ✓ At least 1 finding validated to "reproduced" or "isolated verified"
- ✓ Impact demonstrated with safe evidence
- ✓ Counterevidence reviewed

**Go/No-Go**: User approves or adds findings manually; Codex formats and consolidates

## Autonomous Execution Model

Each phase can run with minimal user intervention:

```
SCOPE + RULES
    ↓
[Phase 1] Recon/Fuzz/Crawl
    ↓ (Gate 1: Endpoint coverage OK?)
[Phase 2] Scanning & Pattern Matching
    ↓ (Gate 2: Candidates found?)
[Phase 3] Validation & Isolation
    ↓ (Gate 3: Findings reproduced?)
[Phase 4] Reporting & Consolidation
    ↓
FINAL REPORT
```

At each gate, Codex can:
- **Auto-continue** if confident (e.g., >10 endpoints found, >5 pattern hits)
- **Ask user** if uncertain (e.g., no endpoints in Phase 1, no patterns in Phase 2)
- **Branch** to deeper investigation if finding suggests attack chain

## Command Execution Strategy

Codex will:
1. **Plan** before executing (show command sequence to user for approval if first run)
2. **Execute** commands in batches where possible (parallel requests, tool chains)
3. **Parse** outputs and flag anomalies in real-time
4. **Decide** next steps based on findings (adaptive testing)
5. **Backtrack** if encountering rate limits, auth walls, or out-of-scope triggers

## Tool Integration

Expected toolchain (user provides or Codex abstracts):
- **Recon**: httpx, curl, Burp CLI (headless), subdomains.io APIs
- **Crawling**: Playwright/Selenium, custom crawler scripts
- **Fuzzing**: ffuf, wfuzz, custom payload generators
- **Scanning**: Burp API, custom rule-based checks, grep-based SAST patterns
- **Validation**: curl, Playwright, custom proof scripts
- **Reporting**: Markdown generation, template merging

---

See individual phase documents for detailed execution commands and decision trees.

## Reference Quality Addendum

## Purpose

Use this section to normalize reference quality for scoring and day-to-day security work. It explains how to apply this reference during discovery, validation, attack-path analysis, reporting, or remediation.

## Workflow

1. Identify the relevant asset, code path, endpoint, workflow, or configuration.
2. Map attacker-controlled input to the closest control and security-sensitive sink or decision.
3. Validate the claim with the safest bounded proof available.
4. Search for counterevidence before promoting the issue.
5. Record impact, confidence, remediation, and proof gaps.

## False-positive checks

Suppress or downgrade when the path is unreachable, the input is not attacker-controlled, the behavior is public or self-only, an effective control blocks the exact path, the issue is scanner-only, or impact is only a best-practice concern.

## Validation example

```markdown
- expected: lower-privileged actor cannot reach protected data or action
- actual: request, test, fixture, or trace shows the protected behavior is reachable
- evidence: masked request/response, code trace, test output, callback, or parser fixture
- counterevidence: controls checked and why they do or do not apply
```

## Output fields

Include affected location, attacker input, closest control, sink or protected decision, validation evidence, impact, severity or confidence, remediation, and remaining proof gaps.
