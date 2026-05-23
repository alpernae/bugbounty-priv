#!/usr/bin/env python3
"""Detect likely exposed key providers and write safe evidence guidance.

This script does not call third-party APIs. It builds safe validation guidance from
provider patterns so raw secrets are not pasted into reports or shell history.
"""
import argparse, re
from pathlib import Path
from datetime import datetime, timezone

PATTERNS = [
    ("github-token", re.compile(r"(?:ghp|github_pat|gho|ghu|ghs)_[A-Za-z0-9_]{20,}"), "GET https://api.github.com/user with Authorization: Bearer $DISCLOSED_GITHUB_TOKEN"),
    ("aws-access-key-id", re.compile(r"AKIA[0-9A-Z]{16}"), "aws sts get-caller-identity with AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY env vars"),
    ("sendgrid-token", re.compile(r"SG\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "GET https://api.sendgrid.com/v3/scopes with Authorization: Bearer $DISCLOSED_SENDGRID_TOKEN"),
    ("slack-webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[A-Za-z0-9]+"), "POST empty JSON to webhook only if policy allows; do not send visible messages"),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9\-]+"), "POST https://slack.com/api/auth.test with Authorization: Bearer $DISCLOSED_SLACK_TOKEN"),
    ("stripe-secret", re.compile(r"sk_(?:live|test)_[A-Za-z0-9]{20,}"), "Use only provider-approved auth/scope metadata endpoint; never create/list charges/customers"),
    ("google-api-key", re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Check key restrictions safely; avoid quota-consuming calls"),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----"), "Do not use. Report exposed private key and recommend revocation/rotation."),
]

def redact(s: str) -> str:
    if len(s) <= 12:
        return s[:2] + "..." + s[-2:]
    return s[:6] + "..." + s[-4:]

def main():
    ap = argparse.ArgumentParser(description="Analyze possible exposed API keys and create safe validation guidance.")
    ap.add_argument("--input", required=True, help="File containing suspected secrets or snippets")
    ap.add_argument("--asset", required=True)
    ap.add_argument("--program", default="TBD")
    ap.add_argument("--out", default="api-key-exposure-triage.md")
    args = ap.parse_args()

    text = Path(args.input).read_text(encoding="utf-8", errors="ignore")
    findings = []
    for provider, pattern, validation in PATTERNS:
        for m in pattern.finditer(text):
            findings.append((provider, redact(m.group(0)), validation))

    now = datetime.now(timezone.utc)
    outfile = Path(args.out)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    body = [
        "# API Key Exposure Triage\n",
        "## Metadata\n",
        f"- Created at: {now.replace(microsecond=0).isoformat().replace('+00:00','Z')}\n",
        f"- Program: {args.program}\n",
        f"- Asset: {args.asset}\n",
        "- Status: needs manual review\n",
        "- Report ready: false\n",
        "## Summary\n",
        f"Detected {len(findings)} potential exposed secret(s). Raw secret values are intentionally not written.\n",
        "## Candidate secrets\n",
    ]
    if not findings:
        body.append("No known patterns matched. Review manually.\n")
    else:
        for provider, redacted, validation in findings:
            body.append(f"- Provider/key type: `{provider}`\n  - Redacted: `{redacted}`\n  - Safe validation guidance: {validation}\n")
    body.extend([
        "\n## Safety boundaries followed\n",
        "- Do not mutate third-party resources.\n- Do not list customer data.\n- Store raw secrets only in local env vars.\n- Redact all tokens in evidence.\n",
        "## References used\n",
        "- `references/api/api-key-exposure/README.md`\n- `references/api/api-key-exposure/keyhacks-validation-playbook.md`\n",
    ])
    outfile.write_text("\n".join(body), encoding="utf-8")
    print(f"Wrote {outfile}")

if __name__ == "__main__":
    main()
