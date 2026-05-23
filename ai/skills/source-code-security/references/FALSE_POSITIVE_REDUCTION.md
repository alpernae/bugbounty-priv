# False Positive Reduction

Before promoting any source-code candidate, prove the candidate survives all gates below. Scanner output, grep hits, examples, project memory, and agent claims are leads only.

## Four required gates

1. Reachability: a route, job, CLI command, webhook, GraphQL resolver, WebSocket handler, parser, or trusted-to-untrusted boundary can execute the code.
2. Attacker control: the relevant value comes from request data, uploaded files, headers, cookies, queue payloads, third-party webhooks, tenant-controlled records, or compromised-but-in-scope lower-privilege actors.
3. Sensitive sink: the value reaches a security-sensitive API such as SQL execution, shell/process launch, template rendering, filesystem access, archive extraction, outbound HTTP, deserialization, XML parsing, token verification, redirect, logging, or policy decisions.
4. Missing effective control: validation, authorization, escaping, parameterization, canonicalization, signature verification, framework defaults, or central middleware do not actually stop the exploit path.

If one gate is missing, keep the item as an unverified suspicion or suppress it with exact counterevidence.

## Common false-positive blockers

- SQL: ORM/query-builder parameter binding, stored constants only, strict enum mapping, numeric parsing before interpolation, or concatenation outside executable SQL.
- Command execution: argument-array APIs with `shell=False`, strict allowlists, fixed command plus validated primitive arguments, no shell metacharacter interpretation.
- XSS: React/Vue/Angular text interpolation, framework autoescaping, `textContent`, trusted sanitizer with the right profile, or data never rendered into HTML/JS/URL context.
- SSRF: fixed upstream host, strict scheme/host allowlist, DNS and IP range checks after redirects, re-resolution at connect time, metadata/private range blocking, and no attacker-controlled proxy.
- Path traversal and zip slip: canonical target path check after path join or archive entry resolution, no symlink overwrite, and storage outside executable/web-served roots.
- Deserialization: typed JSON or protobuf only, signed/encrypted blobs with server-side keys, class allowlists, or data generated only by trusted server code.
- JWT/OAuth: explicit algorithm allowlist, issuer and audience checks, key type matched to algorithm, exact redirect URI matching, and state/nonce validation.
- Secrets: public keys, placeholders, example-only values, test fixtures, generated dummy tokens, or values not accepted by any live service.
- Dependencies: vulnerable package not on a reachable path, not present in the deployed lockfile, patched by backport, or affected feature unused.
- IaC/config: example/dev-only manifests, non-deployed modules, compensating admission policies, private networking, or external enforcement documented in deployment pipeline.

## Promotion rules by class

- Access control: require a concrete object, role, tenant, route or service method, and a missing or bypassed authorization decision. Do not report when the caller already has equivalent privilege or the data is intentionally public.
- XSS: require a browser sink in the right context and meaningful execution impact. Self-XSS, alert-only reflected XSS, and values encoded by framework defaults should not become report-ready findings.
- SSRF: require attacker control over the final URL or fetch target and meaningful reachable impact. Fixed upstreams, post-redirect IP filtering, and private-range blocking are strong counterevidence.
- Secrets: require evidence the value is real, in scope, and meaningful. Public keys, placeholders, examples, dummy tokens, and non-accepted values are suppressors.
- Dependencies: require the vulnerable package version in the deployed dependency graph and the affected feature reachable from an in-scope path.
- DoS: require service-level or cross-tenant availability impact. Single-user slowdown, unrealistic payload size, or missing reachability is not enough.
- Supply chain and CI: require attacker-controlled code, artifact, package, or metadata reaching privileged secrets, publishing, signing, deployment, or cloud permissions.

## Isolated verification pass

For every reproduced finding, re-check from scratch using only the minimum context needed:

1. Locate the source and sink again without relying on prior notes.
2. Re-read the framework or project guard that should block the issue.
3. Produce a minimal safe proof: unit test, request shape, local fixture, or code-level reachability proof.
4. Mark the status as `isolated verified finding` only if the proof still holds.

## Output rule

Do not create report-ready output for grep-only or scanner-only results. Use `scripts/source_candidate_triage.py` to prioritize leads, then manually prove the gates and record proof gaps in the response or in a user-requested artifact.

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
