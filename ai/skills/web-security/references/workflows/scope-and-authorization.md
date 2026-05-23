# Scope And Authorization Workflow

## Purpose

Use this reference before live web or API testing. It defines what is authorized, what accounts and data can be used, and when testing must stop or downgrade.

## Workflow

1. Identify asset, program, environment, and allowed actions.
2. Confirm production, staging, localhost, CTF, or lab rules.
3. Record permitted accounts, roles, tenants, and test data.
4. Record out-of-scope actions such as destructive testing, brute force, DoS, social engineering, persistence, or third-party attacks.
5. Read `scope.md` when present.
6. Read `.github/instructions/memory.md` as context only when present.

## Account Controls

For authorization testing, prefer:

- anonymous control
- Account A owner/member
- Account B same-tier non-owner
- privileged role only when allowed

Keep account data synthetic and low sensitivity.

## Validation Guidance

Before sending requests, define expected safe behavior for each role. For example, Account A should receive `403` or `404` when requesting Account B private object, while Account B should receive `200`.

## False-Positive Checks

Suppress or downgrade when the asset is out of scope, the test data is not owned/authorized, the action is self-only, or the behavior is intentionally public.

## Stop Conditions

Stop or downgrade when:

- scope is unclear and the action is not low-risk
- the test would affect real users or third-party systems
- proof already demonstrates impact
- the next step would be destructive or high volume

## Output Fields

Record asset, environment, accounts, roles, tenant/object ownership, allowed tests, forbidden actions, assumptions, and proof gaps.
