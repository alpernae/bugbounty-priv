# Threat Model Template

## Purpose

Use this template to produce repository-scoped threat models for source-code security scans. It should give discovery enough context to prioritize important assets, boundaries, and attacker-controlled inputs.

## Workflow

1. Fill product and runtime surfaces from repository evidence.
2. Identify assets and privileges that matter.
3. Map trust boundaries and attacker inputs.
4. Define security invariants.
5. Name priority failure modes.
6. Record assumptions and unknowns.

## Template

```markdown
# Threat Model: <repository>

## Product and Runtime Surfaces
- <service/API/worker/CLI/parser/config/deployment surface>

## Assets and Privileges
- <tenant data, credentials, admin actions, signing keys, cloud resources>

## Trust Boundaries
- <anonymous -> authenticated>
- <user -> admin>
- <tenant -> tenant>
- <external integration -> worker>

## Attacker-Controlled Inputs
- <HTTP params, files, queues, webhooks, configs, dependencies>

## Security Invariants
- <authorization, tenant isolation, parser safety, secret handling>

## Priority Failure Modes
- <authz bypass, injection, SSRF, deserialization, secret leak>

## Assumptions and Unknowns
- <deployment or runtime evidence not found>
```

## Validation Checklist

- Every attacker input maps to an invariant.
- Every sensitive asset has a boundary.
- Unknowns are explicit.
- Vulnerability classes are repository-specific.

## Output Use

Later phases use this model to decide impact, scope, and whether a candidate crosses a meaningful boundary.

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
