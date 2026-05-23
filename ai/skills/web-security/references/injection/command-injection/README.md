# OS Command Injection

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | OS Command Injection |
| CWE / external ID | CWE-78 |
| OWASP / WSTG / API mapping | WSTG-INPV-12 / OWASP A03 Injection |

## What to look for

User input reaches an operating-system command, shell, process runner, image/video/PDF converter, archive utility, ping/traceroute/nslookup feature, backup job, or admin diagnostic endpoint without strict argument separation.

## Vulnerable request

```http
POST /tools/ping HTTP/1.1
Host: target.example
Content-Type: application/json
Cookie: session=REDACTED

{"host":"127.0.0.1; printf PROOF_CMD_9f3a"}
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: text/plain

PING 127.0.0.1
PROOF_CMD_9f3a
```

## Expected safe request

```http
POST /tools/ping HTTP/1.1
Host: target.example
Content-Type: application/json
Cookie: session=REDACTED

{"host":"127.0.0.1; printf PROOF_CMD_9f3a"}
```

## Expected safe response / behavior

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"error":"host_must_be_valid_ip_or_hostname"}
```

## Evidence to collect

Show a harmless unique marker such as `PROOF_CMD_<nonce>` or a small timing delta. Do not read files, print environment variables, start shells, write persistent files, connect to third-party systems, or chain to privilege escalation.

## Remediation direction

Avoid shell invocation. Use native libraries for network diagnostics, invoke executables with argument arrays, strict allowlists, canonicalization, sandboxed workers, least-privilege service accounts, and egress controls.

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
