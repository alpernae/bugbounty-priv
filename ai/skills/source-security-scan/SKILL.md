---
name: source-security-scan
description: Run a full source-code security scan or security code review of a pull request, commit, branch, patch, working-tree diff, or repository. Orchestrates threat modeling, finding discovery, false-positive validation, attack-path analysis, severity calibration, and final markdown reporting. Use when the user asks for a security audit, PR security review, code scan, repository-wide vulnerability scan, static analysis, CVE reachability review, or secure code review.
metadata:
  short-description: Run source-code security scan
---

# Security Scan

Use this as the top-level orchestrator for full source-code security scans. Keep the scan phases separate and preserve handoff artifacts between phases.

## Phase Table

| Phase | Skill | Required output before next phase |
|---|---|---|
| 1 | `../source-threat-model/SKILL.md` | Repository threat model or provided authoritative model. |
| 2 | `../source-finding-discovery/SKILL.md` | Candidate inventory or explicit no-findings result. |
| 3 | `../source-validation/SKILL.md` | Validation assessment and closure table for candidates. |
| 4 | `../source-attack-path-analysis/SKILL.md` | Attack-path facts, severity, and final policy decision. |
| 5 | `references/final-report.md` | Final report assembled from surviving findings. |

Use `../source-code-security/references/scan-artifacts.md` to resolve default artifact paths. If the user provides explicit paths, use those.

## Execution Plan

1. Resolve scan target:
   - PR: base branch vs current `HEAD`
   - commit: target commit vs parent or requested baseline
   - branch: merge-base to head
   - working tree: local diff against requested base
   - repository-wide: entire checked-out repository
2. Run threat model at repository scope unless the user explicitly requests narrower scope.
3. Run discovery:
   - diff scans stay anchored to changed code plus supporting files
   - repository-wide scans follow `references/repository-wide-scan.md`
4. Stop early only when discovery has a well-supported no-findings result.
5. Validate each candidate with bounded dynamic proof or focused static trace.
6. Run attack-path analysis for validated or still-plausible candidates.
7. Assemble final markdown report from validation closure rows and attack-path output.

## Checkpoints

| Point | Verify |
|---|---|
| Before discovery | Threat model covers assets, trust boundaries, attacker inputs, and invariants. |
| Before validation | Each candidate has source, closest control, sink/broken control, and impact. |
| Before attack-path analysis | Validation status, evidence, and proof gaps are explicit. |
| Before final report | Only reportable candidates survive policy and counterevidence checks. |

## Diff vs Repository-Wide Behavior

Diff-scoped scans:

- Start from changed files and supporting files needed to understand behavior.
- Expand to sibling instances only when the diff changes a shared control, wrapper, sink, route pattern, parser, auth helper, or template pattern.
- Use unchanged siblings as negative controls unless the diff makes them newly vulnerable.

Repository-wide scans:

- Follow `references/repository-wide-scan.md`.
- Preserve coverage ledger rows as `reportable`, `suppressed`, `not_applicable`, or `deferred`.
- Keep seeded CVE/advisory/root-control rows open until exact local code evidence closes them.

## Final Report Preview

```markdown
# Security Scan Report

Target: <PR/commit/branch/repository>
Scope: <diff-scoped or repository-wide>
Threat model: <artifact path or provided source>

## Findings

### 1. <Title>
- Severity: <critical/high/medium/low/info>
- Status: isolated verified finding
- Affected locations: <file:line>
- Attack path: <short source -> control -> sink chain>
- Evidence: <test, PoC, trace, or code evidence>
- Impact: <security consequence>
- Remediation: <focused fix guidance>

## Suppressed / Not Applicable
- <candidate id>: <counterevidence>

## Deferred Coverage
- <area>: <reason and recommended next step>
```

## Hard Rules

- Do not collapse phases together.
- Do not report scanner-only leads.
- Do not skip validation for plausible high-impact candidates unless validation is blocked and the proof gap is explicit.
- Do not drop exact root-control affected locations during final reporting.
- Avoid broad unbounded scans when a targeted trace can answer the question.
