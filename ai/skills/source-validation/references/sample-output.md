# Sample Validation Output

```markdown
## Validation: cand-017 (Cross-tenant export authorization bypass)

- confidence: high
- method: realistic interface reproduction

### Rubric
- [x] Attacker controls object identifier
- [x] Request reaches protected export action
- [x] Object-level tenant check missing/bypassed
- [x] Unauthorized data returned
- [x] Behavior repeats in clean session

### Evidence
- Account A token exported project belonging to Account B tenant.
- Response contained tenant-B project fields.
- No ownership check before export dispatch.

### Remaining Uncertainty
- None material for reportability.

### Next Step
- Proceed to attack-path analysis and severity calibration.
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
