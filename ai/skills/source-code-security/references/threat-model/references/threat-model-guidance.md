# Threat Model Guidance

Use this guidance during threat model generation.

## Threat Model Generation Checklist

Do not restate this checklist in the final threat model output.

- Start at the repository root and use the minimum hops needed to understand the repository's real-world purpose before narrowing into critical components.
- Keep this phase at repository scope unless the user explicitly asks for a narrower target-scoped threat model.
- Ignore any reviewed commit, diff, changed files, changed directories, commit title, and scan target during threat model generation unless the user explicitly asks for narrower scope.
- Distinguish primary product or runtime code from developer-only, test-only, documentation-only, example, prototype, or one-off tooling paths.
- Identify the primary product or runtime surfaces the repository actually exposes.
- Identify the main trust boundaries and which actors sit on each side of them.
- Explicitly separate attacker-controlled, operator-controlled, and developer-controlled inputs.
- Describe common vulnerability classes that are relevant in this repository context rather than findings about the current diff.
- Call out mitigations, robustness measures, and security controls already present in the repository when they materially affect severity or scope.
- Explain when attacker stories are realistic, when they are out of scope, and when the repository's real-world usage makes a vulnerability class less important.
- Note unique security considerations for the codebase, for example:
  - authn/authz, session management, CSRF, XSS, SSRF, injections, tenant boundaries, rate limits, and secret handling for web applications
  - key management, privacy assumptions, ACLs/RBAC, PII handling, and auditability for cryptography or privacy-sensitive systems
  - public interfaces, embedding assumptions, safe-by-default behavior, footguns, and secure usage patterns for libraries or frameworks
  - production/runtime code paths versus CI, build, or local developer tooling
- Explain when a vulnerability class would be critical, high, medium, or low in this repository and give a couple of concrete examples at each level.
- If a vulnerability class requires attacker control that does not exist in the repo's real-world usage, say so in the severity calibration discussion.
- When possible, point to specific files, components, or controls that ground the threat model.

## Output Contract

When generating a threat model, structure it in Markdown with these sections:

- Overview
- Threat Model, Trust Boundaries, and Assumptions
- Attack Surface, Mitigations, and Attacker Stories
- Severity Calibration (Critical, High, Medium, Low)

The threat model should help a security researcher understand the codebase and its likely security-relevant failure modes. It should be detailed, repository-scoped, and suitable for reuse across unrelated diffs in the same repo.

Within those sections, make sure the output covers:

- repository overview and intended real-world usage
- trust boundaries and assumptions
- attacker stories and out-of-scope attacker stories
- attack surfaces and existing mitigations
- which vulnerability classes matter most in context
- which vulnerability classes are less severe or out of scope in context
- severity calibration with concrete examples at each level
- references to concrete files or controls when those materially ground the model

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
