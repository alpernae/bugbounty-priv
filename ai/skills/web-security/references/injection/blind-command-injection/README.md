# Blind OS Command Injection

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | OS Command Injection |
| CWE / external ID | CWE-78 |
| OWASP / WSTG / API mapping | WSTG-INPV-12 / OWASP A03 Injection |

## What to look for

No direct command output is returned, but a parameter can influence command execution through timing, controlled DNS/HTTP callback, or observable job side effects.

## Vulnerable request

```http
POST /api/import-url HTTP/1.1
Host: target.example
Content-Type: application/json
Cookie: session=REDACTED

{"url":"https://example.test/file.csv","postProcess":"gzip; sleep 3"}
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{"job":"job_123","status":"queued"}

Observed: same job consistently takes ~3 seconds longer than baseline.
```

## Expected safe request

```http
POST /api/import-url HTTP/1.1
Host: target.example
Content-Type: application/json
Cookie: session=REDACTED

{"url":"https://example.test/file.csv","postProcess":"gzip; sleep 3"}
```

## Expected safe response / behavior

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"error":"invalid_post_processor"}
```

## Evidence to collect

Use one or two low-volume timing tests or a collaborator endpoint you control only when allowed. Do not scan egress, query metadata, or invoke commands that disclose data.

## Remediation direction

Replace shell composition with fixed worker actions, strict enum validation, argument arrays, job sandboxing, low-privileged service accounts, and command execution telemetry.

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
