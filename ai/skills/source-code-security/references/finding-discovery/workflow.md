---
name: finding-discovery
description: Discovers candidate source-code security vulnerabilities by inspecting repository evidence, tracing attacker-controlled input to security-sensitive sinks, and separating plausible findings from scanner noise. Identifies injection flaws, authz bypasses, insecure deserialization, path traversal, SSRF, hardcoded credentials, insecure configuration, unsafe API usage, CVE/advisory reachability, and missing security controls. Use when Codex is in the discovery phase, or when the user asks to find vulnerabilities, discover security issues, triage insecure code, run static analysis, investigate SAST results, or perform security audit discovery.
metadata:
  short-description: Discover security candidates
---

# Security Finding Discovery

## Objective

Produce technically plausible candidate findings grounded in code evidence. Discovery is not final validation and not final severity.

Use `../../references/scan-artifacts.md` for default artifact paths. If the user gives explicit paths, use those.

## Scope Routing

| Scan type | Procedure |
|---|---|
| PR, commit, branch, patch | `../security-scan/references/code-diff-scan.md` |
| Repository-wide | `../security-scan/references/repository-wide-scan.md` |
| CVE/advisory-led | Use seed research artifacts and preserve exact seeded rows. |

## Workflow

1. Load threat model and scan scope.
2. Inspect target files plus supporting files that determine reachability, guards, and sinks.
3. Enumerate candidates with a concrete `source -> closest control -> sink` chain.
4. Expand independently reachable sibling instances affected by the same changed root control or shared sink.
5. Demote or discard any candidate missing a concrete source, control, sink, or plausible impact.
6. Record strongest counterevidence for each remaining candidate.
7. Save discovery output using the finding discovery report path.

Feedback loop:

| If | Action |
|---|---|
| Candidate lacks attacker control | Demote to `suppressed` or `not_applicable`. |
| Candidate lacks sink or broken control | Keep as note only, not validation input. |
| Candidate is scanner-only | Trace manually or suppress. |
| Candidate has repeated independent instances | Split into separate candidate rows. |

## References

- `references/discovery-checklist.md` - mandatory quality gates for each candidate.
- `references/finding-bar.md` - vulnerability classes worth carrying forward.
- `references/sample-output.md` - complete candidate output example.

## Inline Candidate Example

```markdown
## Candidate: Unsafe YAML load in webhook import

- candidate_id: cand-004
- status: unverified suspicion
- affected_locations:
  - entrypoint/wrapper: app/webhooks/imports.py:42
  - sink: app/importers/yaml_loader.py:88
- instance_key: deserialization:app/importers/yaml_loader.py:88
- attacker_source: webhook body controlled by integration partner
- vulnerable_sink: `yaml.load(payload)` with default loader
- closest_control: signature check exists, but no schema restriction before parsing
- impact: crafted payload may instantiate unsafe objects or crash import worker
- why_plausible: webhook route forwards raw body directly to YAML importer
- counterevidence: route requires signature, but signer is external tenant-configured integration
- validation_recommended: yes
- taxonomy: [CWE-502]
- proof_gaps: need confirm configured YAML library behavior and route reachability
```

## Output Contract

For each candidate include:

- title
- affected locations with labels: `entrypoint/wrapper`, `root_control`, `sink`, `concrete_implementation`
- instance key for repository-wide scans
- attacker-controlled source
- vulnerable sink or broken control
- closest apparent control and why it is absent, bypassed, mis-scoped, or incomplete
- impact and why the issue is plausible
- counterevidence checked
- whether validation is recommended
- taxonomy with CWE IDs when known

If no plausible candidates remain, return a no-findings result and list what surfaces were checked.

## Hard Rules

- Use tools to inspect files before deciding.
- Stay anchored to scope.
- Do not turn discovery into validation.
- Do not group separate high-impact proof tuples into one candidate.
- Save a visible discovery report when artifact paths are being used.
