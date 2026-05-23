---
name: source-threat-model
description: Generates and maintains repository security threat models by identifying product surfaces, assets, trust boundaries, attacker-controlled inputs, security invariants, and priority failure modes. Produces structured threat model documents for source-code security scans, CVE review, secure design review, attack surface analysis, and security audit preparation. Use when Codex is in the threat-model phase, the user invokes $threat-model, or the user asks for threat analysis, attack surface mapping, risk assessment, STRIDE-style review, or repository security context.
metadata:
  short-description: Build repository threat model
---

# Security Threat Model

## Objective

Create or reuse a repository-scoped threat model that later phases can use for finding discovery, validation, and severity calibration.

Use `../source-code-security/references/scan-artifacts.md` for default artifact paths. If the user provides a path or authoritative model, use it.

## Workflow

1. Resolve repository name and threat model path.
2. If a repository-scoped threat model already exists, use it as source of truth.
3. If the user provides a threat model or authoritative scan guidance, persist it unchanged and stop.
4. Otherwise inspect repository evidence:
   - routes, controllers, handlers, workers, CLIs, parsers, package entrypoints
   - authn/authz, tenancy, identity, secret, storage, network, cloud, CI, and deployment boundaries
   - untrusted inputs from users, tenants, files, queues, webhooks, integrations, dependencies, and configs
5. Produce the structured threat model.
6. Check that it is repository-scoped and not biased toward the current diff unless the user requested that.

## Output Format

Use `references/threat-model-template.md`. Minimal valid output:

```markdown
# Threat Model: <repository>

## Product and Runtime Surfaces
- API service exposes project, billing, export, and admin workflows.
- Worker processes webhook and queue payloads.

## Assets and Privileges
- Tenant data, admin actions, API tokens, signing keys, export files.

## Trust Boundaries
- Anonymous internet -> API gateway
- Authenticated user -> tenant resources
- Tenant admin -> organization controls
- External webhook provider -> worker queue

## Attacker-Controlled Inputs
- HTTP params and JSON bodies
- Uploaded files
- Webhook payloads
- Tenant-controlled configuration

## Security Invariants
- Users can only read/write objects in their tenant.
- Webhooks require valid signatures.
- Uploaded files never become executable trusted-origin content.

## Priority Failure Modes
- Authz bypass, cross-tenant data exposure, SSRF, parser abuse, secret leakage.

## Assumptions and Unknowns
- Deployment ingress config not present; verify during attack-path analysis.
```

## Validation Checkpoint

Before finishing, verify:

| Requirement | Pass condition |
|---|---|
| Assets | Sensitive data and privileged actions are named. |
| Boundaries | Identity, tenant, integration, and deployment boundaries are explicit. |
| Inputs | Attacker-controlled inputs map to at least one invariant. |
| Failure modes | High-impact classes are repository-specific, not generic. |

If an attacker-controlled input has no mapped invariant, revise the model before discovery.

## Reference Files

- `references/threat-model-guidance.md` - detailed generation guidance.
- `references/threat-model-template.md` - reusable document structure.

## Hard Rules

- Do not turn threat modeling into findings about the current diff.
- Keep repository scope unless the user explicitly asks for narrower scope.
- Treat provided authoritative guidance as authoritative.
- Call out unknowns instead of inventing deployment facts.
