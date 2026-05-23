---
name: web-finding-discovery
description: Discovers candidate web and API vulnerabilities by enumerating attack surfaces, mapping endpoints and roles, identifying injection points, checking authentication and authorization flows, selecting issue playbooks, and producing evidence-backed hypotheses. Use when the user asks for reconnaissance, vulnerability discovery, pentest planning, attack surface mapping, bug bounty target review, find web vulnerabilities, API security assessment, GraphQL testing, WebSocket testing, or web security audit discovery.
metadata:
  short-description: Web discovery phase
---

# Web Finding Discovery Phase

## Objective

Generate plausible web security candidates with enough evidence to validate safely. Discovery should produce hypotheses, not final claims.

## Workflow

1. Build endpoint inventory.
2. Build role/object matrix.
3. Select vulnerability modules from references.
4. Generate candidate issues.
5. Review evidence completeness.
6. Hand candidates to validation or suppress weak leads.

## Endpoint Matrix

Use this compact table:

| Method | Path/Operation | Role | Object | Params | State change | Notes |
|---|---|---|---|---|---|---|
| GET | `/api/projects/{id}` | user | project | path id | no | object read |
| POST | `/api/invites` | admin | org | email, role | yes | role assignment |
| mutation | `updateBilling` | owner | org | plan, token | yes | billing |

Checkpoint:

- every state-changing endpoint has role and object owner
- every object id has owner/tenant expectation
- every file, URL, redirect, callback, or query input is marked attacker-controlled or trusted

## Module Selection Examples

| Signal | Open reference |
|---|---|
| Object id changed across accounts | `../web-security/references/authorization/idor-bola/README.md` |
| GraphQL object field leaks | `../web-security/references/api/graphql-bola/README.md` |
| User-controlled URL fetch | `../web-security/references/ssrf/basic/README.md` |
| Reflected parameter in HTML | `../web-security/references/xss/reflected/README.md` |
| Upload served from app origin | `../web-security/references/file-xml/unrestricted-file-upload/README.md` |

## Worked Candidate Example

Input observation:

```text
GET /api/projects/2981 returns project JSON for Account B.
Account A can change the path id and receives HTTP 200.
```

Discovery output:

```markdown
## Candidate: Project read BOLA

- status: unverified suspicion
- endpoint: GET /api/projects/{id}
- attacker_role: authenticated user
- attacker_input: path `id`
- expected_control: object owner or tenant check before response
- actual_behavior: Account A receives Account B project JSON
- impact: cross-user or cross-tenant data exposure if validation repeats cleanly
- reference: authorization/idor-bola
- validation_next_step: replay Account A, Account B, anonymous, and owner controls
- proof_gaps: confirm object tenant, response sensitivity, and clean-session repeatability
```

## Evidence Completeness Check

Before finalizing candidates:

| Missing | Action |
|---|---|
| endpoint or operation | return to mapping |
| attacker-controlled input | suppress or keep as note |
| expected safe behavior | derive from role/object matrix |
| actual observed behavior | capture baseline before validation |
| impact | mark as low-confidence until impact is clear |

## References

- `../web-security/references/index.md` - issue playbook index.
- `../web-security/references/false-positive-reduction.md` - promotion and suppression rules.
- `../web-security/references/coverage-matrix.md` - coverage checklist.

## Output Contract

For each candidate include:

- status
- endpoint, method, role, object, tenant, and request shape
- attacker input
- expected safe behavior
- observed behavior
- likely broken control
- impact hypothesis
- reference module used
- validation next step
- proof gaps
