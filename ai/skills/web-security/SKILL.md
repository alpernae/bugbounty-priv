---
name: web-security
description: Authorized web application and API security testing workflow for scoped reconnaissance, endpoint mapping, role/object matrixing, vulnerability discovery, safe proof-of-concept validation, false-positive reduction, severity triage, bug bounty reporting, and remediation guidance. Use for web, API, GraphQL, WebSocket, browser, authentication, authorization, injection, SSRF, upload, cache, session, XSS, and business-logic testing.
---

# Web Security

Use this skill for authorized web application, API, GraphQL, WebSocket, and browser security testing. Operate as an evidence-first application security triager: scoped, low-noise, reversible, and impact-focused.

## Architecture

Use a hybrid model:

| Need | Use |
|---|---|
| End-to-end web test | This `web-security` orchestrator |
| Threat modeling only | `../web-threat-model/SKILL.md` |
| Discovery only | `../web-finding-discovery/SKILL.md` |
| Validation only | `../web-validation/SKILL.md` |
| Reporting only | `../web-reporting/SKILL.md` |
| Deep issue playbooks | `references/index.md` and issue-specific `README.md` files |

## Hard Rules

1. Confirm the target is in scope or is an authorized local/lab target.
2. Use owned accounts, test tenants, low-volume requests, and reversible actions.
3. Do not exfiltrate secrets, corrupt production data, persist access, evade detection, deploy malware, phish users, or attack third parties.
4. Mask tokens, cookies, personal data, private keys, passwords, emails, and customer data.
5. Stop once vulnerability and impact are demonstrated.

## Core Workflow

1. Scope intake:
   - program, asset, environment, allowed accounts, rate limits, automation rules, and out-of-scope actions.
2. Map application:
   - hosts, API bases, endpoints, parameters, cookies, headers, GraphQL operations, WebSocket channels, uploads, redirects, webhooks, and client routes.
3. Build role/object matrix:
   - anonymous, user, manager, admin, org owner, invited user; object owner, same tenant, cross tenant.
4. Choose modules:
   - open `references/false-positive-reduction.md`, `references/index.md`, then the specific issue reference.
5. Validate safely:
   - baseline request, change one variable, compare behavior, stop at clear impact.
6. Report:
   - use `assets/report-template.md` or `../web-reporting/SKILL.md`.

## Concrete Test Examples

IDOR/BOLA check with owned accounts:

```bash
curl -i "$BASE/api/projects/$PROJECT_B" -H "Authorization: Bearer $TOKEN_A"
curl -i "$BASE/api/projects/$PROJECT_B" -H "Authorization: Bearer $TOKEN_B"
```

Expected signal:

| Result | Interpretation |
|---|---|
| Account A gets `403/404`, Account B gets `200` | likely safe for this path |
| Account A gets `200` and sees Account B data | candidate finding |
| Both get same public data | likely suppress or downgrade |

Safe reflected XSS probe in owned test data:

```text
<img src=x onerror=console.log("owned-test")>
```

Use only inert payloads in owned scope. Escalate only if browser-context impact is meaningful.

## False-Positive Gates

Promote a finding only when all are true:

| Gate | Evidence |
|---|---|
| Reachability | Endpoint, flow, channel, webhook, or upload path is reachable in scope. |
| Attacker control | Attacker controls the relevant id, parameter, file, origin, URL, token, header, body, or workflow state. |
| Broken control | Auth, authz, token binding, parser hardening, CORS/CSRF, redirect/SSRF filter, cache key, or business invariant fails. |
| Impact | Protected data/state/control is exposed, modified, executed, or bypassed. |
| Repeatability | Behavior reproduces with a clean session or isolated replay. |

## Output Contract

For each issue or hypothesis include:

- status: `unverified suspicion`, `reproduced finding`, `isolated verified finding`, `suppressed`, `not applicable`, or `blocked`
- affected endpoint, method, role, object id, tenant id, and request shape
- attacker input and broken control
- expected safe behavior and actual behavior
- evidence: status code, response excerpt, callback, browser proof, or side effect
- impact, confidence, counterevidence, and proof gaps
- Burp-ready request or curl command when useful

## Reference Map

- `references/workflows/PHASES_OVERVIEW.md` - end-to-end phase workflow.
- `references/workflows/recon-and-mapping.md` - recon and endpoint mapping.
- `references/false-positive-reduction.md` - promotion and suppression rules.
- `references/index.md` - per-issue reference index.
- `assets/report-template.md` - report format.

## Scripts

```bash
python scripts/check_skill_structure.py
python scripts/new_finding.py --help
python scripts/api_key_exposure_triage.py --help
```
