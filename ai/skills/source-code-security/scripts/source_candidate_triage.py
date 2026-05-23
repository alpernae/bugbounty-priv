#!/usr/bin/env python3
"""Heuristic source/sink/control triage for source-code security review.

This script prioritizes leads. It does not prove vulnerabilities and should not
be used as a report generator.
"""

import argparse
import json
import os
import re
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "target",
    "bin",
    "obj",
}

TEXT_EXTENSIONS = {
    ".asp",
    ".aspx",
    ".c",
    ".cc",
    ".conf",
    ".config",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".json",
    ".kt",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".tf",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

SOURCE_PATTERNS = [
    r"\brequest\.(?:args|form|json|files|cookies|headers|get_json)\b",
    r"\breq\.(?:query|body|params|headers|cookies|files)\b",
    r"\bctx\.(?:query|request|params|body|headers)\b",
    r"\$_(?:GET|POST|REQUEST|COOKIE|FILES|SERVER)\b",
    r"@Request(?:Param|Body|Header|Part)\b",
    r"\bRequest\.(?:Query|Form|Body|Headers|Cookies)\b",
    r"\br\.URL\.Query\(",
    r"\b(?:argv|process\.env|os\.environ)\b",
    r"\b(?:webhook|payload|message|event|job|queue)\b",
]

CONTROL_PATTERNS = [
    r"\b(?:authorize|authorized|permission|policy|guard|can\(|isAdmin|owner|tenant)\b",
    r"\b(?:validate|validator|schema|allowlist|whitelist|enum|parseInt|Number\.isInteger)\b",
    r"\b(?:prepare|execute|bindParam|bindValue|PreparedStatement|SqlParameter)\b",
    r"\b(?:escape|encode|sanitize|DOMPurify|htmlspecialchars|textContent)\b",
    r"\b(?:realpath|canonical|normalize|resolve|safe_join|getCanonicalPath)\b",
    r"\b(?:verify|signature|issuer|audience|algorithms|nonce|state)\b",
    r"\bshell\s*=\s*False\b",
    r"\bredirect\s*:\s*[\"']manual[\"']",
]

RULES = {
    "command-injection": [
        r"\b(?:os\.system|subprocess\.(?:run|Popen|call|check_output)|commands\.getoutput)\b",
        r"\b(?:system|exec|shell_exec|passthru|popen)\s*\(",
        r"\b(?:child_process\.(?:exec|execFile|spawn)|Runtime\.getRuntime\(\)\.exec|ProcessBuilder)\b",
    ],
    "eval-code-injection": [
        r"\b(?:eval|exec|compile|Function)\s*\(",
        r"\b(?:ReflectionClass|Class\.forName|loadClass|CodeDomProvider|CSharpCodeProvider)\b",
    ],
    "sql-injection": [
        r"\b(?:SELECT|INSERT|UPDATE|DELETE)\b.*(?:\+|`|\{|\%s|format\(|sprintf|\.\s*\$)",
        r"\b(?:query|execute|raw|createQuery|SqlCommand)\s*\(.*(?:\+|`|\{|\%s|format\()",
    ],
    "ssrf": [
        r"\b(?:fetch|axios\.|requests\.|urllib\.|httpx\.|Net::HTTP|open-uri|HttpClient|WebRequest)\b",
        r"\b(?:curl_exec|file_get_contents|fopen)\s*\(",
    ],
    "path-traversal": [
        r"\b(?:readFile|createReadStream|FileInputStream|FileSystemResource|send_file|sendFile)\b",
        r"\b(?:open|fopen|unlink|rename|copyfile|download)\s*\(",
    ],
    "zip-slip": [
        r"\b(?:ZipEntry|ZipInputStream|ZipFile|AdmZip|unzip|extractall|ExtractToDirectory)\b",
    ],
    "unsafe-deserialization": [
        r"\b(?:pickle\.loads|pickle\.load|cPickle\.loads|yaml\.load|ObjectInputStream|readObject)\b",
        r"\b(?:unserialize|deserialize|Marshal\.load|BinaryFormatter)\b",
    ],
    "xxe": [
        r"\b(?:DocumentBuilderFactory|SAXParserFactory|XmlReader|XmlDocument|DOMDocument|simplexml_load)\b",
        r"\b(?:DOCTYPE|ExternalEntity|DtdProcessing|LIBXML_NOENT)\b",
    ],
    "xss": [
        r"\b(?:innerHTML|outerHTML|document\.write|dangerouslySetInnerHTML|Html\.Raw|Response\.Write)\b",
        r"\b(?:res\.send|echo|print)\b.*(?:req\.|\$_|request\.)",
    ],
    "secrets": [
        r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']",
        r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"\bsk_(?:test|live)_[A-Za-z0-9]{16,}\b",
    ],
    "jwt-unsafe": [
        r"\bjwt\.decode\s*\([^)]*(?:verify_signature[\"']?\s*:\s*False|verify\s*=\s*False|algorithms\s*=\s*\[?[\"']none)",
        r"\b(?:decode|verify)\s*\([^)]*algorithms\s*:\s*\[[^\]]*[\"']none[\"']",
    ],
    "weak-crypto": [
        r"\b(?:MD5|SHA1|DES|RC4|ECB|Random\(|Math\.random|random\.random)\b",
    ],
    "iac-dangerous-config": [
        r"\b(?:privileged|allowPrivilegeEscalation|hostNetwork|hostPID|hostIPC)\s*:\s*true\b",
        r"\b(?:0\.0\.0\.0/0|\*|Action\s*=\s*\"\*\"|Resource\s*=\s*\"\*\")",
        r"\b(?:/var/run/docker\.sock|hostPath|public-read|PublicAccessBlockConfiguration)\b",
    ],
}

PLACEHOLDER_SECRET = re.compile(
    r"(?i)(example|dummy|fake|test|changeme|change_me|placeholder|redacted|not-a-secret)"
)

TEST_PATH = re.compile(r"(?i)(?:^|[/\\])(?:test|tests|spec|fixtures?|examples?|samples?|mocks?)(?:[/\\]|$)")


def compile_patterns(patterns):
    return [re.compile(pattern) for pattern in patterns]


COMPILED_RULES = {name: compile_patterns(patterns) for name, patterns in RULES.items()}
COMPILED_SOURCES = compile_patterns(SOURCE_PATTERNS)
COMPILED_CONTROLS = compile_patterns(CONTROL_PATTERNS)


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def has_match(patterns, text):
    return any(pattern.search(text) for pattern in patterns)


def matching_labels(patterns, text):
    labels = []
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            labels.append(match.group(0)[:80])
    return labels


def walk_files(root):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = Path(current) / name
            if path.suffix.lower() in TEXT_EXTENSIONS or not path.suffix:
                yield path


def classify_score(category, rel_path, context, source_hits, control_hits):
    score = 2
    notes = []

    if category not in {"secrets", "iac-dangerous-config", "weak-crypto"}:
        if source_hits:
            score += 2
        else:
            notes.append("no nearby attacker-controlled source found")

    if control_hits:
        score -= 2
        notes.append("nearby control pattern present; verify whether it is effective")

    if TEST_PATH.search(rel_path):
        score -= 1
        notes.append("test/example/fixture path; verify deployed reachability")

    if category == "secrets":
        if "PUBLIC KEY" in context:
            score -= 3
            notes.append("public key material is not a secret by itself")
        if PLACEHOLDER_SECRET.search(context):
            score -= 3
            notes.append("placeholder or redacted-looking value")

    if category == "ssrf" and re.search(r"redirect\s*:\s*[\"']manual[\"']|allowlist|allowedHosts", context):
        notes.append("allowlist or manual redirect handling nearby")

    if score >= 4:
        confidence = "high-lead"
    elif score >= 2:
        confidence = "medium-lead"
    else:
        confidence = "low-or-likely-fp"

    return score, confidence, notes


def scan_file(path, root):
    text = read_text(path)
    if not text:
        return []

    rel_path = str(path.relative_to(root))
    lines = text.splitlines()
    findings = []

    for idx, line in enumerate(lines):
        for category, patterns in COMPILED_RULES.items():
            if not has_match(patterns, line):
                continue

            start = max(0, idx - 8)
            end = min(len(lines), idx + 9)
            context = "\n".join(lines[start:end])
            source_hits = matching_labels(COMPILED_SOURCES, context)
            control_hits = matching_labels(COMPILED_CONTROLS, context)
            score, confidence, notes = classify_score(category, rel_path, context, source_hits, control_hits)

            findings.append(
                {
                    "category": category,
                    "file": rel_path,
                    "line": idx + 1,
                    "score": score,
                    "confidence": confidence,
                    "sink_excerpt": line.strip()[:220],
                    "source_hints": source_hits[:4],
                    "control_hints": control_hits[:4],
                    "fp_notes": notes,
                    "next_step": "prove reachability, attacker control, sink impact, and missing effective control",
                }
            )

    return findings


def scan(root):
    root = Path(root).resolve()
    results = []
    for path in walk_files(root):
        results.extend(scan_file(path, root))
    results.sort(key=lambda item: (item["score"], item["category"], item["file"]), reverse=True)
    return results


def print_text(results, max_findings):
    for item in results[:max_findings]:
        print(f"[{item['confidence']}] {item['category']} {item['file']}:{item['line']} score={item['score']}")
        print(f"  sink: {item['sink_excerpt']}")
        if item["source_hints"]:
            print(f"  source hints: {', '.join(item['source_hints'])}")
        if item["control_hints"]:
            print(f"  control hints: {', '.join(item['control_hints'])}")
        if item["fp_notes"]:
            print(f"  fp notes: {'; '.join(item['fp_notes'])}")
        print(f"  next: {item['next_step']}")


def main():
    parser = argparse.ArgumentParser(description="Prioritize source-code security leads with false-positive gates.")
    parser.add_argument("--root", default=".", help="Repository or folder to scan.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--max-findings", type=int, default=80)
    args = parser.parse_args()

    results = scan(args.root)
    if args.format == "json":
        print(json.dumps(results[: args.max_findings], indent=2))
    else:
        print_text(results, args.max_findings)
        print(f"\nscanned_leads={len(results)} shown={min(len(results), args.max_findings)}")


if __name__ == "__main__":
    main()
