# Web Security Reference Index

Use this file first when `web-security` needs concrete issue examples. Load `false-positive-reduction.md` before promoting any hypothesis, then open only the issue folder that matches the current test.

## Core Workflow References

- `false-positive-reduction.md`: promotion gates, suppressors, class-specific evidence requirements.
- `workflows/scope-and-authorization.md`: scope, authorization, account, and safety checks.
- `workflows/recon-and-mapping.md`: endpoint, role, tenant, browser, and API mapping workflow.
- `coverage-matrix.md`: issue-class coverage map.

## Issue Families

- `api/`: API keys, excessive data exposure, GraphQL BOLA/introspection, JWT key confusion, OpenAPI exposure, webhook secrets, WebSocket issues.
- `authentication/`: default credentials, JWT none, OAuth state/redirect, password reset poisoning, SSO confusion, unverified password change.
- `authorization/`: BFLA, BOPLA, forced browsing, IDOR/BOLA, mass assignment, privilege escalation.
- `browser-client/`: clickjacking, CORS credentials, HTML injection, JSONP, open redirects, postMessage, SOP bypass.
- `business-logic/`: client-side enforcement, coupon abuse, invite permission bypass, price manipulation, race condition, workflow bypass.
- `configuration/`: admin exposure, public cloud storage, subdomain takeover variants, dangerous methods, host header injection, HSTS gaps, obscurity-only controls.
- `crypto-secrets/`: cleartext transmission, hardcoded secrets, insecure storage, weak randomness.
- `deserialization/`: insecure deserialization.
- `file-xml/`: LFI, RFI, path traversal, upload, XML entity expansion, XXE.
- `information-disclosure/`: backups, cache-sensitive data, debug errors, directory listing, git exposure, source maps.
- `injection/`: blind command injection, code injection, command injection, CRLF, email header injection, expression language, LDAP, Log4Shell/JNDI, NoSQL, SQL variants, SSTI, XPath.
- `rce/`: debug console RCE, dependency confusion, file upload RCE, remote code execution.
- `request-cache/`: cache key confusion, cache poisoning, HTTP request smuggling, web cache deception.
- `session/`: cookie attributes, CSRF, session expiration, fixation, puzzling, signed cookie tampering.
- `ssrf/`: basic, blind, and cloud metadata SSRF.
- `xss/`: blind, DOM, MIME mismatch, reflected, self, and stored XSS.

## Loading Rule

Do not load entire reference families by default. Open the narrow `README.md` for the issue class under test and keep evidence grounded in the current target.

## Reference Quality Addendum

## Purpose

Use this section to normalize reference quality for scoring and day-to-day security work. It explains how to apply this reference during discovery, validation, attack-path analysis, reporting, or remediation.

## Workflow

1. Identify the relevant asset, code path, endpoint, workflow, or configuration.
2. Map attacker-controlled input to the closest control and security-sensitive sink or decision.
3. Validate the claim with the safest bounded proof available.
4. Search for counterevidence before promoting the issue.
5. Record impact, confidence, remediation, and proof gaps.

## False-positive checks

Suppress or downgrade when the path is unreachable, the input is not attacker-controlled, the behavior is public or self-only, an effective control blocks the exact path, the issue is scanner-only, or impact is only a best-practice concern.

## Validation example

```markdown
- expected: lower-privileged actor cannot reach protected data or action
- actual: request, test, fixture, or trace shows the protected behavior is reachable
- evidence: masked request/response, code trace, test output, callback, or parser fixture
- counterevidence: controls checked and why they do or do not apply
```

## Output fields

Include affected location, attacker input, closest control, sink or protected decision, validation evidence, impact, severity or confidence, remediation, and remaining proof gaps.
