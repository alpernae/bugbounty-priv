# File Upload Leading to Code Execution

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Unrestricted Upload of File with Dangerous Type |
| CWE / external ID | CWE-434 |
| OWASP / WSTG / API mapping | OWASP A03/A05 / WSTG-BUSL-09 / WSTG-INPV-10 |

## What to look for

Upload feature stores attacker-controlled files in an executable path, accepts server-executable extensions, or allows MIME/extension bypass that could execute code.

## Vulnerable request

```http
POST /profile/avatar HTTP/1.1
Host: target.example
Content-Type: multipart/form-data; boundary=BOUNDARY
Cookie: session=REDACTED

--BOUNDARY
Content-Disposition: form-data; name="avatar"; filename="proof.php"
Content-Type: image/png

<?php echo "PROOF_UPLOAD_EXEC_7c1"; ?>
--BOUNDARY--
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 201 Created
Content-Type: application/json

{"url":"https://target.example/uploads/proof.php"}

GET /uploads/proof.php -> HTTP/1.1 200 OK
PROOF_UPLOAD_EXEC_7c1
```

## Expected safe request

```http
POST /profile/avatar HTTP/1.1
Host: target.example
Content-Type: multipart/form-data; boundary=BOUNDARY
Cookie: session=REDACTED

--BOUNDARY
Content-Disposition: form-data; name="avatar"; filename="proof.php"
Content-Type: image/png

<?php echo "PROOF_UPLOAD_EXEC_7c1"; ?>
--BOUNDARY--
```

## Expected safe response / behavior

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"error":"unsupported_file_type"}
```

## Evidence to collect

In production, avoid uploading a real web shell. Use inert marker content unless explicitly allowed in a lab/staging environment. Evidence should prove executable storage path, accepted dangerous extension, or server-side execution risk.

## Remediation direction

Store uploads outside webroot, disable script execution in upload directories, verify magic bytes, rewrite filenames/extensions, use allowlisted file types, scan content, and serve with safe Content-Type/Content-Disposition.

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
