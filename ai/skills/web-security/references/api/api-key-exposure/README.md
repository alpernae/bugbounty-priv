# Exposed API Key / Secret

## Scope
Use this reference only on assets where you have explicit authorization. This workflow is for validating whether a disclosed key is active and impactful without spending money, changing state, sending messages, accessing customer data, or abusing third-party services.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Use of Hard-coded Credentials / Insufficiently Protected Credentials |
| CWE / external ID | CWE-798 / CWE-522 / CWE-200 |
| OWASP / WSTG / API mapping | WSTG-INFO-05 / OWASP API8 Security Misconfiguration |

## What to look for

API keys, OAuth tokens, webhooks, cloud credentials, service account JSON, private keys, package tokens, CI/CD tokens, map keys, analytics keys, payment keys, email-provider keys, or cloud storage credentials exposed in JavaScript, source maps, mobile bundles, public repos, CI logs, backup files, API responses, docs, screenshots, or error pages.

## Vulnerable request

```http
GET /static/app.js HTTP/1.1
Host: target.example
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: application/javascript

window.__CONFIG__ = {
  githubToken: "ghp_REDACTED_PROOF_TOKEN",
  sendGridKey: "SG.REDACTED_PROOF",
  awsAccessKeyId: "AKIAREDACTEDPROOF"
};
```

## Expected safe request

```http
GET /static/app.js HTTP/1.1
Host: target.example
```

## Expected safe response / behavior

```http
HTTP/1.1 200 OK
Content-Type: application/javascript

window.__CONFIG__ = {
  apiBase: "https://api.target.example",
  publicTelemetryKey: "public_client_key_only"
};
```

## KeyHacks-style safe validation workflow

1. Identify provider and key type from prefix, context, filename, variable name, or surrounding code.
2. Confirm the key is in scope: owned asset, bounty policy allows secret validation, and third-party terms are respected.
3. Store the raw key only in a local environment variable. Never paste it into reports, shell history, screenshots, or chat.
4. Prefer non-mutating validation endpoints: auth status, token metadata, caller identity, scopes, or explicit invalid/valid error difference.
5. Do not list customer resources, send emails/messages, create infrastructure, charge cards, read private data, or rotate/delete keys.
6. Capture only minimal proof: provider, redacted prefix/suffix, endpoint used, status code, scope names if safe, and timestamp.
7. Recommend immediate rotation/revocation and secret scanning.

## Example validation request patterns

These examples use environment variables so the secret is not written to the request transcript. Replace provider/domain only when the HackerOne program allows it.

### GitHub token - scope/caller metadata only

```http
GET /user HTTP/1.1
Host: api.github.com
Authorization: Bearer ${DISCLOSED_GITHUB_TOKEN}
Accept: application/vnd.github+json
```

Valid tokens commonly return `200` with account metadata and response headers can include OAuth scopes. Invalid/revoked tokens return `401`.

### AWS access key - caller identity only

```http
POST / HTTP/1.1
Host: sts.amazonaws.com
Authorization: AWS4-HMAC-SHA256 Credential=${AWS_ACCESS_KEY_ID}/REDACTED
X-Amz-Target: AWSSecurityTokenServiceV20110615.GetCallerIdentity
```

Use `aws sts get-caller-identity` with environment variables. Do not enumerate IAM, S3, EC2, billing, or secrets unless explicitly authorized.

### Slack webhook - validity only

```http
POST /services/T00000000/B00000000/REDACTED HTTP/1.1
Host: hooks.slack.com
Content-Type: application/json

{"text":""}
```

A Slack webhook can reveal valid/invalid behavior without sending meaningful content. Do not post messages to real channels.

### SendGrid token - scope metadata only

```http
GET /v3/scopes HTTP/1.1
Host: api.sendgrid.com
Authorization: Bearer ${DISCLOSED_SENDGRID_TOKEN}
Content-Type: application/json
```

Do not send emails, list contacts, export templates, or change settings.

### Dropbox token - current-account metadata only

```http
POST /2/users/get_current_account HTTP/1.1
Host: api.dropboxapi.com
Authorization: Bearer ${DISCLOSED_DROPBOX_TOKEN}
```

Do not list files or download content.

### Square token - auth boundary only

```http
GET /v2/locations HTTP/1.1
Host: connect.squareup.com
Authorization: Bearer ${DISCLOSED_SQUARE_TOKEN}
```

Only use when program policy allows validating payment-related credentials. Never create payments, refunds, customers, or orders.

## Evidence to collect

- Exact file/URL/repo/path where the key appears.
- Key type/provider and redacted key preview, for example `ghp_...ABCD`.
- Whether it is public, authenticated, or role-restricted.
- Minimal non-mutating validation result, status code, and scope/caller metadata when safe.
- Screenshot or raw response with every secret and account detail redacted.
- Impact: what the exposed key could access based on scopes and provider docs.

## Remediation direction

Rotate/revoke the exposed key, remove it from history/build artifacts/client bundles, move secret use server-side, scope credentials to least privilege, enforce environment-based secret injection, add secret scanning in CI, monitor provider audit logs, and verify no unauthorized use occurred.

## Report checklist

- Asset and exact exposed location.
- Key provider/type and redacted key evidence.
- Safe validation method and minimal result.
- Privilege/scope impact without accessing customer data.
- Rotation/remediation recommendation.
- evidence note path in the response or user-requested artifact updated.

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
