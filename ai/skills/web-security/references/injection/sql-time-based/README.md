# SQL Injection - Time Based

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | SQL Injection |
| CWE / external ID | CWE-89 |
| OWASP / WSTG / API mapping | WSTG-INPV-05 |

## What to look for

Injected database delay changes response timing, indicating SQL execution control.

## Vulnerable request

```http
GET /products?id=10%3BSELECT%20pg_sleep(3)-- HTTP/1.1
Host: target.example
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
X-Response-Time: 3.084s
Content-Type: text/html

Product: Test Product
```

## Expected safe request

```http
GET /products?id=10%3BSELECT%20pg_sleep(3)-- HTTP/1.1
Host: target.example
```

## Expected safe response / behavior

```http
HTTP/1.1 400 Bad Request
X-Response-Time: 0.031s
Content-Type: application/json

{"error":"invalid_id"}
```

## Evidence to collect

Use minimal safe delay and very few requests. Include timing baseline and delayed response comparison.

## Remediation direction

Parameterize, reject stacked queries where not needed, enforce strict input types, and use query timeouts.

## Report checklist

- Affected endpoint, method, and parameter/body field.
- Two-account or role comparison when authorization is involved.
- Baseline safe request and modified vulnerable request.
- Exact response difference, side effect, or screenshot/video proof.
- Business impact written in plain language.
- Clear remediation recommendation.
- Redaction of credentials, tokens, secrets, PII, and private customer data.

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
