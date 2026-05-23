---
name: source-code-security
description: Authorized source-code security review and SAST triage for web, API, backend, CLI, worker, parser, configuration, IaC, cloud, dependency, and supply-chain code. Identifies SQL injection, XSS, path traversal, SSRF, unsafe deserialization, authz bypass, hardcoded secrets, insecure configuration, CVE/advisory reachability, and dangerous API usage. Use when the user asks for a security audit, code scan, static analysis, find vulnerabilities, security bugs, CVE review, false-positive triage, or exploitability review in source code.
metadata:
  short-description: Source-code security review
---

# Source Code Security

Use this as the top-level orchestrator for authorized source-code security work. Treat scanner output, grep hits, agent claims, and prior notes as leads until repository evidence proves reachability, attacker control, broken control, and impact.

## Architecture

Use separate phase skills for execution and detailed references for depth:

| Need | Load |
|---|---|
| Full PR, commit, branch, patch, or repository scan | `../source-security-scan/SKILL.md` |
| Build or reuse repository threat model | `../source-threat-model/SKILL.md` |
| Discover candidate vulnerabilities | `../source-finding-discovery/SKILL.md` |
| Verify candidates and reduce false positives | `../source-validation/SKILL.md` |
| Trace exploit path and calibrate severity | `../source-attack-path-analysis/SKILL.md` |
| Remediate and verify a finding | `../source-fix-finding/SKILL.md` |

Keep phases separate. Discovery produces candidates, validation proves or suppresses them, and attack-path analysis decides final reportability and severity.

## Core Workflow

1. Confirm scope and scan target.
2. Build or load a threat model covering assets, inputs, trust boundaries, and invariants.
3. Inventory routes, parsers, jobs, CLIs, configs, dependencies, cloud/IaC, and privileged workflows.
4. Discover candidates with `source -> closest guard -> sink` evidence.
5. Validate candidates with the strongest bounded method available.
6. Trace attack paths, challenge counterevidence, and calibrate severity.
7. Report only candidates that survive validation and policy checks.

Validation checkpoints:

| Checkpoint | Continue only if |
|---|---|
| After inventory | Main runtime surfaces and trust boundaries are known, or unknowns are explicitly recorded. |
| After discovery | Each candidate has concrete source, guard/control, sink, impact, and proof gaps. |
| Before validation | Scanner-only or duplicate leads are suppressed or demoted. |
| After validation | Surviving findings have evidence, confidence, and remaining uncertainty. |
| Before final report | Severity follows attack-path facts, not bug-class reputation. |

## False-Positive Gates

Promote a candidate only when all gates are supported:

| Gate | Required evidence |
|---|---|
| Reachability | A route, resolver, job, parser, CLI, webhook, plugin, config, or deployed workflow can execute the code. |
| Attacker control | A lower-privileged user, tenant, integration, file, queue, callback, dependency, or external actor controls the relevant value. |
| Sensitive sink or broken control | The value reaches authorization, identity, tenancy, secrets, filesystem, network, parser, command, template, storage, cache, package, cloud, or deployment behavior. |
| Missing effective control | Existing validation, escaping, authz, parameterization, canonicalization, parser hardening, signature check, framework default, or policy does not stop the exact path. |
| Impact | The path can expose, modify, execute, persist, bypass, or deny something security-relevant. |

If a gate is missing, keep the item as `unverified suspicion`, `suppressed`, `not applicable`, or `blocked`.

## Reference Loading

Start with:

- `references/REFERENCES.md` - index of vulnerability families and example banks.
- `references/FALSE_POSITIVE_REDUCTION.md` - promotion and suppression rules.
- `references/scan-artifacts.md` - scan artifact layout when the user asks for durable files.

Then load only the issue family you need, such as `references/sqli/`, `references/ssrf/`, `references/xss/`, `references/authorization/`, `references/files/`, `references/crypto/`, or `references/dependencies/`.

## Script Examples

Use scripts when they help prioritize, but do not treat script output as proof:

```bash
python scripts/source_inventory.py --root .
python scripts/source_candidate_triage.py --root . --format markdown
python scripts/secret_candidate_scanner.py --root . --redact
```

Expected use:

| Script | Use for |
|---|---|
| `source_inventory.py` | Fast language/framework/entrypoint map. |
| `source_candidate_triage.py` | Source/sink/control hints for noisy SAST or grep output. |
| `secret_candidate_scanner.py` | Local redacted secret-candidate triage. |

## Example Finding Output

```markdown
## Candidate: Tenant export bypass through missing object-scope check

- status: unverified suspicion
- confidence: medium
- affected: src/api/export.ts:84, src/services/export_service.ts:133
- source: `project_id` in authenticated JSON request body
- trust boundary: tenant user controls object id crossing tenant boundary
- closest guard: role check in `requireUser`, but no project ownership check
- sink: export service reads and returns project data by id
- missing control: tenant-scoped authorization before export dispatch
- exploitability: attacker needs a valid account and another tenant's project id
- counterevidence checked: no downstream ownership check found in export service
- validation method: Account A vs Account B request replay recommended
- impact: cross-tenant sensitive project export
- severity rationale: likely high if replay confirms data exposure
- proof gaps: runtime behavior and object id predictability still unverified
- references used: references/authorization/idor-bola/README.md
```

## Output Contract

For each candidate or finding include:

- title
- status and confidence
- affected file/function/route/config
- source, trust boundary, closest guard, and sink
- missing or bypassed control
- exploitability reasoning and prerequisites
- counterevidence checked
- validation method and evidence
- impact and severity rationale
- remaining proof gaps
- references used
