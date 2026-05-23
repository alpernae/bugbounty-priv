# Webhook Secret Exposure / Weak Verification

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Insufficiently Protected Credentials |
| CWE / external ID | CWE-522 / CWE-347 |
| OWASP / WSTG / API mapping | OWASP API8 Security Misconfiguration / API2 Broken Authentication |

## What to look for

Webhook signing secrets are exposed, weak, missing, reused across tenants, or server accepts unsigned/spoofed webhook events.

## Vulnerable request

```http
POST /webhooks/payment HTTP/1.1
Host: target.example
Content-Type: application/json
X-Signature: missing

{"event":"invoice.paid","account_id":"acct_test_owned","amount":100}
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"accepted"}
```

## Expected safe request

```http
POST /webhooks/payment HTTP/1.1
Host: target.example
Content-Type: application/json
X-Signature: missing

{"event":"invoice.paid","account_id":"acct_test_owned","amount":100}
```

## Expected safe response / behavior

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"error":"invalid_signature"}
```

## Evidence to collect

Use a test account and harmless event. Do not forge financial state on real accounts. Capture signature behavior, replay behavior, tenant binding, and event idempotency.

## Remediation direction

Require HMAC/signature verification, timestamp tolerance, replay protection, per-tenant secrets, strict event schemas, and independent server-side verification with the payment/provider API.

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
