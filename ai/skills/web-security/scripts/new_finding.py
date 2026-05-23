#!/usr/bin/env python3
import argparse
from pathlib import Path
from datetime import datetime, timezone
import re

WEAKNESS_MAP = {
    "bola": ("CWE-639 / CWE-862 / CWE-863", "A01 Broken Access Control", "API1 Broken Object Level Authorization"),
    "bfla": ("CWE-862 / CWE-863", "A01 Broken Access Control", "API5 Broken Function Level Authorization"),
    "xss": ("CWE-79", "A03 Injection", "N/A"),
    "csrf": ("CWE-352", "A01 Broken Access Control", "API5 if API action"),
    "sqli": ("CWE-89", "A03 Injection", "API8/API10 depending context"),
    "ssrf": ("CWE-918", "A10 Server-Side Request Forgery", "API7 Server Side Request Forgery"),
    "idor": ("CWE-639 / CWE-862 / CWE-863", "A01 Broken Access Control", "API1 Broken Object Level Authorization"),
    "mass-assignment": ("CWE-915", "A01 Broken Access Control", "API3 Broken Object Property Level Authorization"),
    "info-disclosure": ("CWE-200", "A01/A02/A05 depending data", "API3/API8/API9"),
    "api-key-exposure": ("CWE-798 / CWE-522", "A02/A05", "API8"),
    "command-injection": ("CWE-78", "A03 Injection", "API8/API10 depending context"),
    "rce": ("CWE-94 / CWE-78", "A03 Injection", "API8/API10 depending context"),
    "dns-zone-takeover": ("CWE-610", "A05 Security Misconfiguration", "N/A"),
    "subdomain-takeover": ("CWE-610", "A05 Security Misconfiguration", "N/A"),
}

def slugify(value: str) -> str:
    value = re.sub(r"https?://", "", value.lower())
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:80] or "asset"

def main():
    ap = argparse.ArgumentParser(description="Create a HackerOne finding draft for a validated or user-requested web security issue.")
    ap.add_argument("--title", required=True)
    ap.add_argument("--weakness", required=True)
    ap.add_argument("--asset", required=True)
    ap.add_argument("--program", default="TBD")
    ap.add_argument("--out", default="finding.md")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    now_iso = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    cwe, owasp, api = WEAKNESS_MAP.get(args.weakness, ("TBD", "TBD", "TBD"))
    content = f"""# {args.title}

## Summary

TBD

## Program and Scope

- Program: {args.program}
- Asset: {args.asset}
- Testing date: {now.date().isoformat()}
- Test accounts: TBD

## Weakness Mapping

- Weakness key: {args.weakness}
- CWE: {cwe}
- OWASP Top 10: {owasp}
- OWASP API Top 10: {api}

## Affected Endpoint

```http
METHOD /path HTTP/1.1
Host: example.test
```

## Steps to Reproduce

1. TBD

## Evidence

```http
TBD
```

## Expected Behavior

TBD

## Actual Behavior

TBD

## Impact

TBD

## Severity Rationale

TBD

## Remediation

TBD

## Retest Plan

TBD

## Redaction Notes

Secrets and PII must be redacted.
"""
    Path(args.out).write_text(content, encoding="utf-8")
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
