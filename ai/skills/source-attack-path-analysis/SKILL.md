---
name: source-attack-path-analysis
description: Traces security findings from untrusted source to sensitive sink, maps data flow and exploit steps, checks counterevidence, calibrates severity from exploitability and impact, and decides final reportability. Use when Codex is in the attack-path phase, or when the user asks for taint analysis, data flow review, vulnerability path, exploitability assessment, severity calibration, attack chain, impact analysis, or source-to-sink proof.
metadata:
  short-description: Analyze attack paths and severity
---

# Security Attack Path Analysis

## Objective

Convert validated or still-plausible findings into explicit attacker stories, structured attack-path facts, severity calibration, and a final reportability decision.

Use `../source-code-security/references/scan-artifacts.md` for default report paths.


## Input Resolution

Load inputs in this order:

1. Threat model: repository threat model path from `../source-code-security/references/scan-artifacts.md`, or the user-provided threat model.
2. Validation output: validation report, closure table, candidate notes, or explicit finding details from the user.
3. Candidate evidence: affected file lines, source, closest control, sink, reproduction notes, proof gaps, and counterevidence.

If no artifact path exists, ask only for the missing input that blocks analysis. Do not fabricate threat model facts or validation evidence.

## Minimum Facts

Render these facts inline for every surviving path: attacker role, entrypoint, controlled value or action, boundary crossed, missing or bypassed control, sink or asset, impact, and strongest counterevidence.

Use `references/attack-path-facts.md` only when you need field definitions or a structured template.

## Severity Cue

Use `references/severity-policy.md` for thresholds. Keep Critical/High only when a realistic in-scope attacker reaches a meaningful security impact; downgrade correctness-only, self-only, equivalent-privilege, or unreachable paths.

## Workflow

1. Load threat model, validation output, and candidate evidence.
2. Confirm the affected code is in scope and belongs to a real product surface or meaningful production workflow.
3. Build the attack path:
   - entrypoint and attacker role
   - trust boundary crossed
   - controlled value or action
   - closest missing/bypassed control
   - sensitive sink or protected state
   - security impact
4. Challenge the path with strongest counterevidence.
5. If counterevidence defeats the path, mark `suppressed` and skip severity escalation.
6. If the path survives, render attack-path facts and calibrate severity.
7. Apply final policy decision: `report`, `downgrade`, `ignore`, or `defer`.

## References

- `references/attack-path-facts.md` - structured fact fields.
- `references/severity-policy.md` - severity and policy matrix.
- `references/sample-output.md` - complete attack-path report example.

## Inline Example

```markdown
## Attack Path: Cross-tenant export authorization bypass

- candidate_id: cand-017
- affected_locations:
  - entrypoint/wrapper: src/api/export.ts:84
  - root_control: src/authz/project_scope.ts:52
  - sink: src/services/export_service.ts:133

### Steps
1. Authenticated tenant user sends another tenant's `project_id`.
2. API handler checks only that the caller is logged in.
3. Export service loads project data by id without tenant ownership check.
4. Response returns another tenant's export data.

### Attack-Path Facts
- attacker_role: authenticated user
- boundary_crossed: tenant isolation
- preconditions: valid account and target object id
- impacted_asset: project export data
- exploit_reliability: repeatable request replay

### Counterevidence
- General role check exists, but no object ownership guard was found before sink.

### Decision
- calibrated_severity: high
- final_policy_decision: report
- rationale: cross-tenant data exposure through repeatable authenticated request
```

## Checkpoints

| If | Then |
|---|---|
| No realistic attacker role | Suppress or defer with proof gap. |
| Path is internal-only and threat model excludes it | Suppress or downgrade. |
| Control exists but exact bypass is proven | Continue to severity calibration. |
| Impact is only correctness or robustness | Mark low/info or ignore. |
| Root-control line differs from wrapper | Preserve both locations. |

## Output Contract

For each surviving finding include:

- title
- candidate id, instance key, and ledger row id when available
- labeled affected lines from validation
- attack path steps
- rendered attack-path facts
- counterevidence summary
- severity calibration
- final policy decision
- proof gaps and assumptions

## Hard Rules

- Do not invent attack chains unsupported by repository evidence.
- Missing deployment metadata alone is not suppression proof.
- Keep severity calibration separate from validation.
- Do not drop root-control or seeded affected locations.
- Report only findings that survive counterevidence and policy checks.
