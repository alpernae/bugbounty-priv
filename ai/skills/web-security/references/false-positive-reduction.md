# False Positive Reduction

Use this before promoting any web or API hypothesis. Scanner output, proxy observations, status-code differences, and payload reflection are leads only.

## Required Gates

1. Reachability: the route, browser flow, GraphQL operation, WebSocket channel, webhook, file workflow, or API action is reachable in scope.
2. Attacker control: the attacker controls the relevant object id, tenant id, request parameter, body field, header, cookie, origin, uploaded file, URL, token, workflow state, or channel id.
3. Broken control: authentication, authorization, tenant scoping, token binding, signature validation, parser hardening, output encoding, CSRF/CORS/browser policy, file validation, redirect/SSRF filtering, cache keying, rate limiting, or business invariant is absent, bypassed, or mis-scoped.
4. Impact: protected data is disclosed, protected state changes, code or command executes, trusted-origin script runs, internal services are reached, secrets are exposed, or availability impact is meaningful and in scope.
5. Repeatability: the result reproduces from a clean browser profile, fresh HTTP session, or isolated replay.

If any gate is missing, keep the item as `unverified suspicion`, `suppressed`, `not applicable`, or `blocked`.

## Common Suppressors

- Public or intentionally exposed data.
- Self-only behavior with no meaningful security impact.
- The attacker already has equivalent privilege.
- Anonymous and cross-account controls return the expected 401, 403, or object-not-found behavior.
- Framework, gateway, CDN, WAF, middleware, browser policy, or deployment config blocks the exact path.
- The proof is only a scanner alert, reflected string, missing header, version banner, stack trace without sensitive data, or status-code difference.
- Exploitation requires unrealistic victim behavior, production-only destructive actions, or out-of-scope systems.

## Class-Specific Gates

- Access control: use Account A, Account B, and anonymous controls. Record exact leaked fields or unauthorized state changes.
- XSS: prove execution in the relevant victim context and meaningful impact. Self-XSS and alert-only reflected XSS are usually low or ineligible.
- SQL/NoSQL injection: prove query semantic control, timing, error, or data access. Do not dump sensitive rows.
- SSRF: prove controlled outbound fetch first, then meaningful internal, metadata, callback, or network impact within scope.
- CSRF: prove browser-simple cross-site request succeeds with credentials and changes important state.
- CORS: prove attacker-controlled origin can read a sensitive credentialed response.
- File upload: prove upload and retrieval or processing impact together. Upload acceptance alone is not enough.
- Cache/request issues: prove shared cache poisoning, request desync, web cache deception, or cross-user impact, not only parser ambiguity.
- Business logic: prove unauthorized financial, entitlement, workflow, quota, approval, or integrity state change.
- Rate limit and enumeration: only promote when the program accepts the class and the impact is meaningful.

## Evidence Format

For each candidate, preserve:

- baseline request and expected behavior
- attack request with one changed variable
- negative controls
- key response fields or side effects
- role, tenant, and object ownership
- callback logs, browser proof, or timing evidence when relevant
- remaining proof gaps

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
