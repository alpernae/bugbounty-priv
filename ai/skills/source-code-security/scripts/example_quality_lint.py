#!/usr/bin/env python3
"""Lint source-code-skill reference examples for quality problems."""

import argparse
import re
import sys
from pathlib import Path

EXPECTED = {
    "javascript-typescript": ("vulnerable.ts", "safe.ts"),
    "python": ("vulnerable.py", "safe.py"),
    "java": ("vulnerable.java", "safe.java"),
    "php": ("vulnerable.php", "safe.php"),
    "go": ("vulnerable.go", "safe.go"),
}

GENERIC_MARKERS = re.compile(r"(?i)(review note|todo|tbd|sanitize here|fix me|vulnerable code goes here)")
SAFE_CONTROL_MARKERS = re.compile(
    r"(?i)(prepare|execute|bind|allowlist|validate|verify|canonical|normalize|resolve|startsWith|shell=False|textContent|DOMPurify|issuer|audience|signature|safe_join|escape|encode)"
)
RISKY_MARKERS = re.compile(
    r"(?i)(eval|exec|system|shell_exec|pickle|unserialize|SELECT .*\+|innerHTML|document\.write|fetch\(|requests\.|FileInputStream|ZipEntry|jwt\.decode)"
)


def compact(text):
    text = re.sub(r"(?m)^\\s*(#|//).*?$", "", text)
    text = re.sub(r"\\s+", "", text)
    return text


def non_empty_lines(text):
    return [line for line in text.splitlines() if line.strip()]


def warn(warnings, path, message):
    warnings.append(f"{path}: {message}")


def lint_pair(vuln_path, safe_path, slug, warnings, deep=False):
    vuln = vuln_path.read_text(encoding="utf-8", errors="ignore")
    safe = safe_path.read_text(encoding="utf-8", errors="ignore")

    for path, text in ((vuln_path, vuln), (safe_path, safe)):
        if GENERIC_MARKERS.search(text):
            warn(warnings, path, "generic marker/comment found")
        if len(non_empty_lines(text)) < 6:
            warn(warnings, path, "example is too short to show realistic source-to-sink context")

    if compact(vuln) == compact(safe):
        warn(warnings, vuln_path.parent, "vulnerable and safe examples are effectively identical")

    if deep and not RISKY_MARKERS.search(vuln):
        warn(warnings, vuln_path, "vulnerable example has no obvious risky sink marker")

    if deep and not SAFE_CONTROL_MARKERS.search(safe):
        warn(warnings, safe_path, "safe example has no obvious mitigation marker")

    if slug == "zip-slip":
        combined_vuln = vuln.lower()
        combined_safe = safe.lower()
        if "zip" not in combined_vuln or "zip" not in combined_safe:
            warn(warnings, vuln_path.parent, "zip-slip examples should demonstrate archive extraction, not plain download")
        if not any(token in combined_safe for token in ("canonical", "normalize", "resolve", "startswith", "hasprefix")):
            warn(warnings, safe_path, "zip-slip safe example should check normalized destination against extraction root")


def lint(skill_root, deep=False):
    references = Path(skill_root) / "references"
    warnings = []
    for readme in references.rglob("README.md"):
        folder = readme.parent
        examples = folder / "examples"
        if not examples.is_dir():
            continue
        slug = folder.name
        for lang, names in EXPECTED.items():
            lang_dir = examples / lang
            vuln_path = lang_dir / names[0]
            safe_path = lang_dir / names[1]
            if not vuln_path.exists() or not safe_path.exists():
                warn(warnings, lang_dir, "missing vulnerable/safe pair")
                continue
            lint_pair(vuln_path, safe_path, slug, warnings, deep=deep)
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Lint source-code-skill reference examples.")
    parser.add_argument("skill_root", nargs="?", default=".")
    parser.add_argument("--deep", action="store_true", help="Also apply broad risky/safe marker heuristics.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when warnings are found.")
    args = parser.parse_args()

    warnings = lint(args.skill_root, deep=args.deep)
    for item in warnings:
        print(item)
    print(f"warnings={len(warnings)}")
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
