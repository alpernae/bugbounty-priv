# Example Quality

Use this when writing or judging vulnerable and safe examples. The goal is realistic contrast, not toy snippets.

## Required qualities

- Use a recognizable framework or library shape: route handler, controller, resolver, job, parser, service method, Terraform resource, Kubernetes manifest, or dependency manifest.
- Show the source and sink in the same reachable flow unless the example is explicitly about a shared helper.
- Make the vulnerable example fail because of a precise missing control, not because the code is intentionally nonsensical.
- Make the safe example apply the control at the right layer and keep the same business behavior.
- Include enough surrounding code to understand preconditions, but avoid fake comments that tell the reader what to think.
- Prefer real mitigation APIs: prepared statements, contextual escaping, canonical path checks, `shell=False` with argument arrays, parser hardening, strict allowlists, token issuer/audience checks, and signature verification.

## Slop indicators

Treat examples as low quality if they contain:

- `TODO`, `TBD`, "Review note", "sanitize here", or comment-only fixes.
- A vulnerable snippet with no attacker-controlled source.
- A sink name without realistic framework context.
- A safe snippet that only strips characters with regex, escapes after the wrong parser has already run, or catches and ignores errors.
- An example where vulnerable and safe code are nearly identical except for comments.
- A category mismatch, such as a zip-slip reference that only demonstrates normal file download path traversal.

## Safe-pattern traps

- SQL: escaping strings is not equivalent to parameter binding.
- Command injection: `escapeshellarg` is not enough if the whole command string remains attacker-selected.
- SSRF: checking the hostname before following redirects is incomplete.
- Path traversal: `startsWith` is unsafe unless the normalized path and root include a path-separator boundary.
- Zip slip: checking the raw zip entry name is insufficient; check the normalized destination path after joining with the extraction root.
- XSS: HTML escaping is not sufficient for JavaScript, URL, CSS, or SVG contexts.
- JWT: decoding without verification is never an auth check.
- Secrets: `REDACTED`, `example`, `dummy`, and public keys are not live secrets by themselves.

## Adding examples

When adding a vulnerable/safe pair:

1. Name the source, sink, and missing control in the reference README.
2. Keep the vulnerable example exploitable with one small input change.
3. Keep the safe example runnable and preserve intended behavior.
4. Run `scripts/example_quality_lint.py <skill-root>` and review warnings before considering the example done.

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
