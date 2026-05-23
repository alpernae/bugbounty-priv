# XML Entity Expansion

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | XML Entity Expansion |
| CWE / external ID | CWE-776 |
| OWASP / WSTG / API mapping | WSTG-INPV-07 |

## What to look for

XML parser expands nested entities and can consume excessive resources.

## Vulnerable request

```http
POST /api/xml/parse HTTP/1.1
Host: target.example
Content-Type: application/xml

<?xml version="1.0"?>
<!DOCTYPE proof [
<!ENTITY a "1234567890">
<!ENTITY b "&a;&a;&a;">
]>
<proof>&b;</proof>
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: application/xml

<proof>123456789012345678901234567890</proof>
```

## Expected safe request

```http
POST /api/xml/parse HTTP/1.1
Host: target.example
Content-Type: application/xml

<?xml version="1.0"?>
<!DOCTYPE proof [<!ENTITY a "123">]><proof>&a;</proof>
```

## Expected safe response / behavior

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"error":"doctype_not_allowed"}
```

## Evidence to collect

Keep entity expansion tiny and non-disruptive; do not run DoS payloads.

## Remediation direction

Disable DTDs/entities and set parser expansion limits/timeouts.

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
