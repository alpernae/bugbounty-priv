# References Entrypoint

Use this file as the first reference when the `source-code-skill` is active.

## Goal

Guide Codex through authorized source-code security analysis with practical vulnerable and safe examples while avoiding report noise.

## Core scan phase skills

This repository vendors the scan-phase skills inside `references/` so they can be treated as core modules during source-code security work:

- `security-scan/SKILL.md` (orchestrator)
- `threat-model/SKILL.md`
- `finding-discovery/SKILL.md`
- `validation/SKILL.md`
- `attack-path-analysis/SKILL.md`
- `fix-finding/SKILL.md`

Use `scan-artifacts.md` for the default artifact layout and report paths.

## How to use references

1. Identify the suspected vulnerability class.
2. Open the matching folder in `references/`.
3. Read the folder `README.md`.
4. Compare the target code against the five language examples.
5. Confirm source-to-sink reachability.
6. Apply [False Positive Reduction](FALSE_POSITIVE_REDUCTION.md).
7. Use [Example Quality](EXAMPLE_QUALITY.md) before adding or trusting a snippet.
8. Use [Corpus Lessons](CORPUS_LESSONS.md) to calibrate realistic vulnerable and safe patterns.
9. Promote confirmed findings only after isolated verification, then write durable artifacts only when the user asks for them.

## Example folder contract

Every vulnerability reference uses:

```text
README.md
examples/
  javascript-typescript/vulnerable.ts
  javascript-typescript/safe.ts
  python/vulnerable.py
  python/safe.py
  java/vulnerable.java
  java/safe.java
  php/vulnerable.php
  php/safe.php
  go/vulnerable.go
  go/safe.go
```

## Review priority

Prioritize:
1. Authz and tenant boundary bugs.
2. RCE and command execution.
3. Injection.
4. SSRF and file parser flows.
5. Secret exposure.
6. Token/OAuth/session flaws.
7. Business logic and race conditions.
8. Configuration and dependency risks.

## Usually suppress or downgrade

Brute force, user enumeration, and rate-limit-only issues usually need explicit scope permission and meaningful impact before becoming report-ready. Treat them as hypotheses unless the user asks for that class or the program policy accepts them.

## Helper scripts

- `scripts/source_candidate_triage.py --root <repo>`: surface source/sink/control evidence and likely false-positive blockers.
- `scripts/example_quality_lint.py <skill-root>`: find generic comments, missing vulnerable/safe pairs, and obvious example mismatches.
- `scripts/secret_candidate_scanner.py <repo>`: local-only secret candidate scan with redacted output.
