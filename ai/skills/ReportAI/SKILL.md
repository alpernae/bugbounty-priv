---
name: reportai
description: Use when generating a formal security report for validated security findings or when the user explicitly asks for a security report. Do not use for initial vulnerability discovery, speculative findings, or unverified issues.
---

# Instructions

Generate formal security reports only for validated findings.

## Mandatory Rules

- Never create reports for unverified, speculative, or partially confirmed issues
- Never use this skill for vulnerability discovery
- Do not recommend remediation, mitigations, or fixes unless explicitly requested
- Focus only on documenting:
  - vulnerability summary
  - affected component
  - technical impact
  - exploitation requirements
  - attack scenario
  - reproduction steps
  - security impact
  - severity reasoning
  - supporting evidence

## Report Source

Validated findings must come from:
- `/audit-scans`
- isolated verification scans
- user-confirmed vulnerabilities

## Output Location

Export reports to:

`security-reports/[vulnerability-class]/[report-title].md`

## References

Load only when needed:

- [Report Template](references/report-template.md)