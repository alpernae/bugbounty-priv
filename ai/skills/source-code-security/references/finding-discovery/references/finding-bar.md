# Finding Bar

## Purpose

Use this reference during finding discovery to decide which candidate leads are worth validating. It prevents scanner noise, best-practice comments, and duplicate variants from crowding out evidence-backed vulnerabilities.

## Workflow

1. Confirm the candidate has a realistic entrypoint.
2. Confirm attacker control crosses a trust boundary.
3. Confirm a missing or bypassed control is tied to a sensitive sink or protected decision.
4. Confirm plausible security impact.
5. Record counterevidence before handing the candidate to validation.

## Prefer Candidates With

- authorization bypass or tenant isolation break
- account takeover, auth bypass, or token confusion
- injection with meaningful sink impact
- SSRF with realistic internal, metadata, or callback impact
- sensitive data exposure across a user, tenant, role, or trust boundary
- command/code execution, dangerous parser behavior, deserialization, sandbox escape, or supply-chain compromise

## Suppress Or Downgrade

- scanner-only alerts with no reachability
- unreachable, test-only, example-only, or dead code
- missing headers or configuration hygiene without a concrete exploit path
- duplicate variants of one root issue
- findings requiring equivalent admin/root/code-execution privilege unless the privilege delta is the issue

## Validation Handoff Example

```markdown
- candidate_id: cand-012
- family: authz
- source: `project_id` in authenticated request
- control: missing object ownership check
- sink: project export returns data
- impact: cross-tenant data exposure
- counterevidence: role check exists but no tenant check before sink
- validation_next_step: Account A vs Account B replay
```

## Output Fields

Carry forward title, source, control, sink, impact, counterevidence, validation recommendation, and proof gaps.
