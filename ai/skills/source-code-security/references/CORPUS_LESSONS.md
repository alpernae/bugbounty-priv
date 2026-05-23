# Corpus Lessons

This reference captures durable patterns learned from the local training corpus installed under `tmp/source-code-skill-training`:

- `Broken-Vulnerable-Code-Snippets`
- `vulnerable-code-examples`

The corpus includes realistic and intentionally broken snippets. Use it for pattern calibration, not as a benchmark truth source.

## Practical lessons

- File names and vulnerability folder names are useful hints, but code still needs source-to-sink proof. Several examples contain mixed sinks, placeholder secrets, or missing imports.
- Good positive examples combine a real source, a dangerous sink, and a missing control in a reachable handler or parser.
- Good safe examples do more than "sanitize input"; they move to safer APIs or enforce a precise allowlist/canonicalization/signature check.
- Training snippets often contain deliberate shortcuts. Do not copy them verbatim into reports or skill examples unless the surrounding code remains realistic and legally reusable.

## Category calibration

- Command injection: require attacker influence over shell metacharacters, command names, or arguments. Lower confidence when the code uses argument-array APIs with `shell=False` or a strict enum-to-command map.
- SQL injection: require executable SQL built from untrusted data. Lower confidence for parameterized `execute`, ORM query builders with bound values, numeric casts, or fixed SQL fragments.
- Path traversal: require attacker influence over a filesystem path and a sensitive read/write/delete/extract operation. Lower confidence when the code normalizes and checks the joined path against the intended root.
- Zip slip: require archive entry names written under an extraction root. Safe examples must normalize the destination after joining root plus entry and reject paths outside root.
- SSRF: require attacker-controlled URL, host, path-to-host pivot, or redirect influence reaching a server-side HTTP client. Lower confidence for fixed upstreams or strict allowlists with redirect and IP-range handling.
- Unsafe deserialization: require untrusted serialized bytes entering a powerful deserializer such as pickle, PHP `unserialize`, Java `ObjectInputStream`, Ruby `Marshal`, or unsafe YAML. Lower confidence for signed server-only blobs or typed JSON.
- XXE/XML: require an XML parser configuration that allows DTDs, external entities, or network/file resolution. Lower confidence when parser features explicitly disable those behaviors.
- XSS: require untrusted data entering an HTML, attribute, URL, JavaScript, CSS, SVG, or DOM sink in the browser. Lower confidence for framework text interpolation and correct contextual encoding.
- Secrets: require a credential-looking value that plausibly authenticates to a real service. Lower confidence for public keys, obvious examples, placeholders, tests, and generated fake tokens.
- IaC/config: require deployed configuration or a path from source to deployment. Lower confidence for examples, disabled modules, or policies enforced elsewhere.
- SCA/dependency: require an affected version in the actual lock/deployment path plus reachable vulnerable functionality. Do not report version-only matches as exploitable findings.

## Review phrasing

Use direct status language:

- `unverified suspicion`: source, sink, or control is missing.
- `reproduced finding`: the issue works in the current repo context.
- `isolated verified finding`: a separate pass re-derived the claim and confirmed the minimal proof.

Avoid phrases such as "possibly vulnerable" in report-ready output; state the missing evidence instead.

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
