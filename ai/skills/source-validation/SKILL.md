---
name: source-validation
description: Validates candidate security findings by triaging false positives, verifying exploit reachability, checking CVE/advisory applicability, reproducing vulnerable behavior when feasible, and recording proof gaps. Use when Codex is in the validation phase, or when the user asks "is this finding real", validate vulnerability, confirm exploitability, false positive check, security finding verification, validate CVE, SAST triage, or prove/suppress a candidate.
metadata:
  short-description: Validate security findings
---

# Security Validation

## Objective

Turn candidate findings into evidence-backed validation outcomes. Prefer bounded reproduction or falsification when feasible; use focused static trace when runtime setup is unavailable or disproportionate.

Use `../source-code-security/references/scan-artifacts.md` for default validation artifact paths.

## Method Routing

| Candidate type | First method | Fallback |
|---|---|---|
| Authz or tenant bypass | Account A vs Account B request/test | Static trace of object ownership checks |
| Injection | Minimal semantic delta or harmless timing/error proof | Source-to-query/sink trace |
| SSRF | Owned callback/local listener | URL parsing and egress-control trace |
| Parser/crash/DoS | Minimal fixture plus test/debug run | Static guard and exception containment trace |
| Memory safety | ASan/valgrind/debugger with PoC | Focused code trace with proof gap |
| CVE/advisory | Version plus vulnerable code path | Seeded row closure with exact counterevidence |

## Command Examples

```bash
curl -i -X POST "$BASE/api/export" -H "Authorization: Bearer $TOKEN_A" -d '{"project_id":"tenant_b_project"}'
ASAN_OPTIONS=detect_leaks=0 npm test -- export_cross_tenant.spec.ts
valgrind --error-exitcode=99 ./parser_fixture ./pocs/crash.yml
gdb -q -batch -ex run -ex bt -ex quit --args ./parser_fixture ./pocs/crash.yml
```

Use commands as templates; adapt them to the actual repository and keep payloads safe.

## Workflow

1. Write a validation rubric with up to five criteria.
2. Restate source, trust boundary, closest control, sink, preconditions, and expected safe behavior.
3. Choose the strongest feasible validation method from the method table.
4. Run bounded dynamic proof when practical.
5. If runtime proof is blocked, document setup attempts and use focused static trace.
6. Decide disposition: `reportable`, `suppressed`, `not_applicable`, or `deferred`.
7. Save validation notes and artifacts when artifact paths are in use.

Decision checkpoints:

| Check | Continue if |
|---|---|
| Rubric complete | The criteria would prove or falsify the claim. |
| Runtime path available | Build/test/replay is bounded and safe. |
| Runtime blocked | The exact blocker and fallback evidence are recorded. |
| Disposition chosen | Evidence and counterevidence support the closure row. |

## Output Example

```markdown
## Validation: cand-004 Unsafe YAML load in webhook import

- confidence: medium-high
- method: focused unit fixture plus code trace
- disposition: reportable

### Rubric
- [x] Attacker-controlled webhook body reaches importer
- [x] YAML parser uses unsafe loader
- [x] No schema validation occurs before parse
- [ ] Full end-to-end webhook replay completed
- [x] Impact is at least worker crash or unsafe object construction

### Evidence
- `app/webhooks/imports.py:42` passes raw body to importer.
- `app/importers/yaml_loader.py:88` calls `yaml.load` without safe loader.
- Test fixture triggers unsafe constructor path locally.

### Counterevidence
- Signature check authenticates integration source, but tenant-configured integration is still a trust boundary.

### Proof Gap
- Production webhook routing was not started locally; end-to-end replay remains deferred.
```

## Closure Table Columns

For repository-wide scans include:

| Column | Meaning |
|---|---|
| ledger row id | Coverage or seed row id. |
| instance key | Stable `<family>:<file>:<line>` key. |
| root-control file:line | Core broken control location. |
| entrypoint/source | Reachability source. |
| sink/control | Sensitive sink or broken control. |
| disposition | `reportable`, `suppressed`, `not_applicable`, `deferred`. |
| counterevidence or proof gap | Why it closes or remains uncertain. |
| survives | `yes`, `no`, or `uncertain`. |

## References

- `references/validation-guidance.md` - detailed validation rules.
- `references/validation-methods.md` - method selection table.
- `references/sample-output.md` - sample validation output.

## Hard Rules

- Do not imply validation happened when it did not.
- Do not treat setup errors as counterevidence.
- Keep validation effort bounded but serious for high-impact candidates.
- Preserve exact root-control and seed-anchor lines.
- Calibrate confidence from evidence, not bug-class reputation.
