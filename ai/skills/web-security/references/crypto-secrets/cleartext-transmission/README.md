# Cleartext Transmission of Sensitive Data

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Cleartext Transmission of Sensitive Information |
| CWE / external ID | CWE-319 |
| OWASP / WSTG / API mapping | WSTG-CRYP-03 |

## What to look for

Sensitive credentials/session data are transmitted over HTTP or mixed-content endpoints.

## Vulnerable request

```http
POST http://target.example/login HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded

email=test@example.com&password=REDACTED
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Set-Cookie: session=abc123
Content-Type: text/html

Logged in
```

## Expected safe request

```http
POST http://target.example/login HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded

email=test@example.com&password=REDACTED
```

## Expected safe response / behavior

```http
HTTP/1.1 301 Moved Permanently
Location: https://target.example/login
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Evidence to collect

Use your own credentials and redact secrets. Show HTTP endpoint accepts sensitive submission.

## Remediation direction

Redirect HTTP to HTTPS before accepting data, enable HSTS, and mark cookies Secure.

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
