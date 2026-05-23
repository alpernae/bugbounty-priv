---
name: web-validation
description: Validates suspected web and API vulnerabilities by replaying HTTP requests, testing safe payloads, comparing baseline and modified responses, checking exploit reachability, confirming impact, and suppressing false positives with exact counterevidence. Use when the user asks to verify vulnerability, confirm exploit, false positive check, penetration test validation, security finding verification, validate web bug, confirm IDOR, test XSS, validate SSRF, or prove whether a scan finding is real.
metadata:
  short-description: Web validation phase
---

# Web Validation Phase

## Objective

Safely confirm, downgrade, suppress, or defer web security candidates. Validation must be repeatable, scoped, and low-impact.

## Workflow

1. State expected safe behavior.
2. Capture baseline request and response.
3. Change exactly one variable.
4. Compare authorization, data exposure, state change, callbacks, browser execution, errors, and timing.
5. Repeat with a clean session or control account.
6. Decide disposition and record evidence.

## Common Validation Commands

IDOR/BOLA:

```bash
curl -i "$BASE/api/projects/$PROJECT_B" -H "Authorization: Bearer $TOKEN_A"
curl -i "$BASE/api/projects/$PROJECT_B" -H "Authorization: Bearer $TOKEN_B"
curl -i "$BASE/api/projects/$PROJECT_B"
```

SSRF with owned callback:

```bash
curl -i -X POST "$BASE/api/fetch" -H "Authorization: Bearer $TOKEN" -d "{\"url\":\"$OWNED_CALLBACK/probe-123\"}"
```

Safe XSS reflection check:

```text
"><img src=x onerror=console.log("owned-test")>
```

Do not use destructive payloads, secret extraction, web shells, or high-volume traffic.

## Pass/Fail Criteria

| Class | Confirm when | Suppress when |
|---|---|---|
| IDOR/BOLA | lower-privileged account accesses another user's protected object | response is public, self-only, or blocked by ownership check |
| XSS | owned benign payload executes in meaningful trusted context | output is encoded, inert, self-only, or blocked by CSP with no impact |
| SSRF | target performs attacker-controlled outbound request with meaningful reachability | URL is blocked, only same-origin safe fetch occurs, or callback never fires |
| CSRF | victim browser can trigger important state change without required protection | SameSite, token, method/content-type, or auth model blocks exact attack |
| Upload | uploaded content is served/executed in risky context | content is inert, private, re-encoded, or served from safe origin |

## Suppression Record Template

```markdown
## Suppressed: cand-009 Project read BOLA

- request_hash: sha256:<hash>
- baseline: Account B owner received 200 with project JSON
- modified: Account A received 403
- anonymous_control: 401
- attempts: 3 clean sessions
- counterevidence: object ownership middleware rejects cross-tenant ids before handler
- disposition: suppressed
```

## Finding Evidence Template

```markdown
## Validated: Project read BOLA

- endpoint: GET /api/projects/{id}
- role: authenticated user
- changed_variable: path id from Account B
- expected: 403 or 404
- actual: 200 with Account B project fields
- repeatability: reproduced twice with clean Account A session
- impact: cross-user project data disclosure
- confidence: high
```

## References

- `../web-security/references/false-positive-reduction.md` - promotion and suppression rules.
- `../web-security/references/workflows/phase-3-validating-issues.md` - detailed validation workflow.
- `../web-security/references/index.md` - issue-specific validation notes.

## Hard Rules

- Use owned accounts and test data.
- Change one variable at a time.
- Stop once impact is demonstrated.
- Mask secrets and personal data.
- Record exact counterevidence when suppressing.
