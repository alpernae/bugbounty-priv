# Privilege Escalation

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Privilege Escalation |
| CWE / external ID | CWE-269 |
| OWASP / WSTG / API mapping | WSTG-ATHZ-03 |

## What to look for

User can increase own privileges or gain unauthorized capabilities.

## Vulnerable request

```http
PATCH /api/users/me HTTP/1.1
Host: target.example
Authorization: Bearer BASIC_USER_TOKEN
Content-Type: application/json

{"role":"admin"}
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"id":123,"role":"admin"}
```

## Expected safe request

```http
PATCH /api/users/me HTTP/1.1
Host: target.example
Authorization: Bearer BASIC_USER_TOKEN
Content-Type: application/json

{"role":"admin"}
```

## Expected safe response / behavior

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"error":"immutable_or_forbidden_field: role"}
```

## Evidence to collect

Show initial role, request, resulting role/capability, and impact scope.

## Remediation direction

Use server-side immutable fields, deny mass assignment, and check permissions before privilege-changing operations.

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
