# NS Subdomain Takeover

## Scope
Use this reference only on assets where you have explicit authorization. Prefer test accounts, test tenants, sandbox payments, and non-destructive proof data. Do not run destructive payloads, persistence, shells, credential theft, or data exfiltration.

## Mapping

| Field | Value |
| --- | --- |
| HackerOne weakness | Improper Control of Resource Identifiers |
| CWE / external ID | CWE-610 |
| OWASP / WSTG / API mapping | OWASP A05 Security Misconfiguration / DNS delegation |

## What to look for

A subdomain is delegated using NS records to nameservers or a managed DNS provider where the delegated zone is unclaimed, misconfigured, or a nameserver domain is registrable.

## Vulnerable request

```http
GET /dns-evidence/sub.example.com HTTP/1.1
Host: notes.local

Observed commands:
$ dig NS sub.example.com +short
ns1.deleted-zone-provider.example.
$ dig @ns1.deleted-zone-provider.example sub.example.com SOA
;; status: REFUSED
```

## Vulnerable response / observable behavior

```http
HTTP/1.1 200 OK
Content-Type: text/plain

Delegated subdomain points to provider nameservers with no claimed zone; subdomain DNS could be controlled if claimed.
```

## Expected safe request

```http
GET /dns-evidence/sub.example.com HTTP/1.1
Host: notes.local

$ dig NS sub.example.com +short
ns1.active-provider.example.
$ dig @ns1.active-provider.example sub.example.com SOA
```

## Expected safe response / behavior

```http
HTTP/1.1 200 OK
Content-Type: text/plain

Delegation has a valid SOA controlled by the organization, or stale NS records are removed.
```

## Evidence to collect

Collect parent-zone NS delegation, authoritative query results per nameserver, provider-specific no-zone signature, and proof that the nameserver domain/provider is claimable. Avoid taking over the zone unless authorized.

## Remediation direction

Remove stale NS records, claim delegated zones, use automated DNS inventory, alert on dangling delegations, and verify every delegated subdomain returns expected SOA/NS data.

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
