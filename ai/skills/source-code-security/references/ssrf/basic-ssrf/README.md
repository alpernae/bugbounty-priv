# Server-Side Request Forgery

## Mapping

- Category: `ssrf`
- Slug: `basic-ssrf`
- CWE: `CWE-918`
- Review mode: source-code analysis / SAST triage
- Evidence slug: `basic-ssrf`

## What to look for

- Attacker-controlled input reaching a security-sensitive sink.
- Missing validation, encoding, authorization, canonicalization, signature verification, or safe API usage.
- Framework protections that are disabled, bypassed, or applied at the wrong layer.
- Tenant, role, object ownership, or trust-boundary assumptions.

## Source-to-sink questions

1. Where does untrusted input enter?
2. What transformations happen before the sink?
3. Which guard should stop malicious or unauthorized input?
4. Is the guard actually applied on every reachable path?
5. What safe code pattern should replace the vulnerable pattern?

## Code examples

- JavaScript/TypeScript:
  - `examples/javascript-typescript/vulnerable.ts`
  - `examples/javascript-typescript/safe.ts`
- Python:
  - `examples/python/vulnerable.py`
  - `examples/python/safe.py`
- Java:
  - `examples/java/vulnerable.java`
  - `examples/java/safe.java`
- PHP:
  - `examples/php/vulnerable.php`
  - `examples/php/safe.php`
- Go:
  - `examples/go/vulnerable.go`
  - `examples/go/safe.go`

## Evidence checklist

- [ ] Affected file/function/route identified
- [ ] Source-to-sink trace documented
- [ ] Security control missing or insufficient
- [ ] False-positive checks completed
- [ ] Safe remediation pattern provided
- [ ] Evidence, proof gaps, and validation status recorded in the response or user-requested artifact

## Validation workflow

1. Confirm the entrypoint is reachable from the scan scope.
2. Trace attacker-controlled input to the closest guard and then to the sink.
3. Check whether an existing framework default, middleware, sanitizer, validator, allowlist, encoder, parameterized API, or authorization helper defeats the path.
4. Record counterevidence before promoting the candidate.
5. Prefer a focused unit test, harness, request replay, parser fixture, or static source-to-sink trace that proves the exact behavior.

## False-positive checks

Suppress or downgrade when:

- the code is unreachable, test-only, example-only, or not deployed in the reviewed product surface
- the attacker cannot control the value that reaches the sink
- a guard blocks the exact source-to-sink path on every reachable branch
- the impact is only a best-practice concern without a concrete security consequence
- the attacker already needs equivalent privilege and no privilege boundary is crossed

## Impact and remediation

Describe impact in terms of data exposure, state change, code execution, privilege escalation, tenant-boundary break, secret exposure, denial of service, or trust-boundary bypass. Remediation should name the specific control to add or strengthen, such as object-level authorization, parameterized APIs, canonicalization, schema validation, safe parser configuration, output encoding, signature verification, or allowlisted destinations.

## Output fields

When this reference supports a candidate, include:

- affected file/function/route/config
- attacker-controlled source
- closest guard or missing control
- sink or protected decision
- evidence and counterevidence
- validation method and proof gap
- impact, confidence, and remediation
