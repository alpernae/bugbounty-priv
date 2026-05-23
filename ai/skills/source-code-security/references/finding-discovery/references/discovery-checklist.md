# Discovery Checklist

## Purpose

Use this checklist to keep discovery evidence-based before validation begins. A candidate should leave discovery with enough detail for another reviewer to reproduce the reasoning.

## Workflow

1. Identify the entrypoint and trust boundary.
2. Trace attacker-controlled input to the closest guard.
3. Continue from guard to sink or protected decision.
4. Check sibling instances affected by the same control or shared helper.
5. Record counterevidence and proof gaps.
6. Suppress weak leads before validation.

## Candidate Quality Gates

- Reachability is tied to a route, parser, job, CLI, hook, config, dependency, or deployment path.
- Attacker control is concrete, not assumed.
- The closest control is identified and evaluated.
- The sink or protected decision has security impact.
- Counterevidence has been actively searched.

## False-Positive Checks

Suppress when code is unreachable, test-only, guarded on every path, public by design, or requires equivalent privilege. Downgrade when the issue is hygiene-only and lacks concrete impact.

## Example Candidate

```markdown
- title: Unsafe YAML import reachable from webhook
- source: signed webhook body from tenant-configured integration
- closest_control: signature check only, no schema restriction
- sink: `yaml.load` default loader
- impact: unsafe object construction or worker crash
- counterevidence: integration signature limits source but does not make payload trusted
```

## Remediation Prompt

Name the control the later fix should add: safe parser configuration, schema validation, allowlist, authorization, parameterization, canonicalization, or output encoding.
