---
name: web-threat-model
description: Builds threat models for authorized web, API, GraphQL, WebSocket, and browser security testing by enumerating assets, trust boundaries, attacker-controlled inputs, roles, tenants, workflows, and security invariants. Produces structured threat model documents for pentest planning, attack surface mapping, threat analysis, security assessment preparation, bug bounty scoping, and web application risk review. Use when the user asks to build a threat model, map an attack surface, prepare for a pentest, scope a bug bounty, or analyze security risks for a web application or API.
metadata:
  short-description: Web threat model phase
---

# Web Threat Model Phase

Use this phase before web vulnerability discovery or validation. The output should make it obvious what matters, who can attack it, where boundaries are crossed, and which invariants must hold.

## Workflow

1. Confirm scope and authorization.
2. List assets and privileged workflows.
3. Map roles, tenants, identity states, and object ownership.
4. Enumerate attacker-controlled inputs.
5. Map trust boundaries.
6. Define security invariants.
7. Name high-priority failure modes.
8. Validate the model before discovery.

## Output Format

```markdown
# Web Threat Model: <target>

## Scope
- assets: <domains/apps/apis>
- environment: <prod/staging/local/lab>
- accounts: <roles available>
- constraints: <rate limits/out-of-scope actions>

## Assets and Workflows
- project data export
- billing changes
- invitation and role management
- password reset and SSO callback

## Roles and Objects
| Role | Objects owned | Sensitive actions |
|---|---|---|
| anonymous | none | login, signup, reset request |
| user | own profile, own projects | read/update own data |
| org admin | tenant users/projects | invite, export, billing |

## Attacker-Controlled Inputs
- URL path ids, query params, JSON bodies, cookies, headers
- GraphQL variables, WebSocket messages, uploads, webhook payloads
- OAuth redirect parameters and SSO assertions

## Trust Boundaries
- browser -> API
- unauthenticated -> authenticated
- user -> org admin
- tenant A -> tenant B
- external webhook/OAuth provider -> application

## Security Invariants
- users cannot access objects outside their tenant
- state-changing actions require correct role and CSRF/token controls
- redirects stay on allowlisted origins
- uploaded content cannot execute as trusted-origin script

## Priority Failure Modes
- IDOR/BOLA/BFLA, auth bypass, token confusion, SSRF, XSS, SQL/NoSQL injection, upload execution, cache poisoning, business-logic bypass
```

## Worked Workflow Example

Authentication flow:

| Step | Boundary | Invariant |
|---|---|---|
| user submits login | anonymous -> auth service | credentials verified before session creation |
| app sets session cookie | server -> browser | `HttpOnly`, `Secure`, and correct `SameSite` for risk |
| OAuth callback returns code | IdP -> app | state, redirect URI, issuer, and nonce are bound |
| user changes password | user -> account settings | old password or recent auth required |

## Validation Checkpoint

Before moving to discovery, verify:

- every attacker-controlled input maps to at least one invariant
- every sensitive workflow has a role and object owner
- every cross-tenant or privilege boundary has an expected control
- unknowns are explicit, not silently assumed

## References

- `../web-security/references/workflows/scope-and-authorization.md` - scope intake.
- `../web-security/references/workflows/recon-and-mapping.md` - mapping guidance.
- `../web-security/references/coverage-matrix.md` - coverage reminders.
