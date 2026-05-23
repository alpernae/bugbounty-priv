# Scan Artifacts

This file defines the default on-disk layout for security scan artifacts (threat models, per-phase reports, PoCs, and repository-wide coverage/ledger outputs).

Use these conventions only when the user has asked for a scan that produces durable artifacts, or when the user explicitly asks you to write a report/file. Do not create artifact directories by default for ad-hoc questions.

## Resolution Rules

1. If the user provides explicit paths (e.g., `scan_dir`, `artifacts_dir`, or specific output filenames), use the user-provided paths.
2. Otherwise resolve these values:

- `repo_root`: the root directory of the repository being scanned.
- `repo_name`: the basename of `repo_root` (or the repository name from git metadata when it is clearly available).
- `security_scans_dir`: `<repo_root>/security_scans`
- `scan_id`: `YYYYMMDD_HHMMSS` (pick a collision-resistant id; UTC is fine).
- `repo_scan_dir`: `<security_scans_dir>/<repo_name>`
- `scan_dir`: `<repo_scan_dir>/scans/<scan_id>`
- `artifacts_dir`: `<scan_dir>/artifacts`

Create directories only when you are actually going to write artifacts.

## Repository-Scoped Artifact

Persisted across scans:

- Repository threat model path: `<repo_scan_dir>/repo_threat_model.md`

## Per-Scan Artifacts

All per-scan artifacts live under `<scan_dir>`.

### Phase Outputs

- Per-scan threat model (copied from the repository threat model, unchanged): `<scan_dir>/threat_model.md`
- Finding discovery report: `<scan_dir>/finding_discovery.md`
- Validation report: `<scan_dir>/validation.md`
- Attack-path analysis report: `<scan_dir>/attack_path_analysis.md`
- Fix report (only when a fix phase happens): `<scan_dir>/fix_finding.md`
- Final scan report (assembled last): `<scan_dir>/final_report.md`

### Repository-Wide Scan Artifacts

Only when the scan scope is repository-wide:

- Runtime inventory: `<scan_dir>/runtime_inventory.md`
- Seed research (only when seed/advisory hints exist): `<scan_dir>/seed_research.md`
- Exhaustive file checklist: `<scan_dir>/exhaustive-file-checklist.md`
- Repository coverage ledger: `<scan_dir>/repository_coverage_ledger.md`

## Artifact Subdirectories

All supportive artifacts live under `<artifacts_dir>`.

- Validation artifacts directory: `<artifacts_dir>/validation/`
  - PoCs, crafted inputs, logs, and any disposable build/test copies used to validate findings
- Optional build outputs: `<artifacts_dir>/build/`
- Optional logs: `<artifacts_dir>/logs/`

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
