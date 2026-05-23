# Sample Attack-Path Output

```markdown
## Finding: Cross-tenant export authorization bypass

- candidate_id: cand-017
- instance_key: authz:src/api/export.ts:84
- affected_locations:
  - entrypoint/wrapper: src/api/export.ts:84
  - root_control: src/authz/project_scope.ts:52
  - sink: src/services/export_service.ts:133

### Attack Path
1. Authenticated attacker submits `project_id` for another tenant.
2. API handler forwards request to export service.
3. No tenant ownership check at object-level guard.
4. Export service returns data for unauthorized tenant.

### Rendered Facts
- in_scope: yes
- attacker_role: authenticated tenant user
- boundary_crossed: tenant isolation boundary
- required_preconditions: valid account and known target project id
- impacted_asset: cross-tenant project export data

### Counterevidence Checked
- role check exists at handler, but no object ownership verification.
- no downstream re-check in export service.

### Severity and Policy
- calibrated_severity: high
- policy_decision: report
- rationale: cross-tenant sensitive data exposure with reliable repro path
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
