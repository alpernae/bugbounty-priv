# IDOR / Broken Object Level Authorization

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Insecure Direct Object Reference (IDOR) |
| CWE / external ID | CWE-639 |
| OWASP / WSTG / API mapping | WSTG-ATHZ-04 / API1 BOLA |

## What to look for

User can access another user’s object by changing an identifier.

## Vulnerable request

```http
GET /api/invoices/inv_2002 HTTP/1.1
Host: target.example
Authorization: Bearer USER_A_TOKEN
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"id":"inv_2002","owner_id":"user_b","amount":"129.00","email":"userb@example.com"}
```

## Expected safe request

```http
GET /api/invoices/inv_2002 HTTP/1.1
Host: target.example
Authorization: Bearer USER_A_TOKEN
```

## Expected safe response / behavior

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{"error":"not_authorized_for_object"}
```

## Evidence to collect

Use two owned accounts. Show User B owns object and User A can read/update/delete it.

## Remediation direction

Enforce object-level authorization server-side on every request; avoid relying on hidden IDs or client filters.

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
