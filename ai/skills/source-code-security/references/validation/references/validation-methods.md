# Validation Methods Decision Table

## Purpose

Use this reference to choose the strongest bounded validation method for a candidate finding. The goal is to prove or falsify the exact source-to-sink claim without unnecessary setup or unsafe actions.

## Workflow

1. Classify the candidate by sink and impact.
2. Select the first feasible method from the table.
3. Run a bounded proof when safe.
4. If blocked, record the blocker and use the fallback.
5. Decide `reportable`, `suppressed`, `not_applicable`, or `deferred`.

## Method Table

| Candidate Type | Preferred Method | Fallback | Evidence |
|---|---|---|---|
| Crash or parser DoS | Minimal fixture plus debug/test run | Static guard and exception containment trace | crash, stack, handled error, or containment proof |
| Memory safety | ASan/valgrind plus reproducer | Non-interactive debugger trace | sanitizer finding, backtrace, or proof gap |
| Authz/tenant bypass | Account A vs Account B interface replay | Code trace of ownership checks | status/body diff and object ownership evidence |
| Injection | Harmless semantic delta test | Source-to-query/sink trace | changed query behavior, timing, error, or sink path |
| SSRF/outbound fetch | Owned callback or local listener | URL parser and egress-control trace | callback hit or exact block evidence |
| CVE/advisory | Version plus vulnerable code path | Seed row closure with counterevidence | reachable vulnerable symbol or safe version evidence |

## Command Examples

```bash
valgrind --error-exitcode=99 ./parser_fixture ./pocs/crash.yml
gdb -q -batch -ex run -ex bt -ex quit --args ./parser_fixture ./pocs/crash.yml
curl -i "$BASE/api/projects/$OTHER_PROJECT" -H "Authorization: Bearer $TOKEN_A"
```

## False-Positive Checks

Suppress when the exact path is blocked, the source is not attacker-controlled, the code is not reachable, or the vulnerable version/path is not present.

## Output Fields

Record method, command or trace, observed evidence, counterevidence, disposition, confidence, and proof gaps.
