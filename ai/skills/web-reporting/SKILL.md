---
name: web-reporting
description: Generates disclosure-ready web and API vulnerability reports with severity, CVSS-style rationale when useful, reproduction steps, proof-of-concept requests, evidence, impact, remediation, retest checklist, and masked artifacts. Use when the user asks for vulnerability report, pentest findings, bug bounty writeup, security writeup, disclosure report, CVE documentation, remediation guidance, retest checklist, or final report for web findings.
metadata:
  short-description: Web reporting phase
---

# Web Reporting Phase

## Objective

Turn validated web security findings into clear reports that a program triager, developer, or auditor can reproduce and act on.

## Report Completeness Checklist

Before finalizing, verify every finding includes:

| Field | Required |
|---|---|
| Title | Vulnerability class plus affected feature. |
| Severity | Rationale tied to impact and exploitability. |
| Affected asset | URL, endpoint, operation, role, tenant/object context. |
| Reproduction | Step-by-step safe PoC with owned data. |
| Evidence | Masked request/response, callback, screenshot description, or browser proof. |
| Impact | Concrete security consequence. |
| Counterevidence | Controls checked and why they fail or do not apply. |
| Remediation | Specific fix pattern. |
| Retest | Expected fixed behavior and negative controls. |

## Report Template

```markdown
# <Severity> - <Finding Title>

## Summary
<One paragraph explaining the issue and affected feature.>

## Affected Asset
- URL/endpoint: <method path>
- role: <attacker role>
- object/tenant: <scope>

## Reproduction Steps
1. Log in as Account A.
2. Capture baseline request for Account A object.
3. Replace object id with Account B object id.
4. Send request and observe unauthorized response.

## Evidence
```http
GET /api/projects/tenant-b-project HTTP/1.1
Authorization: Bearer <redacted-account-a-token>

HTTP/1.1 200 OK
{"id":"tenant-b-project","name":"<masked>"}
```

## Impact
An authenticated user can read another tenant's project data.

## Severity Rationale
High: cross-tenant data exposure with reliable authenticated request replay.

## Remediation
Enforce object-level tenant ownership before loading or returning project data.

## Retest
- Account A requesting Account B project returns 403 or 404.
- Account B requesting its own project still returns 200.
```

## Remediation Patterns

| Class | Recommended remediation |
|---|---|
| XSS | Contextual output encoding, safe templating, sanitization for rich text, CSP as defense in depth. |
| IDOR/BOLA | Object-level authorization at server boundary and service layer. |
| SSRF | Allowlist destinations, block internal ranges, normalize URLs, restrict protocols, use egress controls. |
| SQL/NoSQL injection | Parameterized queries, typed builders, strict operator allowlists. |
| Upload issues | Content validation, re-encoding, private storage, safe serving origin, no executable processing. |
| CSRF | SameSite strategy, anti-CSRF token, strict content type, method discipline. |

## Worked Example: Reflected XSS

```markdown
# Medium - Reflected XSS in search page

## Summary
The `q` parameter is reflected into the search page without HTML encoding.

## Reproduction
1. Visit `/search?q=%22%3E%3Cimg%20src=x%20onerror=console.log(%22owned-test%22)%3E`.
2. Observe the benign test payload executes in the page context.

## Impact
An attacker can execute JavaScript in the victim's browser if they visit a crafted link. Escalation depends on cookie flags, CSRF posture, and available privileged actions.

## Remediation
HTML-encode reflected search terms and keep CSP as defense in depth.
```

## References

- `../web-security/assets/report-template.md` - full report template.
- `../web-security/references/workflows/phase-4-reporting.md` - reporting workflow.
- `../web-security/references/false-positive-reduction.md` - severity and suppression checks.

## Hard Rules

- Mask sensitive values in all evidence.
- Do not overstate impact beyond the proof.
- Include retest steps that prove both blocked exploit and preserved legitimate behavior.
- State proof gaps plainly when evidence is incomplete.
