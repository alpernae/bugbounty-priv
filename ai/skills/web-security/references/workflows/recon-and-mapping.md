# Recon And Mapping Workflow

## Purpose

Use this reference to map a scoped web, API, GraphQL, WebSocket, or browser target before issue-specific testing. The goal is to build enough surface, role, object, and input context to discover real vulnerabilities without noisy probing.

## Workflow

1. Confirm scope and allowed testing actions.
2. Inventory hosts, routes, API bases, GraphQL operations, WebSocket channels, uploads, redirects, webhooks, and client routes.
3. Identify parameters, cookies, headers, object ids, tenant ids, files, origins, callbacks, and tokens.
4. Map roles and object ownership.
5. Mark state-changing actions and sensitive reads.
6. Pick issue modules from `../index.md`.

## Surface Map

Collect:

- hosts, subdomains, API bases, and environments
- REST, GraphQL, WebSocket, SSE, gRPC-web, upload, webhook, and export endpoints
- query params, body fields, headers, cookies, CSRF tokens, tenant ids, object ids, and role indicators
- client bundle routes and hidden API calls
- auth flows: login, reset, MFA, SSO, OAuth/OIDC/SAML, logout, refresh
- state-changing actions: create, update, delete, billing, invites, roles, exports, integrations

## Role And Object Matrix

| Endpoint | Method | Role | Object owner | Tenant | Baseline | Cross-account | Anonymous |
|---|---|---|---|---|---|---|---|
| `/api/projects/{id}` | GET | user | Account B | tenant B | 200 | test | 401 |

## Validation Guidance

Change one variable at a time and preserve raw request shapes. A mapped endpoint is ready for testing only when expected safe behavior is clear.

## False-Positive Checks

Suppress leads when behavior is public by design, object ownership is enforced, or the observed difference is only a status code without data/state impact.

## Output Fields

Endpoint, method, role, object owner, attacker-controlled fields, expected safe behavior, observed behavior, selected issue module, and proof gaps.

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
