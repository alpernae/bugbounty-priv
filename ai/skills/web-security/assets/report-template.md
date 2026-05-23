# HackerOne Report Template

## Title

`[Weakness] Impact in affected endpoint/action`

Example: `BOLA allows cross-tenant invoice download via /api/invoices/{id}`

## Summary

One or two sentences:

- What is vulnerable?
- Who can exploit it?
- What is the impact?

## Program and Scope

- Program:
- Asset:
- Environment:
- Scope reference:
- Test accounts used:
  - Attacker account:
  - Victim/second owned account:
- Testing date:

## Weakness Mapping

- HackerOne weakness:
- CWE:
- OWASP Top 10:
- OWASP API Top 10:
- WSTG section:

## Affected Endpoint(s)

```http
METHOD /path
Host: app.example.test
```

## Preconditions

- Account/role required:
- Object/resource required:
- Feature flag/subscription needed:
- User interaction needed:

## Steps to Reproduce

1. Log in as account A.
2. Create or identify owned test object A.
3. Log in as account B.
4. Create or identify owned test object B.
5. Send the baseline request as account B.
6. Replay or modify the request as account A.
7. Observe unauthorized data/action.

## Evidence

### Baseline expected behavior

```http
<request/response with secrets redacted>
```

### Vulnerable behavior

```http
<request/response with secrets redacted>
```

## Expected Behavior

The server should verify that the authenticated user is authorized for the requested object/action and return `403` or equivalent when not authorized.

## Actual Behavior

The server permits unauthorized access/action.

## Impact

Explain:

- Data/action exposed.
- Affected users/tenants.
- Required privileges.
- Business risk.
- Chainability.

## Severity Rationale

- Recommended severity:
- Why:
- Limiting factors:

## Root Cause Hypothesis

Example:

The endpoint checks authentication but does not enforce object ownership or tenant-level authorization before returning the resource.

## Remediation

- Enforce server-side authorization on every object/action.
- Use deny-by-default access checks.
- Do not rely on UI/client-side filters.
- Add object ownership/tenant checks in service layer.
- Add regression tests for cross-user and cross-tenant access.
- Log authorization failures.

## Retest Plan

- Same user allowed.
- Same tenant different user denied unless explicitly shared.
- Cross-tenant denied.
- Lower role denied for privileged action.
- Alternate method/version denied.
- Raw response contains only authorized fields.

## Redaction Notes

- Tokens/cookies masked.
- PII masked or synthetic.
- No third-party data accessed.
