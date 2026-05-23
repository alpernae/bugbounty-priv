# Web Security Coverage Matrix

This matrix tracks practical web/API issue coverage in this skill. It is not a severity promise; every issue still needs target-specific reachability, attacker control, broken control, impact, and isolated verification.

| Area | Covered issue families |
| --- | --- |
| Authorization | IDOR/BOLA, BFLA, BOPLA, forced browsing, mass assignment, privilege escalation |
| Authentication | Default credentials, JWT none/key confusion, OAuth state and redirect URI, password reset poisoning, SSO confusion, password-change verification |
| Sessions | Cookie attributes, CSRF, expiration, fixation, session puzzling, signed cookie tampering |
| Injection | SQL variants, NoSQL, LDAP, XPath, command, blind command, code, expression language, SSTI, CRLF, email header, Log4Shell/JNDI |
| XSS/browser | Reflected, stored, DOM, blind, self, MIME mismatch, CORS, clickjacking, HTML injection, JSONP, postMessage, SOP bypass |
| SSRF/network | Basic SSRF, blind SSRF, cloud metadata SSRF |
| Files/parsers | Upload, upload RCE, LFI, RFI, path traversal, XXE, XML entity expansion, insecure deserialization |
| API/realtime | API key exposure, excessive data exposure, OpenAPI exposure, GraphQL BOLA/introspection, webhook secrets, WebSocket auth/CSRF |
| Business logic | Price manipulation, coupons, workflow bypass, invite permissions, client-side enforcement, races |
| Request/cache | Request smuggling, cache poisoning, cache key confusion, web cache deception |
| Configuration | Admin exposure, public cloud storage, subdomain takeover, DNS/NS/CNAME takeover, dangerous methods, host header injection, HSTS gaps |
| Crypto/secrets | Cleartext transmission, hardcoded secrets, insecure storage, weak randomness |
| Information disclosure | Backups, debug errors, directory listing, git exposure, source maps, cache-sensitive data |
| Supply chain/RCE | Dependency confusion, debug console RCE, remote code execution |

## Usually Not Reportable Without Strong Extra Proof

- Missing headers without an exploit chain.
- User enumeration or rate-limit-only observations without accepted scope and meaningful impact.
- Self-XSS without cross-boundary execution.
- Open redirects without OAuth, token, trusted-domain, or comparable security impact.
- Version banners, public metadata, or scanner-only alerts.

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
