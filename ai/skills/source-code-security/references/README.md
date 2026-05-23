# Source Code Security References

## Purpose

This directory is the detailed reference corpus for `source-code-security`. Use it when a scan needs concrete source-to-sink checklists, vulnerable/safe examples, false-positive reduction rules, scan artifact paths, or phase-specific security workflows.

## Workflow

1. Start with `REFERENCES.md` to choose the relevant vulnerability family.
2. Load `FALSE_POSITIVE_REDUCTION.md` before promoting any candidate.
3. Use `scan-artifacts.md` when the user asks for durable scan output.
4. Open only the issue-specific `README.md` files needed for the current candidate.
5. Use phase references under `security-scan/`, `finding-discovery/`, `validation/`, `attack-path-analysis/`, and `fix-finding/` for workflow depth.

## Scoring Standard

A strong reference should include:

- purpose and when to use it
- workflow or checklist
- false-positive and suppression guidance
- validation or proof strategy
- vulnerable/safe examples or output template
- impact and remediation guidance
- expected output fields

## Output Shape

When a reference supports a finding, the final candidate should name the reference and include source, closest control, sink, evidence, counterevidence, impact, confidence, and remediation.
