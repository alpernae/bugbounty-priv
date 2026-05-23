# Sample Fix Report

## Purpose

Use this reference as the output template after fixing or disproving a security finding.

## Workflow

1. Restate the finding in source/control/sink terms.
2. Summarize the minimal fix or explain why no code change was needed.
3. List tests or validation artifacts.
4. Show commands and results.
5. State how the original issue no longer reproduces.
6. Record remaining risk.

## Example

```markdown
## Security Fix Result

- finding: Cross-tenant export authorization bypass
- outcome: fixed
- files_changed:
  - src/authz/project_scope.ts
  - src/api/export.ts
- tests_added:
  - tests/authz/export_cross_tenant.spec.ts

### Commands Run
- npm test -- tests/authz/export_cross_tenant.spec.ts  (pass)
- npm test -- tests/authz/export_owner.spec.ts         (pass)

### Validation
- Original repro with Account A on Account B project now returns 403.
- Positive path for owner account still returns 200.

### Counterevidence And Proof Gaps
- Nearby export routes were checked for direct service calls.
- No remaining bypass was found in the touched scope.

### Remediation
- Object-level tenant ownership is enforced before export dispatch.

### Remaining Risk
- No material residual risk identified for this path.
```

## Output Fields

Include summary, changed files, tests, commands, original-repro result, positive-control result, sibling bypass review, and remaining uncertainty.
