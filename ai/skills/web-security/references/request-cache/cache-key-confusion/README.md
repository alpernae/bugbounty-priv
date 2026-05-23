# Cache Key Confusion / Header Poisoning

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Web Cache Poisoning |
| CWE / external ID | CWE-444 / CWE-20 |
| OWASP / WSTG / API mapping | OWASP A05 Security Misconfiguration / Cache security |

## What to look for

Unkeyed headers, query parameters, or host/protocol headers influence cached responses shared with other users.

## Vulnerable request

```http
GET /login HTTP/1.1
Host: target.example
X-Forwarded-Host: proof-cache.example.invalid
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Cache-Control: public
X-Cache: MISS

<link rel="canonical" href="https://proof-cache.example.invalid/login">
```

## Expected safe request

```http
GET /login HTTP/1.1
Host: target.example
X-Forwarded-Host: proof-cache.example.invalid
```

## Expected safe response / behavior

```http
HTTP/1.1 200 OK
Cache-Control: no-store

<link rel="canonical" href="https://target.example/login">
```

## Evidence to collect

Use harmless marker hostnames you control or `.invalid`. Do not poison production pages for other users. Capture cache headers, key assumptions, and purge/retest evidence if available.

## Remediation direction

Do not trust forwarding headers for generated links, normalize Host handling, include influential headers in cache key or strip them, disable caching for dynamic pages, and deploy cache poisoning tests.

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
