# Unrestricted File Upload

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Improper Input Validation |
| CWE / external ID | CWE-434 |
| OWASP / WSTG / API mapping | WSTG-BUSL-09 |

## What to look for

Upload accepts dangerous files or serves user content in executable/active context.

## Vulnerable request

```http
POST /upload HTTP/1.1
Host: target.example
Content-Type: multipart/form-data; boundary=BOUNDARY
Cookie: session=TEST_USER

--BOUNDARY
Content-Disposition: form-data; name="file"; filename="proof.html"
Content-Type: text/html

<script>alert(1)</script>
--BOUNDARY--
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 201 Created
Content-Type: application/json

{"url":"https://target.example/uploads/proof.html"}
```

## Expected safe request

```http
POST /upload HTTP/1.1
Host: target.example
Content-Type: multipart/form-data; boundary=BOUNDARY
Cookie: session=TEST_USER

--BOUNDARY
Content-Disposition: form-data; name="file"; filename="proof.html"
Content-Type: text/html

<script>alert(1)</script>
--BOUNDARY--
```

## Expected safe response / behavior

```http
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/json

{"error":"file_type_not_allowed"}
```

## Evidence to collect

Show upload acceptance, served content type, and impact. Do not upload shells or malware.

## Remediation direction

Allowlist file types, verify content, store outside webroot/object execution context, randomize names, and force download/nosniff.

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
