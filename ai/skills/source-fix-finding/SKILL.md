---
name: source-fix-finding
description: Fixes and verifies validated or plausible security vulnerabilities by analyzing the source/control/sink path, applying a minimal code change, adding regression tests, and proving the original exploit no longer works. Use when the user asks to fix a vulnerability, remediate a CVE, patch a security bug, repair an exploit path, address a SAST finding, add a security regression test, or verify a security issue is fixed.
metadata:
  short-description: Fix and verify security finding
---

# Fix Finding

## Objective

Turn a concrete security finding into a minimal, validated code change. If the issue is already fixed, prove that with focused validation and report that no code change was needed.

## Inputs

Extract or reconstruct:

- title and affected component
- attacker-controlled source
- closest missing/bypassed control
- vulnerable sink or protected state
- expected security invariant
- impact and preconditions
- existing PoC, reproducer, test, or validation evidence
- affected files and line references

Ask the user only when product policy is truly unknowable from repository evidence.

## Workflow

1. Scope the fix to the smallest boundary that should enforce the invariant.
2. Reproduce or encode the issue before changing code when feasible.
3. Check existing validators, authz helpers, parsers, sanitizers, and test patterns.
4. Apply the smallest behavior change that blocks the exploit path.
5. Add regression coverage for the exploit condition and positive coverage for allowed behavior.
6. Run focused tests, then relevant broader checks for touched files.
7. Re-run the original PoC or test and confirm it fails safely.
8. Search nearby sibling paths for bypasses.
9. Report changed files, validation commands, and remaining risk.

## Fix Example

Finding:

```markdown
Cross-tenant export allows Account A to request Account B project id.
Source: JSON `project_id`
Missing control: tenant ownership check
Sink: export service returns project data
```

Minimal fix pattern:

```typescript
const project = await projects.get(projectId);
if (!project || project.tenantId !== user.tenantId) {
  throw new ForbiddenError("project is not available");
}
return exportProject(project.id);
```

Regression test shape:

```typescript
it("rejects exports for projects outside the caller tenant", async () => {
  const response = await request(app)
    .post("/api/export")
    .set("Authorization", tokenFor(tenantAUser))
    .send({ project_id: tenantBProject.id });

  expect(response.status).toBe(403);
});
```

## Validation Commands

```bash
npm test -- export_cross_tenant.spec.ts
pytest tests/security/test_export_authz.py -q
go test ./internal/export -run TestCrossTenantExport
```

Use the repository's actual tools and documented setup. Do not weaken security controls to make tests pass.

## Completion Checklist

| Check | Required result |
|---|---|
| Original issue restated | Source, control, sink, and impact are clear. |
| Fix boundary | The invariant is enforced at the right layer. |
| Regression coverage | Exploit condition fails safely. |
| Positive coverage | Legitimate behavior still works. |
| Revalidation | Original PoC/test no longer succeeds. |
| Bypass review | Nearby siblings or alternate routes were checked. |

## Output Contract

Include:

- summary of the fix
- files changed
- tests or validation artifacts added
- commands run and pass/fail results
- how the original issue was shown not to reproduce
- whether code changes were needed
- remaining uncertainty or skipped validation

Reference:

- `references/sample-output.md` - report shape for remediation outcomes.

## Hard Rules

- Do not claim the issue is fixed until changed code and the original path are both checked.
- Do not broaden into unrelated cleanup.
- Do not weaken authn, authz, tenant isolation, input validation, sandboxing, or logging.
- Do not remove unrelated user changes.
- State proof gaps plainly when validation is blocked.
