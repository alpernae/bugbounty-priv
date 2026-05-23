# DNS Zone Takeover

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Improper Control of Resource Identifiers |
| CWE / external ID | CWE-610 / CWE-20 |
| OWASP / WSTG / API mapping | OWASP A05 Security Misconfiguration / DNS takeover |

## What to look for

A registered domain delegates authoritative DNS to a third-party provider where the DNS zone was deleted/unclaimed, allowing an attacker to claim the zone and control records.

## Vulnerable request

```http
GET /dns-evidence/example.com HTTP/1.1
Host: notes.local

Observed commands:
$ dig NS example.com +short
ns1.vulnerable-dns-provider.example.
ns2.vulnerable-dns-provider.example.
$ dig @ns1.vulnerable-dns-provider.example example.com SOA
;; status: REFUSED or SERVFAIL / no claimed zone
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: text/plain

Domain delegates to provider nameservers, but authoritative query shows unclaimed/deleted zone signature.
```

## Expected safe request

```http
GET /dns-evidence/example.com HTTP/1.1
Host: notes.local

$ dig NS example.com +short
ns1.provider.example.
$ dig @ns1.provider.example example.com SOA
```

## Expected safe response / behavior

```http
HTTP/1.1 200 OK
Content-Type: text/plain

Authoritative server returns a valid SOA for the owned zone, or delegation is removed.
```

## Evidence to collect

Collect NS records, authoritative responses, provider signature, timestamps, and screenshots. Do not claim the zone, redirect traffic, create MX records, or intercept traffic unless the program explicitly instructs you to do so.

## Remediation direction

Remove stale NS delegation, recreate/claim the DNS zone, verify authoritative SOA consistency, monitor SERVFAIL/REFUSED/no-zone signatures, and inventory domains across registrars/providers.

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
