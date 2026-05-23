# Sample Discovery Output

```markdown
## Candidate: Cross-tenant authorization bypass in project export

- candidate_id: cand-017
- status: unverified suspicion
- affected_locations:
  - entrypoint/wrapper: src/api/export.ts:84
  - root_control: src/authz/project_scope.ts:52
  - sink: src/services/export_service.ts:133
- instance_key: authz:src/api/export.ts:84
- attacker_source: `project_id` from authenticated request body
- broken_control: ownership/tenant scope check is absent before export dispatch
- impact: attacker with account A can export project data belonging to tenant B
- closest_control: role check exists, but no object-level tenant ownership check
- validation_recommended: yes
- relevant_lines:
  - src/api/export.ts:84
  - src/services/export_service.ts:133
- taxonomy:
  - CWE-639
- proof_gaps:
  - need runtime request pair (tenant A vs tenant B) to confirm behavior
```
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
